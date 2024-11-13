from dogeneval.knowledge_extraction.prompt import form_knowledge_point_extract_prompt

from dogeneval.utils.llm.llms import get_openai_model, get_azure_model
from dogeneval.utils.parser import try_parse_json
from dogeneval.utils.load_document import get_content
from dogeneval.utils.mongodb import save_result
from dogeneval.template.ktasks import load_ktasks
from loguru import logger
from tqdm import tqdm
import datetime
import os, json, re
from dogeneval.qa_vector.similarity_search import get_similar_docs
from dogeneval.qa_vector.db import load_db
import pandas as pd

import argparse


def knowledge_extraction(output_dir):
    output_dir = os.path.join(output_dir, "knowledge_points")
    os.makedirs(output_dir, exist_ok=True)

    version_str = datetime.datetime.now().strftime("%m%d%H%M")

    save_knowledge_points = []

    vector_db = load_db("/home/junetheriver/codes/qa_generation/huawei/qa_vector/UNC")
    logger.info("Vector DB loaded.")

    llm = get_openai_model()
    logger.info(llm.chat("测试API，请回复API Test Success"))

    example_file = "/home/junetheriver/codes/qa_generation/huawei/prompts/examples.json"
    with open(example_file, 'r') as f:
        examples = json.load(f)

    for cat, examples in tqdm(examples.items(), desc="Processing categories"):
        for example in tqdm(examples, desc="Processing examples"):
            question_answer = example['Question'] + '\n' + example['Answer']

            docs = get_similar_docs(vector_db, question_answer, topk=10, sample_size=2)

            for doc in tqdm(docs, desc="Processing documents"):
                knowledge_extract_prompt = form_knowledge_point_extract_prompt(doc)

                response = llm.chat(knowledge_extract_prompt)

                parsed_json = try_parse_json(response)

                try:
                    knowledge_points = parsed_json['knowledge_points']

                    for knowledge_point in knowledge_points:
                        knowledge_point['possible_category'] = cat

                    save_knowledge_points.extend(knowledge_points)
                except:
                    logger.error(f"Error parsing json: {response}")
        
    with open(os.path.join(output_dir, f"knowledge_points-{version_str}.json"), 'w') as f:
        json.dump(save_knowledge_points, f, ensure_ascii=False, indent=4)

    df = pd.DataFrame(save_knowledge_points)
    df.rename(columns={
        'title': '标题',
        'type': '类型',
        'description': '描述',
        'content': '内容',
        'path': '路径',
        'possible_category': '可能的题目分类（该文档从该分类中通过相似度搜索得到，不代表一定属于该分类)'
    }, inplace=True)
    df.drop(columns=['id'], inplace=True)

    df.to_excel(os.path.join(output_dir, f"knowledge_points-{version_str}.xlsx"))

def load_docs(input_dir):
    docs = [{'filename': os.path.join(input_dir, file), 'path': file.replace('.txt', '')} for file in os.listdir(input_dir)]
    docs = get_content(docs)
    return docs

def load_docs_from_json(input_json):
    with open(input_json, 'r') as f:
        data = json.load(f)
    return data

def knowledge_extraction(docs, name, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    version_str = datetime.datetime.now().strftime("%m%d%H%M")

    save_knowledge_points = []

    llm = get_azure_model()
    logger.info(llm.chat("测试API，请回复API Test Success"))

    ktasks, require_scene_ktasks = load_ktasks()

    for doc in tqdm(docs, desc="Processing documents"):
        knowledge_extract_prompt = form_knowledge_point_extract_prompt(doc)
        response = llm.chat_json(knowledge_extract_prompt)

        if response:
            kps = response.get('knowledge_points', [])
        else:
            kps = []
        for kp in kps:
            save_result(kp, collection_name=f'{name}-knowledge_points-{version_str}')

        save_knowledge_points.extend(kps)
    
    df = pd.DataFrame(save_knowledge_points)
    df.rename(columns={
        'title': '标题',
        'type': '类型',
        'description': '描述',
        'content': '内容',
        'path': '路径',
    }, inplace=True)

    df.to_excel(os.path.join(output_dir, f"{name}-knowledge_points-{version_str}.xlsx"))

if __name__ == "__main__":
    # input_json = "/home/junetheriver/codes/qa_generation/huawei/data/sampled_pages_200_txt.json"
    # output_dir = "/home/junetheriver/codes/qa_generation/huawei/data"

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json", type=str, required=True)
    parser.add_argument("--output_dir", type=str, required=True)
    parser.add_argument("--name", type=str, required=True)
    args = parser.parse_args()

    input_json = args.input_json
    output_dir = args.output_dir
    name = args.name
    
    docs = load_docs_from_json(input_json)
    logger.info(f"docs: {len(docs)}")
    knowledge_extraction(docs, name, output_dir)
