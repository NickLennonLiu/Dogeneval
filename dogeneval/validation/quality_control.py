from dogeneval.utils.parser import try_parse_json
from dogeneval.utils.llm.llms import get_vllm_model
from dogeneval.validation.quality_control_prompt import form_quality_control_prompt, form_check_prompt, form_answer_prompt, form_quality_control_prompt_with_constraints

CONST_CHECKS = [
    '任务说明和用户问题中的内容不存在重复',
    "问题描述完整，没有引用其他来源的内容"
]

def quality_control(question, answer, checks, llm):
    checks.extend(CONST_CHECKS)
    quality_control_prompt = form_quality_control_prompt_with_constraints(question, answer, checks)
    response = llm.chat_json(quality_control_prompt)
    try:
        score, reason = response.get("score", 0), response.get("reason", "")
    except:
        score, reason = None, None
    return score, reason, quality_control_prompt


def try_answering(kp, question, llm):
    answer_prompt = form_answer_prompt(kp, question)
    response = llm.chat(answer_prompt)
    return response, answer_prompt


def check_answer(row, question, answer, llm):
    check_prompt = form_check_prompt(row, question, answer)
    response = llm.chat_json(check_prompt)
    match = response.get("match", False)
    reason = response.get("reason", "")
    return match, reason, check_prompt