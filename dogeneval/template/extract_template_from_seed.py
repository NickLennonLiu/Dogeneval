import pandas as pd
from dogeneval.utils.llm.llms import get_openai_model, get_azure_model
from dogeneval.utils.parser import try_parse_json
from tqdm import tqdm
from loguru import logger
import json

PROMPT = """下面我将提供给你一个评测题目的所属类别和题目文本，请你提取这个题目的模板。请注意，题目中可能包含一些针对大模型的提示说明，你需要识别出这些内容，将其作为模版的一部分，对于可能发生变动的部分，作为模板中的待填充字段，并给出字段的具体解释。

你的返回内容需要符合如下格式：

{{
    "L1": "Abilities",
    "L2": "Task",
    "L3": "Scene",
    "description": "该题型的定义，描述",
    "template": "",
    "fields": [

    ],
    "system_prompt": "提问问题前对大模型的解释说明",
    "output_requirements": "对模型生成答案的要求",
    "examples": [
        
    ],
    "requirements": "自动化生成QA时所需要服从的要求，作为prompt提供给生成QA的大模型",
    "quality_assess": "针对生成的QA进行质量评估的标准"
}}

示例如下：

题目类别：代码\/MML生成-NL2MML-配置助理
====题目====
你是系统工程师，需要根据参数写业务脚本\n\n下面是一个例子：\n参数：\n#步骤获取NS索引：76；DNN名称：CMIOT5GDCDJ1NB.ZJ；SST标识：128-2C7155；客户：某某企业\n业务脚本：\nSTART\nADD PLMNNS: NSIDX=76, PLMNIDX=0, SST=128, SD=\"2C7155\", STATE=ACTIVE, DESC=\"某某企业\";\nADD NFNS: NFTYPE=NfAMF, NSIDX=76, DESC=\"某某企业\";\nADD LOCALNSDNN:SUBRANGE=HOME_USER, SST=128, SD=\"2C7155\", DNN=\"CMIOT5GDCDJ1NB.ZJ\", CORRECTTYPE=DNN_CORRECTION, DNNPLCY=Default_DNN_preferred, DISFAILPLCY=STANDARD_MODEL;\nEND\n\n根据参数，严格按例子中业务脚本格式，以START开始END结束，写业务脚本\n参数：\n#步骤获取NS索引：0；DNN名称：CMNET；SST标识：127-EEEEEE；客户：for eMBB
====答案====
START\nADD TACGROUPINNSSF: INDEX=6691, TACGROUPNAME=\"128-2C3248\", TACSTART=\"127002\", TACEND=\"127002\";\nADD TACGROUPINNSSF: INDEX=6692, TACGROUPNAME=\"128-2C3248\", TACSTART=\"127050\", TACEND=\"12705A\";\nADD TACGROUPINNSSF: INDEX=6693, TACGROUPNAME=\"128-2C3248\", TACSTART=\"1270B4\", TACEND=\"1270C1\";\nADD TACGROUPINNSSF: INDEX=6694, TACGROUPNAME=\"128-2C3248\", TACSTART=\"127118\", TACEND=\"127129\";\nADD TACGROUPINNSSF: INDEX=6695, TACGROUPNAME=\"128-2C3248\", TACSTART=\"12717C\", TACEND=\"127188\";\nADD TACGROUPINNSSF: INDEX=6696, TACGROUPNAME=\"128-2C3248\", TACSTART=\"1271E0\", TACEND=\"1271E6\";\nADD TACGROUPINNSSF: INDEX=6697, TACGROUPNAME=\"128-2C3248\", TACSTART=\"127244\", TACEND=\"12724B\";\nADD TACGROUPINNSSF: INDEX=6698, TACGROUPNAME=\"128-2C3248\", TACSTART=\"1272A8\", TACEND=\"1272BF\";\nADD TACGROUPINNSSF: INDEX=6699, TACGROUPNAME=\"128-2C3248\", TACSTART=\"12730C\", TACEND=\"127312\";\nADD TACGROUPINNSSF: INDEX=6700, TACGROUPNAME=\"128-2C3248\", TACSTART=\"127370\", TACEND=\"12737B\";\nEND
===========

{{
    "L1": "代码\/MML生成",
    "L2": "NL2MML",
    "L3": "配置代理",
    "description": "考察大模型生成代码以及MML的能力",
    "template": "你是系统工程师，需要根据参数写业务脚本\n\n下面是一个例子：\n参数:{{param_example}}\n业务脚本:{{script_example}}\n\n根据参数，严格按例子中业务脚本格式，以START开始END结束，写业务脚本\n参数：{{param_question}}",
    "fields": [
        {{
            "name": "param_example",
            "description": "参数示例"
        }},
        {{
            "name": "script_example",
            "description": "业务脚本示例"
        }},
        {{
            "name": "param_question",
            "description": "参数问题"
        }}
    ],
    "examples": [
        
    ],
    "requirements": "答案需要与问题之间存在逻辑关系和关联性",
    "quality_assess": "答案是否与问题相关"
}}

题目类别：{category}
====题目====
{question}
====答案====
{answer}
===========

你返回的内容开头不能是```json，直接返回json内容即可。
"""

def main(demo_file):
    # llm = get_openai_model()
    llm = get_azure_model()
    logger.info(f"{llm.chat('请回复API Test Successfully')}")
    
    generated_templates = []
    
    with open(demo_file, "r") as f:
        demo_data = json.load(f)
    for example_cat, examples in tqdm(demo_data.items()):
        example = examples[0]
        prompt = PROMPT.format(category=example_cat, question=example["Question"], answer=example["Answer"])

        response = llm.chat(prompt)
        json_response = try_parse_json(response)

        if json_response is None:
            logger.error(f"Failed to parse response: {response}")
            generated_templates.append({'category': example_cat, 'output': response, 'examples': examples})
        
        json_response['examples'] = examples

        generated_templates.append(json_response)
    
    with open("templates_v2.json", "w") as f:
        json.dump(generated_templates, f, ensure_ascii=False, indent=4)
    

if __name__ == "__main__":
    demo_file = "/home/junetheriver/codes/qa_generation/huawei/dogeneval/prompts/examples.json"
    main(demo_file)