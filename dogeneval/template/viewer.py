import pandas as pd
import json, os, sys, re, random, time, datetime

filename = "templates_1014.xlsx"

df = pd.read_excel(filename)

to_json_columns = ['fields', 'examples']

for column in to_json_columns:
    df[column] = df[column].apply(eval)

# 去除弃用列为“是”的行
df = df[df['弃用'] != '是']

df.to_json("templates_1014.json", orient='records', force_ascii=False, indent=4)

def view_template(data):
    system_prompt_flag = True if data['system prompt'] else False
    output_requirements_flag = True if data['output requirement'] else False
    newline = "\n\n"
    merged = f"{data['system prompt']+newline if system_prompt_flag else ''}{data['template']}{newline+data['output requirement'] if output_requirements_flag else ''}"

    data['tmp_template'] = data['template']
    data['template'] = merged

    name = f"{data['L1']}-{data['L2']}-{data['L3']}".replace("/", "")

    with open(f"abilities_1014/{name}.py", 'w') as f:
        f.write(f"full_template = {repr(merged)}\n")

        f.write(f"fields = {data['fields']}\n")

        f.write(f"examples = {data['examples']}\n")

        print(merged)

        print("\n\nFields:\n")

        print(json.dumps(data['fields'], indent=4, ensure_ascii=False))

        # input("Press Enter to continue...")
    
    return data

with open("templates_1014.json") as f:
    templates = json.load(f)

for data in templates:
    data = view_template(data)

with open("templates_1014_v2.json", 'w') as f:
    json.dump(templates, f, ensure_ascii=False, indent=4)