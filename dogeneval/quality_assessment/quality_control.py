from utils.parser import try_parse_json
from huawei.llm.llms import get_vllm_model
from quality_control_prompt import generate_prompt

def quality_control(template, question):
    prompt = generate_prompt(template, question)
    model = get_vllm_model()
    response = model.generate(prompt)
    return try_parse_json(response)