"""
给定一个字符串或字典，将其翻译成目标语言
"""

import json
from googletrans import Translator

translator = Translator(service_urls=['translate.google.cn'])

def translate_prompt(prompt, origin_lang, target_lang):
    pass

def translate_json(json_data, origin_lang, target_lang):
    json_txt = json.dumps(json_data, ensure_ascii=False)
    print(json_txt)
    translated = translator.translate(json_txt, src=origin_lang, dest=target_lang)
    return json.loads(translated.text)

if __name__ == "__main__":
    test_json = {
        "task_name": "MultipleChoice",
        "description": "该题型要求大模型根据题目和选项，选择正确的答案",
        "system_prompt": "你是核心网运维工程师，请根据题目和选项，选择正确的答案。",
        "template": "{question}\nA: {A}\nB: {B}\nC: {C}\nD: {D}",
        "fields": [
            {
                "name": "question",
                "description": "题目"
            },
            {
                "name": "A",
                "description": "选项A"
            },
            {
                "name": "B",
                "description": "选项B"
            },
            {
                "name": "C",
                "description": "选项C"
            },
            {
                "name": "D",
                "description": "选项D"
            }
        ],
        "output_requirement": "只输出A、B、C、D中的一个字母"
    }
    translated_json = translate_json(test_json, "zh-cn", "en")
    print(translated_json)