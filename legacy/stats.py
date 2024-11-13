import json, os, sys, datetime
import pandas as pd

def count_generated_qas(version_name = 'qa-09021144.json'):
    folder = "/home/junetheriver/codes/qa_generation/huawei/data/generated_qa"
    filename = version_name
    for category in os.listdir(folder):
        with open(os.path.join(folder, category, filename)) as f:
            data = json.load(f)
            print(f"{category}: {len(data)}")

def show_generated_qa(filename, index):
    with open(filename, 'r') as f:
        data = json.load(f)
    q = data[index]
    print(f"Filename: {q['filename']}")
    print("=============Question===============")
    print(q['template'].format(**q['question']))
    print("=============Answer=================")
    print(q['question']['answer'])
    print("====================================")

def format_template_qa(version_name = 'qa-09021920.json'):
    folder = "/home/junetheriver/codes/qa_generation/huawei/data/generated_qa"
    output_dir = "/home/junetheriver/codes/qa_generation/huawei/data/formatted"
    filename = version_name
    for category in os.listdir(folder):
        qas = []
        with open(os.path.join(folder, category, filename)) as f:
            data = json.load(f)
            for q in data:
                question = q['template'].format(**q['question'])
                answer = q['question']['answer']
                qas.append({
                    "filename": q['filename'].replace("/home/junetheriver/datasets/huawei/processed/", ""),
                    "question": question,
                    "answer": answer,
                    "datetime": q['version']
                })
        with open(os.path.join(output_dir, f"{category}.json"), 'w') as f:
            json.dump(qas, f, ensure_ascii=False, indent=4)
        df = pd.DataFrame(qas)
        df.to_csv(os.path.join(output_dir, f"{category}.csv"), index=False, encoding='utf-8-sig')
        

if __name__ == "__main__":
    # count_generated_qas()
    # show_generated_qa("/home/junetheriver/codes/qa_generation/huawei/data/generated_qa/逻辑推理/qa-09021920.json", 51)
    format_template_qa()