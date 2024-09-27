from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document

prompt_template = (
    "{context}"
    "\n\n"
    "你是一名华为云核专家，你需要根据检索到的相关文档内容回答用户的问题。"
    "如果你不知道答案，说你不知道，并直接返回提供的文档内容。"
    "控制输出长度，并指出答案的位置。"
    "\n\n"
    "用户问题：{input}"
)

def get_rag_chain(llm, db):
    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "input"]
    )

    qa_chain = create_stuff_documents_chain(llm, prompt)

    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    rag_chain = create_retrieval_chain(retriever, qa_chain)

    return rag_chain

def main():
    pass

if __name__ == "__main__":
    main()