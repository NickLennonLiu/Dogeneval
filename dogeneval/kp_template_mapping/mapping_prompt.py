MAPPING_PROMPT_ZH = """你是一名运维专家，你的任务是判断文档中的一个知识点能否用于生成一系列题目模板中的若干类题目。

<题目模板列表>
{template_list}
</题目模板列表>

{kp_format}

返回一个json，表示你对上述知识点的内容能否生成上述{template_cnt}个模板的题目的判断，不要考虑该知识点是否有必要生成对应任务，要从生成题目的内容是否有足够好的质量和准确性进行考虑。格式如下：

{{
    "(模板1名称)": {{
        "choose": true/false,
        "reason": "..."
    }}, ...
}}

你返回的内容开头不能是```json，直接返回json内容即可。
"""

# TODO: 更新英文版
MAPPING_PROMPT_EN = """You are an Operations expert. Your task is to determine whether a knowledge point from the documentation can be used to generate several types of questions based on a given list of templates.

<Question Template List>
{template_list}
</Question Template List>

{kp_format}

Return a JSON object indicating your judgment on whether the content of the above knowledge point can generate questions for the {template_cnt} templates listed. Do not consider whether it is necessary to generate tasks for this knowledge point; focus solely on whether the content can support generating questions with sufficient quality and accuracy. The format is as follows:

{{
    "(Template 1 Name)": {{
        "choose": true/false,
        "reason": "..."
    }}, ...
}}

Do not prepend the output with ```json. Return the JSON content directly.
"""