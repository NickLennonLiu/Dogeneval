import torch
from transformers import AutoTokenizer, AutoModel
from FlagEmbedding import FlagAutoModel
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from loguru import logger

# 加载模型和tokenizer
model_name = "/home/junetheriver/models/AI-ModelScope/bge-large-zh-v1.5"
model = FlagAutoModel.from_finetuned(model_name, query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
                                    use_fp16=True)

# 定义生成embedding的函数
def get_embedding(text):
    embedding = model.encode(text)
    return embedding

# 计算两两相似度的平均值
def calculate_avg_similarity(instructions, show_progress=False):
    if show_progress:
        logger.info(f"Calculating average similarity for {len(instructions)} instructions...")
    embeddings = [get_embedding(instr) for instr in tqdm(instructions, disable=not show_progress)]
    if show_progress:
        logger.info(f"Embeddings generated for {len(instructions)} instructions.")
    similarity_matrix = cosine_similarity(embeddings)
    if show_progress:
        logger.info(f"Cosine similarity matrix calculated for {len(instructions)} instructions.")
    
    # 计算上三角矩阵的平均值（排除自身相似度）
    upper_triangle = similarity_matrix[np.triu_indices_from(similarity_matrix, k=1)]
    avg_similarity = upper_triangle.mean()
    return avg_similarity


if __name__ == "__main__":
    # 示例指令集
    instructions = [
        "指令1的内容",
        "指令2的内容",
        "指令3的内容"
    ]

    # 计算平均相似度
    avg_similarity = calculate_avg_similarity(instructions)
    print("指令集两两相似度平均值:", avg_similarity)