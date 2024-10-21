"""
将实时生成的结果保存到远程的mongodb中，方便查看
"""

import pymongo
from pymongo import MongoClient



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