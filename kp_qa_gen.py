import json, os, re, sys, datetime

from tqdm import tqdm
import pandas as pd
from loguru import logger
import time

from dogeneval.utils.llm import llms
from dogeneval.utils.mongodb import save_result
from dogeneval.utils.parser import try_parse_json

from kp_qa_prompts import *



def construct_q2_and_answer(response, template):
    """
    Construct Q2 and Answer from the response of LLM, try best to parse the response and return the question and answer as further as possible.
    """
    response_json = try_parse_json(response)

    if not response_json:
        logger.info(f"Failed to parse response: {response}")
        return None, None, "JSON Parse Error"

    if "error" in response_json:
        logger.error(f"Error in response: {response_json['error']}")
        return response_json, None, f"Error in response: {response_json['error']}"
    
    question = None
    try:
        question = template.format(**response_json)
        answer = response_json["answer"]
    except KeyError as e:
        logger.error(f"KeyError in response: {e}")
        if question:
            return question, None, "Parse Answer Error"
        return response_json, None, f"KeyError in response: {e}"
    
    return question, answer, None


if __name__ == "__main__":

    version_str = f"{datetime.datetime.now():%m%d%H%M}"

    # get LLM
    llm = llms.get_openai_model()
    logger.info(llm.chat("Please reply: Qwen API Test Success!"))

    llm2 = llms.get_azure_model()
    logger.info(llm2.chat("Please reply: Azure API Test Success!"))

    # Load Q1, A1s
    kp_file = "/home/junetheriver/codes/qa_generation/huawei/data/knowledge_points/knowledge_points-09131036.xlsx"
    df = pd.read_excel(kp_file)
    print(df.columns)

    # Load templates
    # template_file = "/home/junetheriver/codes/qa_generation/huawei/data/templates_v3.json"
    template_file = "/home/junetheriver/codes/qa_generation/huawei/dogeneval/template/templates_1014_v2.json"
    with open(template_file) as f:
        templates = json.load(f)

    # Start Pipeline

    total_tries = 0
    total_errors = 0
    total_q2 = 0
    total_matches = 0
    total_unmatches = 0

    qwen_time = 0
    azure_time = 0

    q2 = []

    with tqdm(total=len(df) * len(templates), desc="Processing") as pbar:
        for i, row in df.iterrows():
            if i < 110:
                pbar.update(len(templates))
                continue

            kp_type = row["类型"]
            if kp_type not in  ["处理步骤", "表格", "命令", "具体案例", "代码", "列表", "参数说明", "命令功能"]:
                pbar.update(len(templates))
                continue

            kp_title = row["描述"]
            kp_content = row["内容"]

            if len(kp_content) < 200:
                pbar.update(len(templates))
                continue

            for ability_data in templates:

                pbar.set_description(f"Processing row {i}")
                pbar.set_postfix({"Total": total_tries, "Errors": total_errors, "Q2": total_q2, "Matches": total_matches, "Unmatches": total_unmatches, "Qwen Time": qwen_time, "Azure Time": azure_time})

                total_tries += 1

                # prompt = format_q2_prompt(ability_data, kp_title, kp_content)
                prompt = format_q2_prompt_zeroshot(ability_data, kp_title, kp_content)

                start_time = time.time()
                # response = llm.chat(prompt)
                response = None
                qwen_time += time.time() - start_time

                start_time = time.time()
                response2 = llm2.chat(prompt)
                azure_time += time.time() - start_time

                item = {
                    "L1": ability_data["L1"],
                    "L2": ability_data["L2"],
                    "L3": ability_data["L3"],
                    "template": ability_data["template"],
                    "Q2_response_qwen": response,
                    "Q2_response_azure": response2,
                    "kp_title": kp_title,
                    "kp_content": kp_content,
                    "kp_type": kp_type,
                    "kp_path": row["路径"]
                }
                q2.append(item)

                # 获取答案、构建问题
                template = ability_data["template"]

                # question1, answer1, error1 = construct_q2_and_answer(response, template)
                question1, answer1, error1 = None, None, None
                question2, answer2, error2 = construct_q2_and_answer(response2, template)

                item["Q2_qwen"] = question1
                item["A2_qwen"] = answer1
                item["error_qwen"] = error1

                item["Q2_azure"] = question2
                item["A2_azure"] = answer2
                item["error_azure"] = error2

                if error1 or error2:
                    # 如果这一步有错误，直接保存结果，不再继续
                    # 除非只是answer， 那么要求模型生成一个答案
                    if error1 == "Parse Answer Error" or error2:
                        # TODO: 重新生成答案
                        pass
                    total_errors += 1

                    pbar.update(1)

                    save_result(item, f"Q2-{version_str}")
                    continue
                # Compare A1 and A2, stats the accuracy

                total_q2 += 1

                def check_answer_match(A1, A2):
                    check_prompt = form_check_prompt(A1, A2)
                    response = llm2.chat_json(check_prompt)
                    answer_match = response["match"]
                    return answer_match, response["reason"]
                
                # answer_match_qwen, match_reason_qwen = check_answer_match(kp_content, answer1)
                answer_match_qwen, match_reason_qwen = None, None
                answer_match_azure, match_reason_azure = check_answer_match(kp_content, answer2)

                if answer_match_qwen or answer_match_azure:
                    total_matches += 1
                else:
                    total_unmatches += 1

                item.update({
                    "match_qwen": answer_match_qwen,
                    "reason_qwen": match_reason_qwen,
                    "match_azure": answer_match_azure,
                    "reason_azure": match_reason_azure
                })

                save_result(item, f"Q2-{version_str}")

                pbar.update(1)


    

    with open(f"/home/junetheriver/codes/qa_generation/huawei/data/kp_qa/q2-{version_str}.json", "w") as f:
        json.dump(q2, f, indent=4, ensure_ascii=False)

    df_q2 = pd.DataFrame(q2)
    df_q2.to_excel(f"/home/junetheriver/codes/qa_generation/huawei/data/q2/q2-{version_str}.xlsx", index=False)

