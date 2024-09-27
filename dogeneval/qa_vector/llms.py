from langchain_community.llms import VLLM


def get_vllm_model(model_path='/home/junetheriver/models/qwen/Qwen1.5-72B-Chat-AWQ',
                   num_gpu=4):
    llm = VLLM(
        model=model_path,
        trust_remote_code=True,
        max_new_tokens=800,
        tensor_parallel_size=num_gpu,
    )

    return llm

def get_azure_model():
    pass


if __name__ == "__main__":
    test_model = "/home/junetheriver/models/Qwen/Qwen2-0.5B-Instruct"
    llm = get_vllm_model(test_model, num_gpu=1)
    print(llm.invoke("test"))