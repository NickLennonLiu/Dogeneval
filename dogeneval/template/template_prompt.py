Q2_NO_CHECK_FEWSHOT_PROMPT = """你是一名运维专家，你需要参考给定的题目模板，利用提供的知识点内容，生成一个符合模板或类似模板格式的题目。

下面是示例题目，格式可能不完全与模板要求一致，仅供参考：
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

在生成题目时，你需要考虑如下约束：
{constraints}

返回一个json，字段包括模板中所需的字段，以及answer字段和explanation字段，answer字段是题目的答案，explanation字段是题目的解析，解释为什么得到这个答案。你生成的问题和答案中的术语需要与给定的语料内容匹配，不能生造说法。

参考格式如下：
====================
{json_example}
====================

你返回的内容开头不能是```json，直接返回json内容即可。
"""

Q2_NO_CHECK_ZEROSHOT_PROMPT = """你是一名运维专家，你需要参考给定的题目模板，利用提供的知识点内容，生成一个符合模板或类似模板格式的题目。

你需要生成的问题的模板如下：
====================
{question_template}
====================

其中{{}}代表需要填充的参数。

生成问题的知识点如下：
====================
{context}
====================

在生成题目时，你需要考虑如下约束：
{constraints}

返回一个json，字段包括模板中所需的字段，以及answer字段和explanation字段，answer字段是题目的答案，explanation字段是题目的解析，解释为什么得到这个答案。你生成的问题和答案中的术语需要与给定的语料内容匹配，不能生造说法。

参考格式如下：
====================
{json_example}
====================

你返回的内容开头不能是```json，直接返回json内容即可。
"""

Q2_NO_CHECK_FEWSHOT_WITH_SCENE_PROMPT = \
"""你是一名运维专家，你需要参考给定的题目模板，利用提供的知识点内容，生成一个符合模板或类似模板格式的题目。

下面是示例题目，格式可能不完全与模板要求一致，仅供参考：
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

在生成问题时，你需要基于知识点内容构造一个业务场景或运维场景，然后基于该场景去生成各个字段。

在生成题目时，你需要考虑如下约束：
{constraints}

返回一个json，字段包括模板中所需的字段，以及answer字段和explanation字段，answer字段是题目的答案，explanation字段是题目的解析，解释为什么得到这个答案。你生成的问题和答案中的术语需要与给定的语料内容匹配，不能生造说法。

参考格式如下：
====================
{json_example}
====================

你返回的内容开头不能是```json，直接返回json内容即可。
"""

Q2_NO_CHECK_ZEROSHOT_WITH_SCENE_PROMPT = """你是一名运维专家，你需要参考给定的题目模板，利用提供的知识点内容，生成一个符合模板或类似模板格式的题目。

你需要生成的问题的模板如下：
====================
{question_template}
====================

其中{{}}代表需要填充的参数。

生成问题的知识点如下：
====================
{context}
====================

在生成问题时，你需要基于知识点内容构造一个业务场景或运维场景，然后基于该场景去生成各个字段。

在生成题目时，你需要考虑如下约束：
{constraints}

返回一个json，字段包括模板中所需的字段，以及answer字段和explanation字段，answer字段是题目的答案，explanation字段是题目的解析，解释为什么得到这个答案。你生成的问题和答案中的术语需要与给定的语料内容匹配，不能生造说法。

参考格式如下：
====================
{json_example}
====================

你返回的内容开头不能是```json，直接返回json内容即可。
"""

def format_constraints(constraints):
    """
    构建 生成Q2 Prompt 中的约束
    """
    return '\n'.join([f"{i+1}. {constraint}" for i, constraint in enumerate(constraints)])

def format_kp_context(kp_title, kp_description, kp_content):
    """
    构建 生成Q2 Prompt 中的知识点内容
    """
    return f"""知识点标题：
{kp_title}
====================
知识点描述：
{kp_description}
====================
知识点内容：
{kp_content}"""

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


def format_qa_generation_prompt(template, constraints, kp, is_zeroshot: bool, require_scene: bool, example=None, lang="zh"):
    """
    构建 生成Q2 Prompt
    """

    json_example = format_json_example(template["fields"])
    context = format_kp_context(kp["title"], kp["description"], kp["content"])
    constraints = format_constraints(constraints)

    if is_zeroshot:
        if require_scene:
            return Q2_NO_CHECK_ZEROSHOT_WITH_SCENE_PROMPT.format(**{
                "question_template": template['template'],
                "context": context,
                "constraints": constraints,
                "json_example": json_example,
            })
        else:
            return Q2_NO_CHECK_ZEROSHOT_PROMPT.format(**{
                "question_template": template['template'],
                "context": context,
                "constraints": constraints,
                "json_example": json_example,
            })
    else:
        example_prompt = format_question_example(example["Question"], example["Answer"])
        if require_scene:
            return Q2_NO_CHECK_FEWSHOT_WITH_SCENE_PROMPT.format(**{
                "question_example": example_prompt,
                "question_template": template['template'],
                "context": context,
                "constraints": constraints,
                "json_example": json_example,
            })
        else:
            return Q2_NO_CHECK_FEWSHOT_PROMPT.format(**{
                "question_example": example_prompt,
                "question_template": template['template'],
                "context": context,
                "constraints": constraints,
                "json_example": json_example,
            })
