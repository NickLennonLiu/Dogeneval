SCENE_QA_PRMOPT = """你是华为核心网运维工程师，请你根据下面的知识点和任务模板，构造一个业务场景，然后生成对应的任务参数。

知识点：
{context}

任务模板：
{task_template}

请返回一个json，字段包括scene和task_params，scene是构造的业务场景，task_params是构造的业务场景对应的任务参数。

参考格式如下：
====================
{json_example}
====================
"""

def format_scene_qa_prompt(context, task_template, json_example):
    return SCENE_QA_PRMOPT.format(context=context, task_template=task_template, json_example=json_example)