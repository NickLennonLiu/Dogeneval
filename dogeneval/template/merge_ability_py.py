import pandas as pd
import json, os
import importlib

if __name__ == "__main__":
    template_dir = "/home/junetheriver/codes/qa_generation/huawei/dogeneval/template/abilities"

    for file in os.listdir(template_dir):
        if file.endswith(".py") and not file.startswith("__"):
            filename = os.path.join(template_dir, file)

            spec = importlib.util.spec_from_file_location(filename, filename)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            print(module.data)