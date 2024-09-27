import pandas as pd
import os, json, re, datetime
from dogeneval.utils.llm.llms import get_azure_model, get_openai_model
from dogeneval.utils.token_utils import get_qwen_token_num
from tqdm import tqdm
from dogeneval.utils.parser import try_parse_json
from loguru import logger

llm = get_openai_model()
logger.info(llm.chat("测试，请回复API test success"))

bigbench_task_folder = "/home/junetheriver/codes/qa_generation/BIG-bench/bigbench/benchmark_tasks"


# tasks
tasks = []

for task_folder in os.listdir(bigbench_task_folder):
    task_file = os.path.join(bigbench_task_folder, task_folder, "task.json")
    if not os.path.exists(task_file):
        continue
    with open(task_file, "r") as f:
        task = json.load(f)

    task_json = {}

    concern_fields = ['name', 'description', 'keywords', 'metrics', 'examples']
    for field in concern_fields:
        if field in task:
            if field == 'examples':
                task_json[field] = [task[field][0]]
            else:
                task_json[field] = task[field]
    
    tasks.append(task_json)


# abilities_examples
current_abilities_examples_file = "/home/junetheriver/codes/qa_generation/huawei/dogeneval/prompts/examples.json"

abilities_examples = json.load(open(current_abilities_examples_file, "r"))

for cat in abilities_examples:
    abilities_examples[cat] = abilities_examples[cat][0]
    
# ability_templates
from dogeneval.template.abilities import ability_templates

for ability in ability_templates:
    del ability['examples']

ability_template_text = json.dumps(ability_templates, ensure_ascii=False, indent=4)

# PROMPT

PROMPT = """你是华为大模型的评测集构建专家，需要构建一个通信领域的大模型评测体系，现在基于产品文档设计了以下任务，它们的描述、模板如下：

=============================================
{ability_template_text}
=============================================

现在对于BIG-Bench中的这个任务，请你判断如下几点：
1. 这个任务是否已经属于已有任务中的某一个或属于其变种、子集
2. 这个任务是否符合通信领域大模型评测的范畴

这个任务的描述是：
=============================================
{task_description}
=============================================

如果你认为这个任务不适合加入到现有任务中，返回一个json，格式如下：

{{
    "task_name": "任务名称",
    "decision": "reject",
    "reason": "原因"
}}

如果你认为这个任务适合加入到现有任务中，你需要为这个任务设计一个模板，并描述构建此类任务的题目应该采取的步骤或流程，返回一个json，格式如下：

{{
    "task_name": "任务名称（英文）",
    "decision": "accept",
    "reason": "原因",
    "ability": "总结任务的上层抽象能力，如：逻辑推理",
    "task": "翻译成中文的任务描述",
    "template": "题目模板",
    "fields": [
        {{
            "name": "字段名",
            "type": "字段类型",
            "description": "字段描述"
        }}
    ],
    "steps": "题目构建步骤或流程"
}}

你返回的内容需要是纯json，开头不要带```json，结尾不要带```
"""



results = []

for task in tqdm(tasks):
    task_description = json.dumps(task, ensure_ascii=False, indent=4)
    prompt = PROMPT.format(ability_template_text=ability_template_text, task_description=task_description)
    
    token_len = get_qwen_token_num(prompt)
    tqdm.write(f"token_len: {token_len}")
    
    if token_len > (32768 - 4096):
        tqdm.write(f"任务 {task['name']} 的token数超过限制，跳过")
        tqdm.write(prompt)
        continue

    response = llm.chat(prompt)

    response_json = try_parse_json(response)

    if response_json:
        if response_json['decision'] == 'accept':
            tqdm.write(f"任务 {task['name']} 被接受")
            tqdm.write(f"response_json: {response_json}")
        else:
            tqdm.write(f"任务 {task['name']} 被拒绝，原因：{response_json['reason']}")

        response_json['original_task'] = task
        results.append(response_json)
    else:
        tqdm.write(f"任务 {task['name']} 的判断失败")
        results.append({
            "task_name": task['name'],
            "decision": "fail",
            "reason": "判断失败",
            "original_task": task
        })
    
    # 临时保存

    tmp_file = "/home/junetheriver/codes/qa_generation/huawei/data/bigbench_mapping_results.jsonl"
    with open(tmp_file, "at+") as f:
        f.write(json.dumps(results[-1], ensure_ascii=False))
        f.write("\n")

# 保存结果
with open("/home/junetheriver/codes/qa_generation/huawei/data/bigbench_mapping_results.json", "w") as f:
    f.write(json.dumps(results, ensure_ascii=False, indent=4))