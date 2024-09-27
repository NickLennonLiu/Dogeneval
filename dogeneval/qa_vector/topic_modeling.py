import faiss
import pickle
from sklearn.cluster import KMeans
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
import numpy as np


embeddings = HuggingFaceBgeEmbeddings(
        model_name="/home/junetheriver/models/AI-ModelScope/bge-large-zh-v1.5",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
vector_store = FAISS.load_local("UNC", embeddings=embeddings, allow_dangerous_deserialization=True)
vector_store.docstore


vectorstore_data = vector_store.get(include=['embeddings', 'metadatas'])
embs = vectorstore_data['embeddings']

num_clusters = 10

kmeans = KMeans(n_clusters=num_clusters, random_state=0)

cluster_assignments = kmeans.fit_predict(embs)

print(cluster_assignments)