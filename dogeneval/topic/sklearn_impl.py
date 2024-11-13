import pandas as pd
import json, os, re
import pickle
from gensim import corpora, models
import jieba.posseg as jp, jieba
from tqdm import tqdm
from loguru import logger
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import LatentDirichletAllocation


def train_lda_sklearn(words_ls, num_topics = 10):
    """
    sklearn 实现 LDA 模型
    """
    documents = [' '.join(words) for words in words_ls]

    # 将文档-单词矩阵转化为TF-IDF矩阵
    vectorizer = CountVectorizer()
    tfidf_transformer = TfidfTransformer()
    tfidf_matrix = tfidf_transformer.fit_transform(vectorizer.fit_transform(documents))

    lda = LatentDirichletAllocation(n_components=num_topics, max_iter=50, learning_method='online', learning_offset=50., random_state=0)
    lda.fit(tfidf_matrix)

    # save model
    lda.save('data/topic_modelling/lda_sklearn.model')

    return lda

def train_lda_sklearn_perplexity(words_ls):
    """
    基于困惑度计算 LDA 的合适主题数
    """
    documents = [' '.join(words) for words in words_ls]

    vectorizer = CountVectorizer()
    tfidf_transformer = TfidfTransformer()
    tfidf_matrix = tfidf_transformer.fit_transform(vectorizer.fit_transform(documents))
    dictionary = vectorizer.get_feature_names_out()

    num_topics_range = range(2, 10)
    perplexities = []
    ldas = []
    for num_topics in tqdm(num_topics_range, desc="Training LDA models"):
        lda = LatentDirichletAllocation(n_components=num_topics, max_iter=10, learning_method='online', learning_offset=10., random_state=0)
        lda.fit(tfidf_matrix)
        perplexities.append(lda.perplexity(tfidf_matrix))
        ldas.append(lda)

    best_num_topics = num_topics_range[perplexities.index(min(perplexities))]

    print(f"Best number of topics: {best_num_topics}")

    # Plot the perplexities
    plt.figure(figsize=(10, 6))
    plt.plot(num_topics_range, perplexities, marker='o', linestyle='-', color='b')
    plt.xlabel('Number of Topics')
    plt.ylabel('Perplexity')
    plt.title('Perplexity for Different Number of Topics')
    plt.grid(True)
    plt.savefig('data/topic_modelling/perplexity.png')
    plt.show()

    # 输出每个主题的 top 10 词
    best_lda = ldas[best_num_topics]
    for i, topic in enumerate(best_lda.components_):
        print(f"Topic {i + 1}:")
        print([dictionary.get(idx) for idx in topic.argsort()[:-11:-1]])
        print()
    
    return best_num_topics, ldas[best_num_topics]