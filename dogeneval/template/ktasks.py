import os
import json

def load_ktasks():
    """
    TODO: 从mongodb中加载任务模板
    返回所有模板
    """
    raise DeprecationWarning("load_ktasks is deprecated, use load_ktasks_from_json instead")
    root_path = "/home/junetheriver/codes/qa_generation/huawei/dogeneval/template/ktasks"
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

def load_ktasks_from_json(filename):
    with open(filename, 'r') as f:
        ktasks = json.load(f)
    return ktasks

