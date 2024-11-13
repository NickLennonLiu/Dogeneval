from bs4 import BeautifulSoup
import os
import html2text
import chardet

def parse_html(input_path, output_path):
    # 判断文件的编码
    with open(input_path, 'rb') as f:
        data = f.read()
        encoding = chardet.detect(data)['encoding']

    with open(input_path, 'r', encoding=encoding) as f:
        data = f.read()
    text = parse_html_content(data)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)


def parse_html_content(data):
    soup = BeautifulSoup(data, 'html.parser')
    for img in soup('img'):
        img.decompose()  # 删除<img>标签
    html = str(soup)
    text = html2text.html2text(html, bodywidth=0)

    # 删除文末的版权信息
    text = text.split('\n\n版权所有 © 华为技术有限公司\n\n')[0]
    # 删除文末的上一节和下一节
    text = text.split('[< 上一节]')[0]
    text = text.split('[下一节 >]')[0]

    return text

def parse_htmls(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            input_path = os.path.join(root, file)
            # print(input_path)
            path = os.path.dirname(input_path).replace(input_dir+'/', '')
            output_path = os.path.join(output_dir, path, file.replace('.html', '.txt'))
            # print(output_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            parse_html(input_path, output_path)

if __name__ == '__main__':
    input_dir = './sampled_pages_200'
    output_dir = './sampled_pages_200_txt'
    parse_htmls(input_dir, output_dir)
