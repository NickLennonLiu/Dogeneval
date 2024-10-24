from dogeneval.utils.mongodb import load_results

import pandas as pd
import numpy as np

import json, re, os, sys, time, datetime, random

import matplotlib.pyplot as plt

def mongo_obj_to_dict(obj_list):
    return [obj.to_dict() for obj in obj_list]

def export_and_merge_collections(collection_names, output_name):
    results = []
    for collection_name in collection_names:
        results.extend(load_results(collection_name))
    print(len(results))

    ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
    for result in results:
        result["match_reason"] = ILLEGAL_CHARACTERS_RE.sub('', result["match_reason"])

    # results = mongo_obj_to_dict(results)
    # print(results[0].to_dict())

    df = pd.DataFrame(results)
    df.to_excel(f"{output_name}.xlsx", index=False)
    return results

if __name__ == "__main__":
    collection_names = ["QA_GEN-10232248", "QA_GEN-10240840"]
    export_and_merge_collections(collection_names, "QA_GEN_1024")