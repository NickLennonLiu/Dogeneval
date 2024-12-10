"""
以一个知识点为例子，尝试题目生成的整个完整流程
"""

import json, os, re, sys, datetime, random

from tqdm import tqdm
import pandas as pd
from loguru import logger
import time

from dogeneval.validation.quality_control_prompt import form_quality_control_prompt_with_constraints
from dogeneval.utils.llm import llms
from dogeneval.utils.mongodb import save_result, load_results_as_df
from dogeneval.utils.parser import try_parse_json
from dogeneval.validation.quality_control import quality_control, try_answering, check_answer
from dogeneval.kp_template_mapping.mapping import map_kp_to_templates
from dogeneval.template.template_prompt import format_qa_generation_prompt
from dogeneval.template.ktasks import load_ktasks_from_json
logger.remove()
logger.add(sys.stderr, level="DEBUG")

def form_question_prompt(ktask):
    prompt = ktask["template"]
    if ktask["system_prompt"]:
        prompt = ktask["system_prompt"] + "\n\n" + prompt
    if ktask["output_requirement"]:
        prompt += "\n\n" + ktask["output_requirement"]
    return prompt

def construct_qa_and_answer(response, template):
    """
    Construct Q2 and Answer from the response of LLM, try best to parse the response and return the question and answer as further as possible.
    """
    response_json = try_parse_json(response)

    explain = response_json.get("explanation", None)

    if not response_json:
        logger.info(f"Failed to parse response: {response}")
        return None, None, explain, "JSON Parse Error"

    if "error" in response_json:
        logger.error(f"Error in response: {response_json['error']}")
        return response_json, None, explain, f"Error in response: {response_json['error']}"
    
    question = None
    try:
        question = template.format(**response_json)
        answer = response_json["answer"]
    except KeyError as e:
        logger.error(f"KeyError in response: {e}")
        if question:
            return question, None, explain, "Parse Answer Error"
        return response_json, None, explain, f"KeyError in response: {e}"
    
    
    
    return question, answer, explain, None


def gen_qa_and_check(llm, 
                     qa_generation_prompt, row, task, checks, 
                     is_zeroshot, require_scene, example, lang,
                     name, version_str, pbar):
    kp_type = row["type"]
    kp_title = row["description"]
    kp_content = row["content"]
    
    start_time = time.time()
    response = llm.chat(qa_generation_prompt)
    gen_time = time.time() - start_time

    template = task['template_merged']

    item = {
        "task": task["task_name"],
        "kp_type": kp_type,
        "kp_title": kp_title,
        "kp_content": kp_content,
        "template": template,
        "qa_gen_prompt": qa_generation_prompt,
        "qa_gen_response": response,
        "qa_gen_time": gen_time,
        "is_zeroshot": is_zeroshot,
        "require_scene": require_scene,
        "example": example,
        "kp_path": row["path"]
    }

    save_result({
        "instruction": qa_generation_prompt,
        "input": "",
        "output": response
    }, f"{name}-qa_gen-{lang}-{version_str}", "Instructions")

    question, answer, explain, error = construct_qa_and_answer(response, template)

    item["Question"] = question
    item["Answer"] = answer
    item["explain"] = explain
    item["error"] = error

    # quality control
    score, reason, quality_control_prompt = quality_control(question, answer, checks, llm)
    item["quality_score"] = score
    item["quality_reason"] = reason
    item["quality_control_prompt"] = quality_control_prompt

    save_result({
        "instruction": quality_control_prompt,
        "input": "",
        "output": json.dumps({
            "score": score,
            "reason": reason
        }, ensure_ascii=False)
    }, f"{name}-quality_control-{lang}-{version_str}", "Instructions")

    if error:
        return item, True, None

    # 尝试让模型作答
    model_answer, answer_prompt = try_answering(row, question, llm)
    item["Model_Answer"] = model_answer
    item["answer_prompt"] = answer_prompt
    # 检查模型作答是否正确
    match, reason, check_prompt = check_answer(row, question, model_answer, llm)

    item["match"] = match
    item["match_reason"] = reason
    item["check_prompt"] = check_prompt

    save_result({
        "instruction": check_prompt,
        "input": "",
        "output": json.dumps({
            "match": match,
            "reason": reason
        }, ensure_ascii=False)
    }, f"{name}-check_answer-{lang}-{version_str}", "Instructions")

    return item, False, match, gen_time


success_task_count = {}

def gen_questions_from_kp(kp, name, lang="zh"):
    version_str = f"{datetime.datetime.now():%m%d%H%M}"
    random.seed(42)

    # get LLM
    llm = llms.get_azure_model()

    # load knowledge points
    kp = kp

    # load ktasks TODO: 改成从数据库中加载
    ktasks = load_ktasks_from_json("/home/junetheriver/codes/qa_generation/huawei/dogeneval/template/ktask_1129.json")
    for task in ktasks:
        task['template_merged'] = form_question_prompt(task)
    ktasks_dict = {ktask["task_name"]: ktask for ktask in ktasks}
    logger.info(f"Loaded {len(ktasks)} ktasks")

    kp_qa_gen = []

    # mapping kp to ktasks
    mapped_templates, mapping_instructs = map_kp_to_templates(kp, ktasks, llm, lang)

    # 临时措施，如果匹配得比较多，就不生成选择题和问答题了，而是生成更高级的题目
    if len(mapped_templates) >= 5:
        mapped_templates = [i for i in mapped_templates if i["task_name"] not in ["QuestionAnswering", "MultipleChoice"]]
    if len(mapped_templates) >= 5:
        mapped_templates = [i for i in mapped_templates if i["task_name"] not in ["ReadingComprehension", "LogicAnalysis"]]

    logger.info(f"Mapped {len(mapped_templates)} templates: {[i['task_name'] for i in mapped_templates]}")

    # generate questions
    for task in mapped_templates:

        # 如果某个任务类型已经生成足够的题目，就不再生成
        if check_success_task_count(success_task_count, task["task_name"], max_count=1):
            continue

        # 选择fewshot or zeroshot
        # 一半概率fewshot，一半概率zeroshot
        if random.random() < 0.6 and len(task.get("examples", [])): # fewshot
            # 等概率挑选一个example
            example = random.choice(task["examples"])
            is_zeroshot = False
        else: # zeroshot          # zeroshot
            example = None
            is_zeroshot = True

        if task["require_scene"]:
            require_scene = True
        else:
            require_scene = False

        qa_generation_prompt = format_qa_generation_prompt(task, task["constraints"], 
                                                            kp, is_zeroshot, require_scene, example, lang)
        
        retry = 0
        while retry < 3:
            try:
                item, error, match, used_time = gen_qa_and_check(llm, 
                                qa_generation_prompt, kp, task, task["checks"], 
                                is_zeroshot, require_scene, example, lang, 
                                name, version_str, None)

                if match and item['quality_score'] == 1:
                    update_success_task_count(success_task_count, task["task_name"])

                break
            except Exception as e:
                retry += 1
                time.sleep(60)
                logger.error(f"Error in gen_qa_and_check: {e}")

        kp_qa_gen.append(item)
    return kp_qa_gen


def update_success_task_count(task_count_dict, task_name):
    if task_name not in task_count_dict:
        task_count_dict[task_name] = 0
    task_count_dict[task_name] += 1

def check_success_task_count(task_count_dict, task_name, max_count=100):
    if task_name not in task_count_dict:
        return False
    if task_count_dict[task_name] >= max_count:
        return True
    return False

def check_complete(task_count_dict, task_names, max_count=100):
    for task_name in task_names:
        if not check_success_task_count(task_count_dict, task_name, max_count):
            return False
    return True

if __name__ == "__main__":
    kp = {
        "content": """在相关网元均完成本特性的配置后，可以采用以下步骤检查特性工作是否正常：
用户MS签约的QoS版本为rel5或者rel99。
1. 用户MS开机发起附着请求。
2. 用户MS发起PDP激活请求。
3. 查询QoS参数。
进入“MML命令行-UNC”窗口。
[**DSP SMCTX**](../MML/Document/dsp_smctx.html): IDTYPE=显示类型;
预期结果：用户附着成功并且PDP激活成功，用户签约的最大上行速率、最大下行速率已经根据转换规则被修改。""",
        "type": "处理步骤",
        "title": "QoS覆盖特性检查",
        "description": "描述在相关网元均完成QoS覆盖特性配置后，如何通过一系列步骤检查特性工作是否正常。",
        "path": "网络部署/特性部署/UNC特性指南/QoS功能/WSFD-105001 QoS覆盖/unc_2000_feature_om_qos_overwritten_02.html"
    }
    kp_qa_gen = gen_questions_from_kp(kp, "test", "zh")
    with open("demo.json", 'w') as f:
        json.dump(kp_qa_gen, f, ensure_ascii=False, indent=4)