"""
将实时生成的结果保存到远程的mongodb中，方便查看
"""

import pymongo
from pymongo import MongoClient
import pandas as pd


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
    df.to_excel(file_path, index=False)


if __name__ == "__main__":
    export_collection_to_excel("QA_GEN-10281814", "qa_gen_10281814.xlsx")
