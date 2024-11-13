"""
将实时生成的结果保存到远程的mongodb中，方便查看
"""

import pymongo
from pymongo import MongoClient
import pandas as pd
import re


def load_mongodb_client():
    mongo_url = "mongodb://admin:opseval@166.111.68.22:57018/"
    client = pymongo.MongoClient(mongo_url)
    return client

MONGODB_CLIENT = load_mongodb_client().DogenEval

def save_result(result, collection_name):
    # check if the collection exists
    if collection_name not in MONGODB_CLIENT.list_collection_names():
        MONGODB_CLIENT.create_collection(collection_name)

    result = MONGODB_CLIENT[collection_name].insert_one(result)
    return result

def load_results(collection_name):
    cursor = MONGODB_CLIENT[collection_name].find()
    documents = []
    for document in cursor:
        documents.append(document)

    return documents

def load_results_as_df(collection_name):
    documents = load_results(collection_name)
    df = pd.DataFrame(documents)
    return df

def export_collection_to_excel(collection_name, file_path):
    df = load_results_as_df(collection_name)
    ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
    # 将df中所有字符串类型的值都进行上面的替换
    df = df.applymap(lambda x: re.sub(ILLEGAL_CHARACTERS_RE, '', x) if isinstance(x, str) else x)

    df.to_excel(file_path, index=False)

def mongo_obj_to_dict(obj_list):
    return [obj.to_dict() for obj in obj_list]

def export_and_merge_collections(collection_names, file_path):
    results = []
    for collection_name in collection_names:
        results.extend(load_results(collection_name))
    print(len(results))

    ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
    # 将df中所有字符串类型的值都进行上面的替换
    df = df.applymap(lambda x: re.sub(ILLEGAL_CHARACTERS_RE, '', x) if isinstance(x, str) else x)

    df = pd.DataFrame(results)
    df.to_excel(file_path, index=False)
    return results


if __name__ == "__main__":
    export_collection_to_excel("emsplus-QA_GEN-11112014", "emsplus-qa_gen_11112014.xlsx")
