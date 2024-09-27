from codes.qa_vector.llms import get_vllm_model
from chain import get_rag_chain
from db import load_db


def main():
    db_dir = "UNC"
    db = load_db(db_dir)
    model_path = "/home/junetheriver/models/Qwen/Qwen2-0.5B-Instruct-AWQ"
    llm = get_vllm_model(model_path, num_gpu=1)
    rag_chain = get_rag_chain(llm, db)
    # print(rag_chain)
    result = rag_chain.invoke({"input": "介绍一下RMV NVPROFILE这个命令"})
    print(result['answer'])


if __name__ == "__main__":
    main()