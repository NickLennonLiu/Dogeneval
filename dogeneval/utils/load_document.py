import argparse
import pandas
import os
import glob
from dogeneval.utils.token_utils import get_qwen_token_num
import unittest
import pickle
from loguru import logger


def load_word_ls(path = 'data/word_ls.pkl'):
    with open(path, 'rb') as f:
        word_ls, metadata_ls = pickle.load(f)
    return word_ls, metadata_ls

def load_documents(folder, root_folder='/home/junetheriver/datasets/huawei/processed'):
    if os.path.isfile(folder):
        return [{
            'filename': folder,
            'path': folder.replace(root_folder+"/", "")
        }]

    # 用glob遍历root_folder下所有子文件夹中的txt文件
    files = glob.glob(os.path.join(folder, '**/*.txt'), recursive=True)
    # for file in files:
    #     print(file.replace(root_folder+"/", ""))
    files = [
        {
            'filename': file,
            'path': file.replace(root_folder, "")
        } for file in files]
    return files

def load_documents_and_contents(folder, root_folder='/home/junetheriver/datasets/huawei/processed'):
    files = load_documents(folder, root_folder)
    files = get_content(files)
    return files

def default_merge_method(files):
    merged_text = ""
    for file in files:
        merged_text += file['content'] + '\n\n'
    return merged_text

def get_path_token_size(path: str, merge_method=default_merge_method):
    if os.path.isfile(path):
        return get_qwen_token_num(open(path, 'r').read())
    files = load_documents(path)
    files = get_content(files)
    merged_text = merge_method(files)
    token_num = get_qwen_token_num(merged_text)
    return token_num

def try_larger_folder(path: str, max_token_num: int, merge_method=default_merge_method):
    """
    从一个目录出发，尽可能包含多文件，直到文件内容token数超过limit
    """
    token_num = get_path_token_size(path, merge_method)
    logger.info(f"Current path: {path}, token num: {token_num}")
    while token_num < max_token_num:
        logger.info(f"Current path: {path}, token num: {token_num} < {max_token_num}")
        last_path = path
        path = os.path.dirname(path)
        token_num = get_path_token_size(path, merge_method)
    logger.info(f"Current path: {path}, token num: {token_num} >= {max_token_num}")
    return last_path


def iter_folder(path: str, max_token_num: int, iter_func, merge_method=default_merge_method):
    if os.path.isfile(path):
        return iter_func(path)

    files = load_documents(path)
    files = get_content(files)
    merged_text = merge_method(files)
    token_num = get_qwen_token_num(merged_text)
    if token_num < max_token_num:
        return iter_func(path)
    else:
        # logger.debug(f"Current path: {path}, token num: {token_num} >= {max_token_num}")
        for sub_path in os.listdir(path):
            sub_path = os.path.join(path, sub_path)
            iter_folder(sub_path, max_token_num, iter_func, merge_method)


def get_parent_layer(path: str, upper_layer: int = 9, target_range: tuple[int, int] = (100, 1000)):
    """
    给定一个路径，往上找，直到找到一个目录，这个目录下的文件数在target_range范围内，或者到达upper_layer层
    """
    layers = len(path.split('/'))
    while layers > upper_layer:
        layers = len(path.split('/'))
        # 计算这个目录从根节点开始，往下有几层
        path = os.path.dirname(path)
        files = load_documents(path)
        if len(files) >= target_range[0] and len(files) <= target_range[1]:
            return path
    return path

def get_content(files):
    for file in files:
        file['content'] = open(file['filename'], 'r').read()
    return files

def load_documents_content(folder, root_folder='/home/junetheriver/datasets/huawei/processed'):
    files = load_documents(folder, root_folder)
    files = get_content(files)
    return files


class TestLoadDocuments(unittest.TestCase):
    def test_load_documents(self):
        root_folder = '/home/junetheriver/datasets/huawei/processed/UNC_20.9.5'
        files = load_documents(root_folder)
        files = get_content(files)
        print(files[0])
    
    def test_get_parent_layer(self):
        path = '/home/junetheriver/datasets/huawei/processed/UNC_20.9.5/OM参考/命令/UNC工程命令/DSP DBSTATS参数补充说明/系统视图/zh-cn_topic_0000001304906153.txt'
        upper_layer = 1
        try_upper = 1
        target_range = (20, 100)
        parent = get_parent_layer(path, upper_layer, try_upper, target_range=target_range)
        print(parent)


if __name__ == "__main__":
    # root_folder = '/home/junetheriver/datasets/huawei/processed/UNC_20.9.5'
    # load_documents(root_folder)

    path = '/home/junetheriver/codes/qa_generation/huawei/data/UNC_20.9.5/'
    # upper_layer = 1
    # target_range = (10000, 100000)
    # parent = get_parent_layer(path, upper_layer, target_range=target_range)

    # try_larger_folder(path, 8000)
    iter_folder(path, 2000, print)