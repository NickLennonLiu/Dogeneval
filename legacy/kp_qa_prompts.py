import json

Q2_PROMPT = """你是核心网运维工程师，你需要参考给定的题目模板，利用提供的知识点内容，生成一个符合模板或类似模板格式的题目。

问题示例如下：
====================
{question_example}
====================

你需要生成的问题的模板如下：
====================
{question_template}
====================

其中{{}}代表需要填充的参数。

生成问题的知识点如下：
====================
{context}
====================

请你判断上述语料内容能否生成所需问题以及答案。如果可以，返回一个json，字段包括模板中所需的字段，以及answer字段和explanation字段，answer字段是题目的答案，explanation字段是题目的解析，解释为什么得到这个答案。你生成的问题和答案中的术语需要与给定的语料内容匹配，不能生造说法。如果无法生成，返回一个json，字段为error，内容为无法生成的原因。

参考格式如下：
====================
{json_example}
====================

你返回的内容开头不能是```json，直接返回json内容即可。
"""

Q2_PROMPT_ZEROSHOT = """你是核心网运维工程师，你需要参考给定的题目模板，利用提供的知识点内容，生成一个符合模板或类似模板格式的题目。

你需要生成的题目的模板如下：
====================
{question_template}
====================

其中{{}}代表需要填充的参数。

生成问题的知识点如下：
====================
{context}
====================

请你尽可能利用上述知识点进行给定模板的题目生成，返回一个json，字段包括模板中所需的字段，以及answer字段和explanation字段，answer字段是题目的答案，explanation字段是题目的解析，解释为什么得到这个答案。你生成的问题和答案中的术语需要与给定的语料内容匹配，不能生造说法。如果无法生成，返回一个json，字段为error，内容为无法生成的原因。

参考格式如下：
====================
{json_example}
====================

你返回的内容开头不能是```json，直接返回json内容即可。
"""

def format_question_example(question, answer):
    """
    构建 生成Q2 Prompt 中的题目示例
    """
    return f"""问题：
{question}
====================
答案：
{answer}"""

def format_json_example(fields):
    """
    构建 生成Q2 Prompt 中的json示例
    """
    return f"""{{
    {",    ".join([f'"{field["name"]}": "{field["description"]}"' for field in fields])},
    "answer": "answer",
    "explanation": "explanation"
}}"""

def format_kp_context(kp_title, kp_content):
    """
    构建 生成Q2 Prompt 中的知识点内容
    """
    return f"""知识点标题：
{kp_title}
====================
知识点内容：
{kp_content}"""


def format_q2_prompt(template_data, kp_title, kp_content):
    """
    构建 生成Q2 Prompt
    """
    return Q2_PROMPT.format(**{
        "question_example":format_question_example(template_data["examples"][0]["Question"], template_data["examples"][0]["Answer"]),
        "question_template": template_data['template'],
        "context": format_kp_context(kp_title, kp_content),
        "json_example": format_json_example(template_data["fields"]),
    })


def format_q2_prompt_zeroshot(template_data, kp_title, kp_content):
    """
    构建 生成Q2 Zeroshot Prompt
    """
    return Q2_PROMPT_ZEROSHOT.format(**{
        # "ability_description": template_data["description"],
        "question_template": template_data['template'],
        "context": format_kp_context(kp_title, kp_content),
        "json_example": format_json_example(template_data["fields"]),
    })



def form_check_prompt(a1, a2):
    """
    给定两个文本内容，构建 判断两个文本内容是否匹配 的Prompt
    """
    prompt = f"""你是一名华为的运维工程师，请你判断以下两个文本内容在内容上是否匹配，是否是参考材料和正确答案之间的关系：

====================文本1====================
{a1}
============================================ 

====================文本2====================
{a2}
============================================

请你返回一个json，表示两个文本内容的匹配情况，字段包括match字段和reason字段，match字段表示两个文本内容是否匹配，值为true或false；reason字段表示匹配情况的原因，如果match为true，reason字段应为两个文本之间的对应关系，如果match为false，reason字段应为不匹配的原因。

参考格式如下：
{{
    "match": true,
    "reason": "两个文本内容匹配，文本1中的xxx对应文本2中的yyy..."
}}
{{
    "match": false,
    "reason": "两个文本内容不匹配，原因是...(例如：文本2中的xxx在文本1中没有对应项)"
}}

你返回的内容开头不能是```json，直接返回json内容即可。
"""
    return prompt