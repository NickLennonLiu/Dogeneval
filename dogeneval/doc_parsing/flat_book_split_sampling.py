"""
对文档结构较为扁平的书籍采样得到sample.json
"""
import os, random, json
import pandas as pd
from dogeneval.doc_parsing.splitter import split_page

def filter_books(book_list):
    black_list = ["游戏", "微信"]
    book_list = [book for book in book_list if not any(black_list_item in book for black_list_item in black_list)]
    return book_list

def sample_book_and_pages(book_folder, book_num, page_num):
    book_list = os.listdir(book_folder)
    book_list = filter_books(book_list)
    random.shuffle(book_list)
    sampled_book_list = book_list[:book_num]
    sample_pages = []
    for book in sampled_book_list:
        page_list = os.listdir(os.path.join(book_folder, book))
        random.shuffle(page_list)
        sampled_page_list = page_list[:page_num]
        sampled_page_list = [os.path.join(book_folder, book, page) for page in sampled_page_list]
        sample_pages.extend(sampled_page_list)
    return sample_pages

def pages_to_splits(pages, root_path):
    splits = []
    for page in pages:
        splits.extend(split_page(page, root_path))
    return splits


if __name__ == "__main__":
    en_book_folder = "/home/junetheriver/codes/qa_generation/huawei/data/data/books_en"
    zh_book_folder = "/home/junetheriver/codes/qa_generation/huawei/data/data/books_zh"
    
    en_sample_pages = sample_book_and_pages(en_book_folder, 10, 10)
    zh_sample_pages = sample_book_and_pages(zh_book_folder, 10, 10)

    en_docs = pages_to_splits(en_sample_pages, en_book_folder)
    zh_docs = pages_to_splits(zh_sample_pages, zh_book_folder)

    with open("en_sample_pages.json", "w", encoding="utf-8") as f:
        json.dump(en_docs, f, ensure_ascii=False, indent=4)
    with open("zh_sample_pages.json", "w", encoding="utf-8") as f:
        json.dump(zh_docs, f, ensure_ascii=False, indent=4)

