import pandas as pd
import json
import os

result_file = "/home/junetheriver/codes/qa_generation/huawei/data/bigbench_mapping_results.json"

df = pd.read_json(result_file)

df.to_excel("/home/junetheriver/codes/qa_generation/huawei/experiments/bigbench_mapping/bigbench_mapping_results.xlsx", index=False)