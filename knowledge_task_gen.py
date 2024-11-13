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

def load_ktasks():
    root_path = "./dogeneval/template/ktasks"
    level1s = ["1_recall", "2_transform", "3_apply"]
    ktasks = []
    require_scene_ktasks = []
    for level1 in level1s:
        level1_path = os.path.join(root_path, level1)
        for file in os.listdir(level1_path):
            if file.endswith(".json"):
                with open(os.path.join(level1_path, file), "r") as f:
                    sub_ktasks = json.load(f)
                    ktasks += sub_ktasks
                    if level1 == "3_apply":
                        require_scene_ktasks += [i['task_name'] for i in sub_ktasks]
    return ktasks, require_scene_ktasks

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
                     is_zeroshot, require_scene, example, 
                     version_str, pbar):
    kp_type = row["type"]
    kp_title = row["description"]
    kp_content = row["content"]
    
    start_time = time.time()
    response = llm.chat(qa_generation_prompt)
    gen_time = time.time() - start_time

    template = task['template']

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

    return item, False, match, gen_time

def gen_questions_from_kp(kp_collection_name, name):
    version_str = f"{datetime.datetime.now():%m%d%H%M}"
    random.seed(42)

    # get LLM
    llm = llms.get_azure_model()

    # load knowledge points
    # kp_file = "./data/knowledge_points/knowledge_points-09131036.xlsx"
    # df = pd.read_excel(kp_file)
    # print(df.columns)
    df = load_results_as_df(kp_collection_name)

    # filter kp
    # filter_kp_type = ["处理步骤", "表格", "命令", "具体案例", "代码", "列表", "参数说明", "命令功能", "事实陈述"]
    # df = df[df["type"].isin(filter_kp_type)]
    length_thres = 100
    df = df[df["content"].str.len() >= length_thres]
    # 打乱
    df = df.sample(frac=1).reset_index(drop=True)

    # load ktasks
    ktasks, require_scene_ktasks = load_ktasks()
    for task in ktasks:
        task['template'] = form_question_prompt(task)
    ktasks_dict = {ktask["task_name"]: ktask for ktask in ktasks}
    logger.info(f"Loaded {len(ktasks)} ktasks")

    # load fcc
    with open("/home/junetheriver/codes/qa_generation/huawei/dogeneval/template/ktask_fcc.json", "r") as f:
        ktask_fcc = json.load(f)

    total_tries = 0
    total_errors = 0
    total_questions = 0
    total_matches = 0
    total_unmatches = 0

    gen_time = 0

    kp_qa_gen = []

    with tqdm(total=len(df) * len(ktasks), desc="Processing") as pbar:
        for i, row in df.iterrows():

            # mapping kp to ktasks
            mapped_templates = map_kp_to_templates(row, ktasks, llm)

            # 临时措施，如果匹配得比较多，就不生成选择题和问答题了，而是生成更高级的题目
            if len(mapped_templates) > 6:
                mapped_templates = [i for i in mapped_templates if i["task_name"] not in ["QuestionAnswering", "MultipleChoice"]]

            logger.info(f"Mapped {len(mapped_templates)} templates: {[i['task_name'] for i in mapped_templates]}")

            # generate questions
            for task in mapped_templates:

                total_tries += 1
                pbar.set_description(f"Processing row {i}")
                pbar.set_postfix({"Total": total_tries, "Errors": total_errors, "Questions": total_questions, "Matches": total_matches, "Unmatches": total_unmatches, "Time": gen_time})

                # 选择fewshot or zeroshot
                # 一半概率fewshot，一半概率zeroshot
                if random.random() < 0.6 and len(task.get("examples", [])): # fewshot
                    # 等概率挑选一个example
                    example = random.choice(task["examples"])
                    is_zeroshot = False
                else: # zeroshot          # zeroshot
                    example = None
                    is_zeroshot = True

                if task["task_name"] in require_scene_ktasks:
                    require_scene = True
                else:
                    require_scene = False

                qa_generation_prompt = format_qa_generation_prompt(task, ktask_fcc[task["task_name"]]["constraints"], 
                                                                    row, is_zeroshot, require_scene, example)
                
                retry = 0
                while retry < 3:
                    try:
                        item, error, match, used_time = gen_qa_and_check(llm, 
                                        qa_generation_prompt, row, task, ktask_fcc[task["task_name"]]["checks"], 
                                        is_zeroshot, require_scene, example, 
                                        version_str, pbar)
                        
                        save_result(item, f"{name}-QA_GEN-{version_str}")
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
    # gen_questions_from_kp(emsplus_kp_collection_name, "emsplus")
    gen_questions_from_kp(unc_kp_collection_name, "unc")
