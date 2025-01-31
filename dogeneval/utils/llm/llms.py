from openai import OpenAI

from dogeneval.utils.parser import try_parse_json
from dogeneval.utils.decorators import retry
import requests

openai_api_key = "EMPTY"
chatanywhere_api_key = "sk-bLpSKRfukRTVQFsqTSjkwHxWpS7p8qywofrzH5q2Ks3UcqKp"

def get_vllm_model(model_path='/home/junetheriver/models/qwen/Qwen1.5-72B-Chat-AWQ', num_gpu=4):
    from vllm import LLM, SamplingParams
    # model = "/mnt/tenant-home_speed/xz/opsfm-xz/models/Qwen/Qwen1.5-32B-Chat"
    
    llm = LLM(model=model_path, 
              trust_remote_code=True, 
              max_model_len=8192, 
              tensor_parallel_size=num_gpu, 
              gpu_memory_utilization=0.9)

    return llm


class AzureClient:
    
    def __init__(self):
        self.llm = self.get_azure_model()

    def get_azure_model(self):
        from langchain_openai.chat_models import AzureChatOpenAI
        llm = AzureChatOpenAI(
            # gpt4
            azure_endpoint="https://swedencentralchatgpt.openai.azure.com/",
            # azure_ad_token="1df6890f43db40e093c00df74e3fc185",
            api_key="1df6890f43db40e093c00df74e3fc185",
            openai_api_version="2024-02-01",
            azure_deployment="gpt4-test",
            
            # gpt4o
            # api_key = "77d239285ca8450287186024ffc22f57",
            # api_version = "2024-02-01",
            # azure_endpoint = "https://eastuszhiyan.openai.azure.com/",
            # azure_deployment = "gpt4o-test",
            # model = "gpt-4o",
        )
        return llm
    
    @retry(default_return_value="")
    def chat(self, prompt):
        response = self.llm.invoke(prompt).content
        return response
    
    @retry(default_return_value=dict())
    def chat_json(self, prompt):
        response = self.llm.invoke(prompt).content
        return try_parse_json(response)
    
    def balance(self):
        return -1


def get_azure_model():
    return AzureClient()

def qwen_template(prompt):
    prompt = f"<|im_start|>system\nYou are a helpful assistant.<|im_end|><|im_start|>user\n{prompt}<|im_end|><|im_start|>assistant\n"
    return prompt

def get_qwen_answer(llm, questions):
    from vllm import SamplingParams
    questions = [qwen_template(q) for q in questions]
    sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=8192, stop_token_ids=[151643, 151645], stop=['<|endoftext|>', '<|im_end|>'])
    answers = llm.generate(questions, sampling_params=sampling_params, use_tqdm=False)
    return answers
    


class OpenAIClient:
    def __init__(self, model="/home/junetheriver/models/Qwen/Qwen2-72B-Instruct-AWQ",
                        api_base="http://10.0.0.1:8080/v1",
                        temperature=0.7,
                        top_p=0.8,
                        repetition_penalty=1.05,
                        max_tokens=4096):
        self.client = OpenAI(api_key=openai_api_key, base_url=api_base)
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.repetition_penalty = repetition_penalty
        self.max_tokens = max_tokens

    def generate(self, prompt):
        chat_response = self.client.chat.completions.create(
            model = self.model,
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=self.max_tokens,
            extra_body={
                "repetition_penalty": self.repetition_penalty,
            }
        )
        return chat_response
    
    def chat(self, prompt):
        chat_response = self.generate(prompt)
        return chat_response.choices[0].message.content
    
    def chat_json(self, prompt):
        chat_response = self.generate(prompt)
        return try_parse_json(chat_response.choices[0].message.content)

    def balance(self):
        return -1

def get_openai_model():
    return OpenAIClient()


class ChatAnywhereClient():
    def __init__(self):
        self.key = chatanywhere_api_key
        self.client = OpenAI(
            api_key=chatanywhere_api_key, 
            base_url="https://api.chatanywhere.tech/v1")
        self.model = "gpt-4o-ca"

    def chat(self, prompt):
        chat_response = self.client.chat.completions.create(
            model = self.model,
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return chat_response.choices[0].message.content
    
    def chat_json(self, prompt):
        chat_response = self.chat(prompt)
        return try_parse_json(chat_response)

    def balance(self):
        url = "https://api.chatanywhere.org/v1/query/balance"
        response = requests.post(url, headers={"Authorization": f"{self.key}"}).json()
        balance = response.get("balanceTotal") - response.get("balanceUsed")
        return balance

def get_chatanywhere_model():
    return ChatAnywhereClient()


if __name__ == "__main__":
    llm = get_chatanywhere_model()
    from loguru import logger
    logger.info(llm.chat("Please reply: API test success."))
    logger.info(llm.balance())