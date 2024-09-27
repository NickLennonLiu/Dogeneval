from load_document import load_documents, get_content
from codes.qa_generation.huawei.llm import get_vllm_model, get_qwen_answer
import os
import json
from time import sleep
from loguru import logger
from prompt import get_prompts
from multitasks import multi_process
from ability_analysis.doc_map import load_cat_doc
            


def main(root_dir, output_file):
    # Get documents
    documents = load_documents('/home/junetheriver/datasets/huawei/processed/UNC_20.9.5')
    
    # Optional: sample documents
    documents = documents[:4]
    
    # Get contents
    documents = get_content(documents)

    # Get Prompts
    questions = get_prompts(documents)

    # Multi-process
    multi_process(questions, output_file, num_gpus=4, batch_size=32)


def gen_cat_questions():
    documents = load_documents('/home/junetheriver/datasets/huawei/processed/UNC_20.9.5')
    cat_docs = load_cat_doc(documents)
    
    # sample cat_docs
    sample_cnt = 10
    for cat, docs in cat_docs.items():
        # 随机采样
        import random
        random.shuffle(docs)
        cat_docs[cat] = docs[:sample_cnt]
    
    # Get contents
    for cat, docs in cat_docs.items():
        cat_docs[cat] = get_content(docs)

    # Get Examples
    with open("/home/junetheriver/codes/qa_generation/huawei/prompts/examples.json") as f:
        cat_examples = json.load(f)
    
    # Get Prompts
    cat_questions = {}
    for cat, docs in cat_docs.items():
        cat_questions[cat] = get_prompts(docs, 
                                         doc_name='UNC',
                                         category=cat,
                                         examples=cat_examples[cat]
                                         )
    
    # Save Prompts
    with open("/home/junetheriver/results/huawei/qa_prompt.json", 'w') as f:
        json.dump(cat_questions, f, indent=4, ensure_ascii=False)

    # Generate Questions
    for cat, questions in cat_questions.items():
        output_file = f"/home/junetheriver/results/huawei/{cat}.txt"
        results = multi_process(questions, 
                      output_file, 
                      cat,
                      num_gpus=4, batch_size=32)
        with open(f"/home/junetheriver/results/huawei/{cat}.json", 'w') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    root_dir = '/home/junetheriver/datasets/huawei/processed/UNC_20.9.5'
    output_file = '/home/junetheriver/results/huawei/demo.txt'
    # main(root_dir, output_file)
    gen_cat_questions()