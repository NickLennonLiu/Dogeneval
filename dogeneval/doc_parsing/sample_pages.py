import os
import json
import shutil
import numpy as np
from loguru import logger
import matplotlib.pyplot as plt
import random
def collect_all_files(src_directory, dest_directory):
    # 如果目标文件夹不存在，则创建
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    # 遍历源文件夹的所有子目录
    for root, dirs, files in os.walk(src_directory):
        for file in files:
            # 构建文件的完整路径
            file_path = os.path.join(root, file)

            # 构建目标文件的路径，不带目录结构，直接放到目标文件夹
            dest_path = os.path.join(dest_directory, file)

            # 如果目标文件夹中已存在相同文件名的文件，避免覆盖
            if os.path.exists(dest_path):
                base, extension = os.path.splitext(file)
                dest_path = os.path.join(dest_directory, f"{base}_copy{extension}")

            # 复制文件到目标文件夹
            shutil.copy2(file_path, dest_path)
            print(f"Copied {file_path} to {dest_path}")


def collect_file_lengths_by_characters(directory):
    file_lengths = []

    # 遍历目录及其子目录中的所有文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                # 读取文件并计算字符数
                with open(file_path, 'r', encoding='gbk') as f:
                    content = f.read()
                    file_lengths.append(len(content))
            except (OSError, UnicodeDecodeError) as e:
                print(f"Error reading {file_path}: {e}")

    return file_lengths


def sample_page_with_path(src_dir, output_json, sample_size=200):
    sampled_files = []

    mml_count = 500

    for root, dirs, files in os.walk(src_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getsize(file_path) > 2000:
                if "UNC MML命令" in file_path:
                    mml_count -= 1
                    if mml_count > 0:
                        sampled_files.append(file_path)
                else:
                    sampled_files.append(file_path)
    logger.info(f"sampled files: {len(sampled_files)}, mml_count: {500 - mml_count}")
    sampled_files = random.sample(sampled_files, sample_size)
    # 将filename, path, content保存到output_json
    data = [
        {
            "filename": file,
            "path": file.replace('.txt', ''),
            "content": open(file, 'r', encoding='gbk').read()
        } for file in sampled_files
    ]
    with open(output_json, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    src_dir = '/home/junetheriver/codes/qa_generation/huawei/data/sampled_pages'  # 替换为源文件夹路径
    dest_dir = '/home/junetheriver/codes/qa_generation/huawei/data/sampled_pages_all'  # 替换为目标文件夹路径

    # # collect_all_files(src_dir, dest_dir)
    # lengths = collect_file_lengths_by_characters(dest_dir)

    # # 画出lengths的分布图
    # plt.hist(lengths, bins=100, edgecolor='black', range=(0, 20000))
    # plt.show()
    # plt.savefig('lengths_distribution.png')

    # # 采样dest_dir中字符数大于8000的文件200个
    # sampled_files = []
    # for root, dirs, files in os.walk(dest_dir):
    #     for file in files:
    #         file_path = os.path.join(root, file)
    #         if os.path.getsize(file_path) > 8000:
    #             sampled_files.append(file_path)
    # print(len(sampled_files))
    # # 从sampled_files中随机采样200个
    # sampled_files = random.sample(sampled_files, 200)
    # print(len(sampled_files))
    # # 保存sampled_files到sampled_pages_200
    # os.makedirs('sampled_pages_200', exist_ok=True)
    # for file in sampled_files:
    #     shutil.copy(file, os.path.join('sampled_pages_200', os.path.basename(file)))

    output_json = '/home/junetheriver/codes/qa_generation/huawei/data/sampled_pages_200.json'
    sample_page_with_path(src_dir, output_json, sample_size=200)
    
