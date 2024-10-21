import pandas as pd
import json, re, os, sys, time, datetime, random
from tqdm import tqdm
import tiktoken
from time import sleep

from dogeneval.utils.llm.llms import get_azure_model

from dogeneval.utils.parser import try_parse_json
from dogeneval.utils.mongodb import save_result

from loguru import logger

MAPPING_PROMPT = """你是核心网运维工程师，你的任务是判断产品文档中的一个知识点能否用于生成一系列题目模板中的若干类题目。

<题目模板列表>
{template_list}
</题目模板列表>

<知识点描述>
{kp_title}
</知识点描述>

<知识点内容>
{kp_content}
</知识点内容>

返回一个json，表示你对上述知识点的内容能否生成上述{template_cnt}个模板的题目的判断，不要考虑该知识点是否有必要生成对应任务，要从生成题目的内容是否有足够好的质量和准确性进行考虑。格式如下：

{{
    "(模板1名称)": {{
        "choose": true/false,
        "reason": "..."
    }}, ...
}}

你返回的内容开头不能是```json，直接返回json内容即可。
"""


def format_template_example(template_data):
    template = template_data['template']
    description = template_data['description']
    fields = template_data['fields']
    name = f"{template_data['L1']}-{template_data['L2']}-{template_data['L3']}".replace("/", "")

    return json.dumps({
        "name": name,
        "description": description,
        "template": template,
        "fields": fields,
    }, ensure_ascii=False, indent=4)

def format_kp_templ_mapping_prompt(kp_title, kp_content, template_list, tem_cnt=10):
    # 以tem_cnt为size，将template_list分割
    template_list = [template_list[i:i + tem_cnt] for i in range(0, len(template_list), tem_cnt)]
    prompts = []
    for templates in template_list:

        template_example = "\n".join([format_template_example(template_data) for template_data in templates])

        prompt = MAPPING_PROMPT.format(**{
            "template_list": template_example,
            "kp_title": kp_title,
            "kp_content": kp_content,
            "template_cnt": len(templates),
            })
        
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
        kp_title = row["描述"]
        kp_content = row["内容"]

        row_json = eval(row.to_json())

        prompts = format_kp_templ_mapping_prompt(kp_title, kp_content, templates, tem_cnt=6)

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
