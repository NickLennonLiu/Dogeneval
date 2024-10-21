"""
将模型输出的文本解析为json格式
"""

import json
from ast import literal_eval
import demjson
import ast
import re

from loguru import logger
logger.add("logs/parser.log", rotation="10 MB")

def line_txt_to_json(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    data = []
    for line in lines:
        if line.startswith('```'):
            line = line.replace('```json', '').replace('```', '')
        
        line = line.replace("\\n", "\n").strip()
        line = line.replace('"{', '{').replace('}"', '}').replace('\\"', '"')
        
        print(line)
        ast.literal_eval(line)
        json.loads(line)
    return data

# 使用正则表达式匹配键和值中的未转义换行符
def escape_newlines_in_json_string(json_str):
    # 匹配键值对中的值部分，并替换其中的未转义换行符
    def replace_newlines(match):
        key, value = match.groups()
        # 替换值中的未转义换行符
        escaped_value = value.replace('\n', '\\n')
        return f'"{key}": "{escaped_value}"'

    # 正则表达式匹配：捕获键和值，特别注意捕获键值中的换行符
    pattern = r'"([^"]*)":\s*"([^"]*?)"'
    escaped_json_str = re.sub(pattern, replace_newlines, json_str)

    return escaped_json_str

def remove_json_markdown(text):
    if text.startswith("```json"):
        text = text[7:]
    if text.endswith("```"):
        text = text[:-3]
    return text

def try_parse_json(text, return_text_if_failed=False):
    original_text = text
    text = escape_newlines_in_json_string(text)
    text = remove_json_markdown(text)
    # print(text)
    try:
        return json.loads(text)
    except json.JSONDecodeError as err:
        logger.warning(err)
        try:
            return literal_eval(text)
        except Exception as err:
            logger.warning(err)
            try:
                return demjson.decode(text)
            except Exception as err:
                logger.warning(err)
                logger.warning(text)
                return None if not return_text_if_failed else original_text
            


if __name__ == "__main__":
    # test_string = """{"param_question": "参数：PROXYSW=ENABLE,RECOVERY=1", "answer": "START\nSET GWPROXYFUNC:PROXYSW=ENABLE,RECOVERY=1;\nEND"}"""
    test_string = """{\n    "error": "给定的语料内容无法直接转换为所需的问题和答案格式，因为缺少具体的参数值来填充模板中的参数问题部分。"\n}"""
    print(test_string)
    print(try_parse_json(test_string))