"""
从现有的collection中抽取prompt和response的数据，构造用于微调小模型的指令数据集
"""
from dogeneval.utils.mongodb import load_results_as_df
from dogeneval.validation.filters import main_filter
import json
import random

def load_instruct(df, prompt_col, response_col):
    if isinstance(response_col, str):
        instructions = [
            {
                "instruction": row[prompt_col],
                "input": "",
                "output": row[response_col]
            }
            for _, row in df.iterrows()
        ]
    elif isinstance(response_col, dict):
        instructions = [
            {
                "instruction": row[prompt_col],
                "input": "",
                "output": json.dumps({
                    key_abbr: row[key] for key, key_abbr in response_col.items()
                }, ensure_ascii=False)
            }
            for _, row in df.iterrows()
        ]
    return instructions

def split_train_test(instructions, train_ratio=0.8):
    random.shuffle(instructions)
    split_idx = int(len(instructions) * train_ratio)
    train_instructions = instructions[:split_idx]
    test_instructions = instructions[split_idx:]
    return train_instructions, test_instructions

def save_json(instructions, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(instructions, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    df = load_results_as_df("unc-QA_GEN-11131408")
    df = main_filter(df)
    qa_gen_instructions = load_instruct(df, "qa_gen_prompt", "qa_gen_response")
    quality_instructions = load_instruct(df, "quality_control_prompt", {
        "quality_score": "score",
        "quality_reason": "reason"
    })
    check_instructions = load_instruct(df, "check_prompt", {
        "match": "match",
        "match_reason": "reason"
    })
    answer_instructions = load_instruct(df, "answer_prompt", "Model_Answer")
    
    train_qa_gen, test_qa_gen = split_train_test(qa_gen_instructions)
    train_quality, test_quality = split_train_test(quality_instructions)
    train_check, test_check = split_train_test(check_instructions)
    train_answer, test_answer = split_train_test(answer_instructions)

    save_json(train_qa_gen, "train_qa_gen.json")
    save_json(test_qa_gen, "test_qa_gen.json")
    save_json(train_quality, "train_quality.json")
    save_json(test_quality, "test_quality.json")
    save_json(train_check, "train_check.json")
    save_json(test_check, "test_check.json")
    save_json(train_answer, "train_answer.json")
    save_json(test_answer, "test_answer.json")
    

