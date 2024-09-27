from load_document import get_parent_layer, load_documents, get_content
from loguru import logger
import random

def _get_similar_docs_parent_folders(vector_db, data, topk=20):
    similar_results = vector_db.similarity_search(data, topk=topk)
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