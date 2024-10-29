import os
import xml
import shutil
import argparse
import random
from dogeneval.doc_parsing.html2txt import parse_html_content
import json
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from functools import partial

from loguru import logger

def dfs_xml(root, resource_dir, cur_path,
            layer_func: callable, node_func: callable, 
            layer_json, errors):
    """
    layer_func: 处理层级信息的函数
    node_func: 处理节点信息的函数
    layer_json: 层级信息
    """
    if len(root) == 0:  # 根节点
        node_func(root, cur_path)

        layer_json[root.get('txt')] = root.get('url')

        
    else:           # 非根节点
        layer_json[root.get('txt')] = {}
        
        layer_func(root, cur_path)

        for child in root:
            path = cur_path + '/' + child.get('txt', '') if child.get('txt') else cur_path
            dfs_xml(child, resource_dir, path,
                    layer_func, node_func, 
                    layer_json[root.get('txt')], errors)


def parse_hdx_unzipped(resource_dir, layer_func: callable, node_func: callable):
    navi_xml = os.path.join(resource_dir, "navi.xml")
    with open(navi_xml, 'r') as f:
        data = f.read()
        root = ET.fromstring(data)

    layer_json = {}
    errors = []
    dfs_xml(root, resource_dir, '', layer_func, node_func, layer_json, errors)
    

def print_layer_info(root: Element, cur_path: str):
    logger.info(f"layer: {root.attrib}")
    return

def print_node_info(root: Element, cur_path: str):
    logger.info(f"node: {root.attrib}")
    return

def sample_pages(root: Element, cur_path: str, resource_dir: str, output_list: list, sample_num: int = 1):
    pages = []
    for child in root:
        if not len(child):
            pages.append(child)
    if not len(pages):
        return
    sample_pages = random.sample(pages, sample_num)
    output_list.extend([
        {"path": cur_path, "page": page} for page in sample_pages
    ])

def save_pages(pages: list, resource_dir: str, output_dir: str):
    for page in pages:
        path = page["path"]
        # 去掉path开头的/
        path = path.lstrip("/")
        page = page["page"]
        url = page.get("url")
        # 创建output_dir/path
        output_path = os.path.join(output_dir, path)
        os.makedirs(output_path, exist_ok=True)
        # 保存page
        origin_page = os.path.join(resource_dir, url)
        # 检查origin_page是否存在，如果不存在，尝试url lower后检查
        if not os.path.exists(origin_page):
            origin_page = os.path.join(resource_dir, url.lower())

        if not os.path.exists(origin_page):
            raise FileNotFoundError(f"page {url} not found")

        ext = origin_page.split(".")[-1]
        shutil.copy(origin_page, output_path)

def parse_html_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    for doc in data:
        content = doc["content"]
        content = parse_html_content(content)
        doc["content"] = content
        doc["path"] = doc["path"].replace('/home/junetheriver/codes/qa_generation/huawei/data/sampled_pages/', '')
    return data

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--resource_dir', type=str, default='/home/junetheriver/codes/qa_generation/huawei/data/unc_html/resources')

    # args = parser.parse_args()
    # resource_dir = args.resource_dir

    # sampled_pages = []

    # layer_func = partial(sample_pages, resource_dir=resource_dir, output_list=sampled_pages)
    # node_func = lambda x, y: None
    # parse_hdx_unzipped(resource_dir, layer_func, node_func)

    # logger.info(f"sampled pages: {len(sampled_pages)}")

    # save_pages(sampled_pages, resource_dir, "/home/junetheriver/codes/qa_generation/huawei/data/sampled_pages")

    data = parse_html_json("/home/junetheriver/codes/qa_generation/huawei/data/sampled_pages_200.json")
    with open("/home/junetheriver/codes/qa_generation/huawei/data/sampled_pages_200_txt.json", 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
