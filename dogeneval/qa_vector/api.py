from fastapi import FastAPI, Request
from llms import get_vllm_model
from chain import get_rag_chain
from db import load_db

app = FastAPI()

db_dir = "UNC"
db = load_db(db_dir)
model_path = "/home/junetheriver/models/Qwen/Qwen2-72B-Instruct-AWQ"
llm = get_vllm_model(model_path, num_gpu=4)
rag_chain = get_rag_chain(llm, db)

@app.post("/process")
async def process_request(request: Request):
    data = await request.json()
    input_text = data.get("input", "")
    # 调用LangChain进行处理
    result = rag_chain.invoke({"input": input_text})['answer']
    return {"result": result}

# 运行服务
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)