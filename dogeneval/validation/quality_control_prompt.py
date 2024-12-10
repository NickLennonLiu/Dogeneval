def form_quality_control_prompt(template, question_components):
    PROMPT = """您是一位问题生成质量控制专家。您的任务是根据给定的模板评估生成的问题，并确定它是否符合所需的标准。请分析以下问题组成部分并提供您的评估：

模板：
{template}

生成的问题，其中answer字段为答案：
{question_components}

指示：
1. 仔细检查生成问题的每个组成部分。
2. 将生成的组成部分与模板结构进行比较。
3. 检查以下问题：
   - 信息缺失或不完整
   - 内容错误或事实性错误
   - 组成部分之间的不一致
   - 语法或结构问题
   - 模糊或缺乏清晰度

4. 提供详细的问题评估，解决以下几点：
   a. 问题是否符合给定的模板结构？
   b. 是否所有必需的组成部分都存在且完整？
   c. 内容是否准确并与主题相关？
   d. 问题是否构造良好且清晰？
   e. 这些组成部分是否可以组合成一个连贯且适当的问题？

5. 给出您的最终评估。

请以JSON格式提供您的评估结果，格式如下：

{{
    "评估": {{
        "符合模板结构": true/false,
        "组成部分完整": true/false,
        "内容准确性": true/false,
        "问题构造": true/false,
        "组合适当性": true/false
    }},
    "最终评估": "批准"/"建议修改"/"拒绝",
    "修改建议": "如果需要修改，在这里提供具体建议",
    "拒绝原因": "如果拒绝，在这里解释原因"
}}

示例输出：
{{
    "评估": {{
        "符合模板结构": true,
        "组成部分完整": true,
        "内容准确性": true,
        "问题构造": true,
        "组合适当性": true
    }},
    "最终评估": "批准",
    "修改建议": "",
    "拒绝原因": ""
}}

请根据上述指示提供您的评估结果。
"""
    return PROMPT.format(template=template, question_components=question_components)


def form_check_prompt(kp, question, response):
    prompt = f"""你是一名核心网运维工程师，请你根据给定的知识库内容，判断模型回复是否为给定题目的正确答案。

====================知识库内容====================
知识点描述：{kp['description']}
知识点内容：
{kp['content']}
=============================================

====================题目====================
{question}
=============================================

====================模型回复====================
{response}
=============================================

请你返回一个json，字段包括match字段和reason字段，match字段表示模型回复是否为给定题目的正确答案，值为true或false；如果match为true，reason字段应为模型回复与给定题目和知识点之间的对应关系，如果match为false，reason字段应为不正确的原因。如果模型作答中表示“无法回答”，则match字段应为false，reason字段为模型作答中的解释。

参考格式如下：
{{
    "match": true,
    "reason": "模型回复与给定题目和知识点之间的对应关系"
}}
{{
    "match": false,
    "reason": "不正确的原因"
}}

你返回的内容开头不能是```json，直接返回json内容即可。
"""
    return prompt


def format_checks(checks):
    return "\n".join([f"{i+1}. {check}" for i, check in enumerate(checks)])

def form_quality_control_prompt_with_constraints(question, answer, checks):
    prompt = f"""你是核心网运维工程师，给定一个模型生成的问题和答案，请你根据给定的检查项，判断该题目的质量。

====================问题====================
{question}
=============================================

====================答案====================
{answer}
=============================================

检查项：
{format_checks(checks)}

请返回一个json，字段包括score字段和reason字段，score字段表示模型生成的题目和答案符合检查项要求的程度，值为符合检查项除以检查项总数；reason字段应为模型生成的题目和答案不符合检查项要求的原因。

参考格式如下：
{{
    "score": 0.5,
    "reason": "生成的QA对不符合第一个检查项，原因是..."
}}
{{
    "score": 1,
    "reason": "生成的QA对符合所有检查项中描述的要求"
}}

你返回的内容开头不能是```json，直接返回json内容即可。
"""
    return prompt


def form_answer_prompt(kp, question):
    prompt = f"""你是一名核心网运维工程师，请你根据参考资料，回答给定题目。如果你认为给定的题目无法回答，请回复“无法回答”并解释原因。

====================参考资料====================
知识点描述：
{kp['description']}

知识点内容：
{kp['content']}
=============================================

{question}
"""
    return prompt