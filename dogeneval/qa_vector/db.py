import os

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import CharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS

def load_db(db_dir):
    embedding_model = HuggingFaceBgeEmbeddings(
        model_name="/home/junetheriver/models/AI-ModelScope/bge-large-zh-v1.5",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    db = FAISS.load_local(
        db_dir,
        embedding_model,
        allow_dangerous_deserialization=True
    )
    return db

def gen_db(document_dir, db_name):
    loader = DirectoryLoader(document_dir, 
                             glob="**/*.txt", 
                             show_progress=True,
                             use_multithreading=True,
                             max_concurrency=8,
                             loader_cls=UnstructuredMarkdownLoader,
                             )
    docs = loader.load()
    
    print("Docs loaded")

    documents = docs

    print("Docs split")

    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": True}
    embedding_model = HuggingFaceBgeEmbeddings(
                        model_name="/home/junetheriver/models/AI-ModelScope/bge-large-zh-v1.5",
                        model_kwargs=model_kwargs,
                        encode_kwargs=encode_kwargs
                    )
    
    db = FAISS.from_documents(documents, embedding_model)

    db.save_local(db_name)

def main():
    pass


if __name__ == "__main__":
    document_dir = "/home/junetheriver/datasets/huawei/processed/UNC_20.9.5"
    db_name = "UNC"
    gen_db(document_dir, db_name)