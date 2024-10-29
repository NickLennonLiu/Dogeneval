from dogeneval.utils.parser import try_parse_json
from dogeneval.utils.llm.llms import get_vllm_model
from dogeneval.quality_assessment.quality_control_prompt import form_quality_control_prompt, form_check_prompt, form_answer_prompt


def quality_control(template, question):
    prompt = form_quality_control_prompt(template, question)
    model = get_vllm_model()
    response = model.generate(prompt)
    return try_parse_json(response)


def try_answering(kp, question, llm):
    answer_prompt = form_answer_prompt(kp, question)
    response = llm.chat(answer_prompt)
    return response


def check_answer(row, question, answer, llm):
    check_prompt = form_check_prompt(row, question, answer)
    response = llm.chat_json(check_prompt)
    match = response.get("match", False)
    reason = response.get("reason", "")
    return match, reason