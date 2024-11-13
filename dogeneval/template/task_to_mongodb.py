from dogeneval.utils.mongodb import save_result
from dogeneval.template.ktasks import load_ktasks
import json

if __name__ == "__main__":
    ktasks, require_scene_ktasks = load_ktasks()
    with open("/home/junetheriver/codes/qa_generation/huawei/dogeneval/template/ktask_fcc.json", "r") as f:
        ktask_fcc = json.load(f)
    
    for ktask in ktasks:
        ktask.update(ktask_fcc.get(ktask["task_name"], {
            "issues": [],
            "constraints": [],
            "checks": []
        }))
        save_result(ktask, "Tasks")
