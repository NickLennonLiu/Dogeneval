PROMPT = """
你是一名华为的运维工程师，你需要根据给定的产品文档内容和题目模板，生成一套问题和答案。

问题示例如下：
====================
{question_example}
====================

你需要生成的问题的模板如下：
====================
{question_template}
====================

其中{{}}代表需要填充的参数。

生成问题的语料如下：
====================
{context}
====================

请你判断上述语料内容能否生成所需问题以及答案。如果可以，返回一个json，字段包括模板中所需的字段，以及answer字段和explanation字段，answer字段是题目的答案，explanation字段是题目的解析，解释为什么得到这个答案。你生成的问题和答案中的术语需要与给定的语料内容匹配，不能生造说法。

参考格式如下：
====================
{json_example}
====================

如果无法生成，返回一个json，字段为error，内容为无法生成的原因。

你返回的内容开头不能是```json，直接返回json内容即可。
"""

def format_question_example(question, answer):
    return f"""问题：
{question}
====================
答案：
{answer}"""

def format_json_example(fields):
    return f"""{{
    {",    ".join([f'"{field["name"]}": "{field["description"]}"' for field in fields])},
    "answer": "answer",
    "explanation": "explanation"
}}"""

def format_qa_generation_prompt(template_data, context):
    return PROMPT.format(**{
        "question_example":format_question_example(template_data["examples"][0]["question"], template_data["examples"][0]["answer"]),
        "question_template": template_data['template'],
        "context": context,
        "json_example": format_json_example(template_data["fields"]),
    })


if __name__ == "__main__":
    from .abilities.code_generation import data as code_data
    result = PROMPT.format(**{
        "question_example":format_question_example(code_data["examples"][0]["question"], code_data["examples"][0]["answer"]),
        "question_template": code_data['template'],
        "context": "Some context",
        "json_example": format_json_example(code_data["fields"]),
    })
    print(result)