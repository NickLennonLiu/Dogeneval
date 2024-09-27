from .prompt import form_knowledge_point_extract_prompt

from utils.llm.llms import get_openai_model
from utils.parser import try_parse_json
from huawei.dogeneval.utils.load_document import load_documents, get_content
from loguru import logger
from tqdm import tqdm
import datetime
import os, json, re
from qa_vector.similarity_search import get_similar_docs
from qa_vector.db import load_db
import pandas as pd


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

if __name__ == "__main__":
    output_dir = "/home/junetheriver/codes/qa_generation/huawei/data"
    knowledge_extraction(output_dir=output_dir)
