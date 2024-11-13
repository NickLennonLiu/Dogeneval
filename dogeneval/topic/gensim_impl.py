import pandas as pd
import json, os, re
import pickle
from gensim import corpora, models
import jieba.posseg as jp, jieba
from tqdm import tqdm
from loguru import logger
import matplotlib.pyplot as plt

def train_lda_gensim(words_ls, num_topics = 10):
    # 得到文档-单词矩阵 （直接利用统计词频得到特征）
    dictionary = corpora.Dictionary(words_ls)
    # 将dictionary转化为一个词袋，得到文档-单词矩阵
    corpus = [dictionary.doc2bow(words) for words in words_ls]
    # 词袋处理后的结果，使用TF-IDF算法处理后，可以进一步提升LDA的效果
    texts_tf_idf = models.TfidfModel(corpus)[corpus]

    lda = models.LdaMulticore(corpus=texts_tf_idf, id2word=dictionary, num_topics=num_topics)

    # save model
    lda.save('data/topic_modelling/lda_gensim.model')

    for topic in lda.print_topics(num_words=20):
        print(topic)

    return lda

def train_lda_gensim_coherence(words_ls):
    """
    基于主题一致性 Topic Coherence 选择合适的主题数，并训练 LDA 模型
    """
    from gensim.models.coherencemodel import CoherenceModel

    dictionary = corpora.Dictionary(words_ls)
    corpus = [dictionary.doc2bow(words) for words in words_ls]
    texts_tf_idf = models.TfidfModel(corpus)[corpus]

    num_topics_range = range(2, 10)

    coherence_scores = []
    lda_models = []
    for num_topics in tqdm(num_topics_range, desc="Training LDA models"):
        lda_model = models.LdaMulticore(corpus=texts_tf_idf, id2word=dictionary, num_topics=num_topics)
        coherence_model = CoherenceModel(model=lda_model, texts=words_ls, dictionary=dictionary, coherence='c_v')
        coherence_scores.append(coherence_model.get_coherence())
        lda_models.append(lda_model)

    best_num_topics = num_topics_range[coherence_scores.index(max(coherence_scores))]
    print(f"Best number of topics: {best_num_topics}")

    # Plot the coherence scores
    plt.figure(figsize=(10, 6))
    plt.plot(num_topics_range, coherence_scores, marker='o', linestyle='-', color='b')
    plt.xlabel('Number of Topics')
    plt.ylabel('Coherence Score')
    plt.title('Coherence Scores for Different Number of Topics')
    plt.grid(True)
    plt.savefig('data/topic_modelling/coherence_scores.png')
    plt.show()

    # 输出每个主题的 top 10 词
    best_lda = lda_models[best_num_topics-2]
    for tid, topic in best_lda.print_topics(num_words=10):
        print(f"Topic {tid}: {topic}")

    # 保存话题
    with open(f"data/topic_modelling/lda_gensim_{best_num_topics}_topics.txt", "w") as f:
        for tid, topic in best_lda.print_topics(num_words=10):
            f.write(f"Topic {tid}: {topic}\n")

    return best_num_topics, lda_models[best_num_topics-2]

def train_lda_gensim_perplexity(words_ls):
    """
    基于困惑度计算 LDA 的合适主题数
    """
    dictionary = corpora.Dictionary(words_ls)
    corpus = [dictionary.doc2bow(words) for words in words_ls]
    texts_tf_idf = models.TfidfModel(corpus)[corpus]

    num_topics_range = range(2, 10)

    perplexity_scores = []
    lda_models = []
    for num_topics in tqdm(num_topics_range, desc="Training LDA models"):
        lda_model = models.LdaMulticore(corpus=texts_tf_idf, id2word=dictionary, num_topics=num_topics)
        log_perplexity = lda_model.log_perplexity(texts_tf_idf)
        perplexity_scores.append(log_perplexity)
        lda_models.append(lda_model)

    best_num_topics = num_topics_range[perplexity_scores.index(min(perplexity_scores))]
    print(f"Best number of topics: {best_num_topics}")

    # Plot the perplexity scores
    plt.figure(figsize=(10, 6))
    plt.plot(num_topics_range, perplexity_scores, marker='o', linestyle='-', color='b')
    plt.xlabel('Number of Topics')
    plt.ylabel('Perplexity Score')
    plt.title('Perplexity Scores for Different Number of Topics')
    plt.grid(True)
    plt.savefig('data/topic_modelling/perplexity_scores.png')
    plt.show()

    # 输出每个主题的 top 10 词
    best_lda = lda_models[best_num_topics-2]
    for tid, topic in best_lda.print_topics(num_words=10):
        print(f"Topic {tid}: {topic}")

    # 保存话题
    with open(f"data/topic_modelling/lda_gensim_{best_num_topics}_topics_perplexity.txt", "w") as f:
        for tid, topic in best_lda.print_topics(num_words=10):
            f.write(f"Topic {tid}: {topic}\n")

    return best_num_topics, lda_models[best_num_topics-2]

def train_lda_gensim_hdp(words_ls):
    """
    HDP 模型
    """
    from gensim.models.hdpmodel import HdpModel

    dictionary = corpora.Dictionary(words_ls)
    corpus = [dictionary.doc2bow(words) for words in words_ls]
    hdp_model = HdpModel(corpus, id2word=dictionary)

    hdp_topics = hdp_model.show_topics()

    # save model
    hdp_model.save('data/topic_modelling/hdp_model.model')

    return hdp_model, hdp_topics