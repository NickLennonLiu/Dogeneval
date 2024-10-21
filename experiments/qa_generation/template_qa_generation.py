from dogeneval.template.template_prompt import format_qa_generation_prompt
from dogeneval.template.abilities import ability_templates
from dogeneval.utils.llm.llms import get_openai_model
from dogeneval.qa_vector.db import load_db
from dogeneval.utils.load_document import get_parent_layer, load_documents, get_content
from dogeneval.utils.parser import try_parse_json
import random, os, json, datetime

from tqdm import tqdm
from loguru import logger
logger.add("template_qa_generation.log", rotation="10 MB")

def _get_similar_docs_parent_folders(vector_db, data, topk=20):
    similar_results = vector_db.similarity_search(data['examples'][0]['question'], topk=topk)
    similar_docs = [doc.metadata['source'] for doc in similar_results]

    parent_folders = set()
    for doc in similar_docs:
        parent = get_parent_layer(doc, upper_layer=9, target_range=(50, 10000))
        parent_folders.add(parent)
    return parent_folders

def get_similar_docs(vector_db, data, topk=10, sample_size=100):
    parent_folders = _get_similar_docs_parent_folders(vector_db, data, topk=topk)

    docs = sum([load_documents(parent) for parent in parent_folders], [])
    logger.info(f"Found {len(docs)} related docs in {len(parent_folders)} parent folders.")

    # 如果docs数量太多，对docs进行采样
    if len(docs) > sample_size:
        docs = random.sample(docs, sample_size)
    docs = get_content(docs)

    return docs

def main(output_dir):
    version_str = datetime.datetime.now().strftime("%m%d%H%M")

    vector_db = load_db("/home/junetheriver/codes/qa_generation/huawei/qa_vector/UNC")
    logger.info("Vector DB loaded.")

    llm = get_openai_model()
    result = llm.chat("Hello, this is an api test. Please reply me that 'API test is successful'.")
    logger.info(result)

    sample_size = 1000

    for ability_data in ability_templates:
        logger.info(f"Processing ability: {ability_data['name']}")

        os.makedirs(os.path.join(output_dir, ability_data['name']), exist_ok=True)

        docs = get_similar_docs(vector_db, ability_data, sample_size=sample_size)

        qa = []
        logger.info("Start generating QA pairs.")
        for doc in tqdm(docs):
            content = doc['content']

            prompt = format_qa_generation_prompt(ability_data, content)

            try:
                result = llm.chat(prompt)
            except KeyboardInterrupt:
                raise
            except:
                continue

            json_result = try_parse_json(result)

            # if json_result and 'error' not in json_result:
            if json_result:
                full_json = {
                    'question': json_result,
                    'path': doc['path'],
                    'filename': doc['filename'],
                    'template': ability_data['template'],
                    'version': version_str,
                    'examples': ability_data['examples']
                }
                qa.append(full_json)

                with open(os.path.join(output_dir, ability_data['name'], f"tmp-{version_str}.jsonl"), 'at+') as f:
                    f.write(json.dumps(full_json, ensure_ascii=False))
                    f.write('\n')
        
        with open(os.path.join(output_dir, ability_data['name'], f"qa-{version_str}.json"), 'w') as f:
            json.dump(qa, f, ensure_ascii=False, indent=4)
        


if __name__ == "__main__":
    main("/home/junetheriver/codes/qa_generation/huawei/data/generated_qa")
    
    # similar_docs = _get_similar_docs_parent_folders(load_db("/home/junetheriver/codes/qa_generation/huawei/qa_vector/UNC"), ability_templates[0])
    # for path in similar_docs:
    #     print(path.replace("/home/junetheriver/datasets/huawei/processed/", ""))

    # llm = get_openai_model()

    # with open("demo/add_ngpra.txt") as f:
    #     context = f.read()

    # from codes.qa_generation.huawei.template.abilities.code_generation import data as code_data
    # prompt = format_qa_generation_prompt(code_data, context)

    # print(prompt)

    # result = llm.generate(prompt)
    # print(result)
