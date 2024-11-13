import os
import json
import shutil
import numpy as np
from loguru import logger
import random
import matplotlib.pyplot as plt
from math import ceil

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


def output_to_json(files, output_json, encoding='utf-8', root_dir=''):
    data = [
        {
            "filename": file,
            "path": file.replace('.txt', '').replace(root_dir, ''),
            "content": open(file, 'r', encoding=encoding).read()
        } for file in files
    ]
    with open(output_json, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

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
    output_to_json(sampled_files, output_json, encoding='utf-8')


def get_files_in_dir(dir_path, min_chars=200, max_chars=None):
    """获取满足字符数条件的文件"""
    files_in_dir = {}
    for root, dirs, files in os.walk(dir_path):
        valid_files = []
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    char_count = len(content)
                    
                    # 检查字符数是否满足要求
                    if char_count >= min_chars and (max_chars is None or char_count <= max_chars):
                        valid_files.append(file)
            except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
                # 跳过无法读取的文件
                continue
        files_in_dir[root] = valid_files
    return files_in_dir

def sample_files(dir_path, num_samples):
    # 获取所有文件并计算每个子文件夹的文件数
    files_in_dir = get_files_in_dir(dir_path)
    all_files = []
    sub_dir_files_count = {}

    for subdir, files in files_in_dir.items():
        sub_dir_files_count[subdir] = len(files)
        all_files.extend([(subdir, file) for file in files])

    # 计算每个子文件夹的采样权重，并按比例计算采样数量
    total_files = len(all_files)
    sample_counts = {
        subdir: max(ceil(num_samples * (count / total_files)), 1)
        for subdir, count in sub_dir_files_count.items()
    }

    # 从每个子文件夹中采样所需数量的文件
    sampled_files = []
    for subdir, count in sample_counts.items():
        if count > len(files_in_dir[subdir]):
            # 如果采样数大于实际文件数，只能全选
            sampled_files.extend([(subdir, file) for file in files_in_dir[subdir]])
        else:
            sampled_files.extend(random.sample([(subdir, file) for file in files_in_dir[subdir]], count))

    # 返回采样的文件列表
    return [os.path.join(subdir, file) for subdir, file in sampled_files]

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
    
