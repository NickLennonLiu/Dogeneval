from html2txt import parse_htmls
from sample_pages import sample_files, output_to_json

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--html_dir', type=str)
    parser.add_argument('--txt_dir', type=str)
    parser.add_argument('--sample_json', type=str)
    parser.add_argument('--sample_size', type=int, default=200)
    parser.add_argument('--stage', type=str, choices=['html2txt', 'sample'])
    args = parser.parse_args()

    # 原始文件（可能是一个zip、一个目录html）
    # 经过某种处理得到了一个文件夹目录，里面是不同层级的html文件

    html_dir = args.html_dir
    txt_dir = args.txt_dir
    sample_json = args.sample_json
    sample_size = args.sample_size

    # html_dir = "/home/junetheriver/codes/qa_generation/huawei/data/zabbix/zabbix_manual"
    # txt_dir = "/home/junetheriver/codes/qa_generation/huawei/data/zabbix/zabbix_manual_txt"
    # sample_json = "/home/junetheriver/codes/qa_generation/huawei/data/zabbix/zabbix_manual_sample.json"

    if not args.stage or args.stage == 'html2txt':
        parse_htmls(html_dir, txt_dir)

    # 从txt文件夹中采样一定数量的题目

    if not args.stage or args.stage == 'sample':
        sampled_files = sample_files(txt_dir, sample_size)
        output_to_json(sampled_files, sample_json, root_dir=txt_dir)

    
