from dogeneval.template.ktasks import load_ktasks
import json

from loguru import logger

def form_question_prompt(ktask):
    prompt = ktask["template"]
    if ktask["system_prompt"]:
        prompt = ktask["system_prompt"] + "\n\n" + prompt
    if ktask["output_requirement"]:
        prompt += "\n\n" + ktask["output_requirement"]
    return prompt

ktasks, require_scene_ktasks = load_ktasks()
for task in ktasks:
    task['template'] = form_question_prompt(task)
ktasks_dict = {ktask["task_name"]: ktask for ktask in ktasks}
logger.info(f"Loaded {len(ktasks)} ktasks")

with open("/home/junetheriver/codes/qa_generation/huawei/dogeneval/template/ktask_fcc.json", "r") as f:
    ktask_fcc = json.load(f)

for ktask in ktasks:
    fcc = ktask_fcc[ktask["task_name"]]
    ktask['issues'] = fcc['issues']
    ktask['constraints'] = fcc['constraints']
    ktask['checks'] = fcc['checks']

with open("ktask_1129.json", "w") as f:
    json.dump(ktasks, f, indent=4, ensure_ascii=False)