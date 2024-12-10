import pandas as pd
import json, re, os, sys, time, datetime, random
from tqdm import tqdm
import tiktoken
from time import sleep

from dogeneval.utils.llm.llms import get_azure_model

from dogeneval.utils.parser import try_parse_json
from dogeneval.utils.mongodb import save_result

from loguru import logger

from .mapping_prompt import MAPPING_PROMPT_ZH, MAPPING_PROMPT_EN

def form_question_prompt(template_data):
    prompt = template_data["template"]
    if template_data["system_prompt"]:
        prompt = template_data["system_prompt"] + "\n\n" + prompt
    if template_data["output_requirement"]:
        prompt += "\n\n" + template_data["output_requirement"]
    return prompt

def format_template_example(template_data):
    template = form_question_prompt(template_data)
    description = template_data['description']
    fields = template_data['fields']
    name = template_data['task_name']
    constraints = template_data.get("constraints", "")
    return json.dumps({
        "task_name": name,
        "description": description,
        "template": template,
        "fields": fields,
        "constraints": constraints
    }, ensure_ascii=False, indent=4)

def format_kp(kp, lang="zh"):
    if lang == "zh":
        return f"""<知识点类型>
{kp["type"]}
</知识点类型>

<知识点描述>
{kp["description"]}
</知识点描述>

<知识点内容>
{kp["content"]}
</知识点内容>
"""
    elif lang == "en":
        return f"""<Knowledge Point Type>
{kp["type"]}
</Knowledge Point Type>

<Knowledge Point Description>
{kp["description"]}
</Knowledge Point Description>

<Knowledge Point Content>
{kp["content"]}
</Knowledge Point Content>
"""

def format_kp_templ_mapping_prompt(kp, template_list, tem_cnt=10, lang="zh"):
    # 以tem_cnt为size，将template_list分割
    template_list = [template_list[i:i + tem_cnt] for i in range(0, len(template_list), tem_cnt)]
    prompts = []
    for templates in template_list:

        template_example = "\n".join([format_template_example(template_data) for template_data in templates])

        if lang == "zh":
            MAPPING_PROMPT = MAPPING_PROMPT_ZH
        else:
            MAPPING_PROMPT = MAPPING_PROMPT_EN

        prompt = MAPPING_PROMPT.format(**{
            "template_list": template_example,
            "kp_format": format_kp(kp, lang),
            "template_cnt": len(templates),
            })
        
        logger.debug(prompt)
        
        # 用openai自带的库计算prompt的token数量
        enc = tiktoken.encoding_for_model("gpt-4o")
        token_count = len(enc.encode(prompt))

        if token_count > 8192:
            print(f"Token count: {token_count}")
            print("Token count exceeds 8192, please split the prompt.")
            print(prompt)
            raise
        
        prompts.append(prompt)
    return prompts

def map_kp_to_templates(kp, templates, llm, lang="zh"):

    prompts = format_kp_templ_mapping_prompt(kp, templates, tem_cnt=6, lang=lang)
    
    row_json = {}

    instructs = []

    for prompt in prompts:
        max_retries = 3
        while max_retries > 0:
            max_retries -= 1
            try:
                response = llm.chat_json(prompt)
                row_json.update(response)
                instructs.append({
                    "instruction": prompt,
                    "input": "",
                    "output": json.dumps(response, ensure_ascii=False)
                })
            except Exception as err:
                sleep(5)
                logger.error(err)
                continue
            break

    mapped_templates = [
        template_data for template_data in templates if row_json.get(template_data["task_name"], {}).get("choose", False)
    ]

    return mapped_templates, instructs
    


if __name__ == "__main__":
    template_file = "/home/junetheriver/codes/qa_generation/huawei/dogeneval/template/templates_1014_v2.json"

    with open(template_file) as f:
        templates = json.load(f)

    print(len(templates))

    kp_file = "/home/junetheriver/codes/qa_generation/huawei/data/knowledge_points/knowledge_points-09131036.xlsx"
    df = pd.read_excel(kp_file)

    max_token_cnt = 0

    llm = get_azure_model()

    results = []

    for i, row in tqdm(df.iterrows(), total=len(df)):
        row_json = eval(row.to_json())

        prompts = format_kp_templ_mapping_prompt(row_json, templates, tem_cnt=6)

        for prompt in prompts:
            max_retries = 3
            while max_retries > 0:
                max_retries -= 1
                try:
                    response = llm.chat_json(prompt)

                    row_json.update(response)
                except Exception as err:
                    sleep(5)
                    logger.error(err)
                    continue
                break

        results.append(row_json)
        save_result(row_json, "kp_template_mapping")
        
        sleep(1)
    
    with open("./kp_mapping_results.json", "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
