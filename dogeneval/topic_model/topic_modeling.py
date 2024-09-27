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

from load_document import load_documents_content

from topic_model.gensim_impl import train_lda_gensim_coherence, train_lda_gensim_perplexity, train_lda_gensim_hdp
from topic_model.sklearn_impl import train_lda_sklearn_perplexity
from topic_model.topmost_impl import train_lda_topmost

def get_stopwords(path = "/home/junetheriver/codes/qa_generation/huawei/data/stopwords/all_stopwords.txt"):
    stop_words = ['html', 'cn', 'Document', 'zh', 'png', 'G', 
                  '参数', '统计', '计算公式', '测量点', '消息', '单位',
                  '性能', '次数', '采集', '命令', '相关', '指标'
                  ]

    stopwords_file = path
    with open(stopwords_file, 'r') as f:
        for line in f:
            stop_words.append(line.strip())

    stop_words = set(stop_words)
    return stop_words

def load_word_ls(path = 'data/word_ls.pkl'):
    with open(path, 'rb') as f:
        word_ls, metadata_ls = pickle.load(f)
    return word_ls, metadata_ls

def gen_word_ls(files, stop_words, 
                word_ls_output = 'data/word_ls.pkl'):
    words_ls = []
    metadata_ls = []
    flags = ('n', 'nr', 'ns', 'nt', 'eng', 'v', 'd')
    # noun, proper noun for a person's name, proper noun for a place, proper noun for a organization, English word, verb, adverb

    for file in files:
        words = [w.word for w in jp.cut(file['content']) if w.flag in flags and w.word not in stop_words]
        words_ls.append(words)
        metadata_ls.append(file)

    with open(word_ls_output, 'wb') as f:
        pickle.dump((words_ls, metadata_ls), f)
    
    return words_ls, metadata_ls

def main1():
    stop_words = get_stopwords()
    files = load_documents_content()
    words_ls, metadata_ls = gen_word_ls(files, stop_words)

def map_topics_to_documents(lda_model, corpus, metadata_ls):
    # 获取每个文档的主题分布
    doc_topics = lda_model.get_document_topics(corpus, minimum_probability=0.0)
    
    # 将主题分布与原始文档元数据关联
    doc_topic_mapping = []
    for doc_topic, metadata in zip(doc_topics, metadata_ls):
        # 将主题分布转换为列表，便于排序
        topic_dist = sorted(doc_topic, key=lambda x: x[1], reverse=True)
        # 获取最主要的主题（概率最高的主题）
        main_topic = topic_dist[0][0]
        doc_topic_mapping.append({
            'metadata': metadata,
            'main_topic': main_topic,
            'topic_distribution': topic_dist
        })
    
    return doc_topic_mapping

def save_topic_document_mapping(doc_topic_mapping, output_file='data/topic_modelling/doc_topic_mapping.json'):
    # 将映射结果保存为JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(doc_topic_mapping, f, ensure_ascii=False, indent=2)

def main2():
    # word_ls, metadata_ls = load_word_ls()
    stop_words = get_stopwords()
    files = load_documents_content()
    word_ls, metadata_ls = gen_word_ls(files, stop_words)

    
    # sklearn implementation
    # best_num_topics, lda = train_lda_sklearn_perplexity(word_ls)
    # gensim coherence implementation
    best_num_topics, lda = train_lda_gensim_coherence(word_ls)
    # gensim perplexity implementation
    best_num_topics, lda = train_lda_gensim_perplexity(word_ls)
    # gensim hdp implementation
    hdp_model, hdp_topics = train_lda_gensim_hdp(word_ls)

    # 生成语料库
    dictionary = corpora.Dictionary(word_ls)
    corpus = [dictionary.doc2bow(words) for words in word_ls]
    
    # 将主题映射回文档
    doc_topic_mapping = map_topics_to_documents(lda, corpus, metadata_ls)
    
    # 保存映射结果
    save_topic_document_mapping(doc_topic_mapping)
    
    # 打印一些示例结果
    print("Sample document-topic mappings:")
    for i, doc_map in enumerate(doc_topic_mapping[:5]):  # 打印前5个文档的映射
        print(f"Document {i+1}:")
        print(f"  Main topic: {doc_map['main_topic']}")
        print(f"  Title: {doc_map['metadata']['title']}")
        print(f"  Top 3 topics: {doc_map['topic_distribution'][:3]}")
        print()

if __name__ == '__main__':
    # main1()
    main2()
                
