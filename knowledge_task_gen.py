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
logger.add(sys.stderr, level="INFO")

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

def gen_questions_from_kp(kp_collection_name, name, lang="zh", database="Knowledge_Points", task_target_count=10):
    version_str = f"{datetime.datetime.now():%m%d%H%M}"
    # random.seed(42)

    # task count dict
    task_count_dict = {}

    # get LLM
    llm = llms.get_azure_model()

    # load knowledge points
    df = load_results_as_df(kp_collection_name, database=database)

    # filter kp
    length_thres = 200
    df = df[df["content"].str.len() >= length_thres]
    # 打乱
    df = df.sample(frac=1).reset_index(drop=True)

    # load ktasks TODO: 改成从数据库中加载
    ktasks = load_ktasks_from_json("/home/junetheriver/codes/qa_generation/huawei/dogeneval/template/ktask_1129.json")
    for task in ktasks:
        task['template_merged'] = form_question_prompt(task)
    ktasks_dict = {ktask["task_name"]: ktask for ktask in ktasks}
    logger.info(f"Loaded {len(ktasks)} ktasks")

    total_tries = 0
    total_errors = 0
    total_questions = 0
    total_matches = 0
    total_unmatches = 0
    total_quality_1 = 0

    gen_time = 0

    kp_qa_gen = []

    with tqdm(total=len(df) * len(ktasks), desc="Processing") as pbar:
        for i, row in df.iterrows():


            def filter_unfinished_tasks(ktasks, task_count_dict):
                return [i for i in ktasks if not check_success_task_count(task_count_dict, i["task_name"], max_count=task_target_count)]

            unfinished_tasks = filter_unfinished_tasks(ktasks, task_count_dict)

            # mapping kp to ktasks
            mapped_templates, mapping_instructs = map_kp_to_templates(row, unfinished_tasks, llm, lang)
            for instruct in mapping_instructs:
                save_result(instruct, f"{name}-mapping-{lang}-{version_str}", "Instructions")

            logger.info(f"Mapped {len(mapped_templates)} templates: {[i['task_name'] for i in mapped_templates]}")

            # generate questions
            for task in mapped_templates:

                total_tries += 1
                pbar.set_description(f"Processing row {i}")
                pbar.set_postfix({"Total": total_tries, "Errors": total_errors, "Questions": total_questions, "Matches": total_matches, "Unmatches": total_unmatches, "Quality1": total_quality_1, "Time": gen_time})

                # 选择fewshot or zeroshot
                # 一半概率fewshot，一半概率zeroshot
                if random.random() < 1 and len(task.get("examples", [])): # fewshot
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
                                                                    row, is_zeroshot, require_scene, example, lang)
                
                retry = 0
                while retry < 3:
                    try:
                        item, error, match, used_time = gen_qa_and_check(llm, 
                                        qa_generation_prompt, row, task, task["checks"], 
                                        is_zeroshot, require_scene, example, lang, 
                                        name, version_str, pbar)

                        if match and item['quality_score'] == 1:
                            update_success_task_count(task_count_dict, task["task_name"])
                        
                        save_result(item, f"{name}-QA_GEN-{lang}-{version_str}", "DogenEval")
                        break
                    except Exception as e:
                        retry += 1
                        time.sleep(60)
                        logger.error(f"Error in gen_qa_and_check: {e}")
                
                gen_time += used_time
                if error:
                    total_errors += 1
                else:
                    total_questions += 1
                    if match:
                        total_matches += 1
                    else:
                        total_unmatches += 1

                    if item['quality_score'] == 1:
                        total_quality_1 += 1

                pbar.update(1)
                
                kp_qa_gen.append(item)
            
            pbar.update(len(ktasks) - len(mapped_templates))
    
    with open(f"{name}-kp_qa_gen-{version_str}.json", "w") as f:
        json.dump(kp_qa_gen, f, indent=4, ensure_ascii=False)

    df_kp_qa_gen = pd.DataFrame(kp_qa_gen)
    df_kp_qa_gen.to_excel(f"{name}-kp_qa_gen-{version_str}.xlsx", index=False)


if __name__ == "__main__":
    zabbix_kp_collection_name = "zabbix-knowledge_points-11111457"
    emsplus_kp_collection_name = "emsplus-knowledge_points-11111757"
    unc_kp_collection_name = "knowledge_points-10281449"

    book_zh = "book-knowledge_points-zh-11141312"

    task_target_count = 50

    # gen_questions_from_kp(emsplus_kp_collection_name, "emsplus")
    # gen_questions_from_kp(book_zh, "book_zh", "zh")
    gen_questions_from_kp(unc_kp_collection_name, name="unc", database="DogenEval", task_target_count=task_target_count)