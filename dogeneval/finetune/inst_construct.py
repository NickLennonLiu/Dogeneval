"""
从现有的collection中抽取prompt和response的数据，构造用于微调小模型的指令数据集
"""
from dogeneval.utils.mongodb import load_results_as_df

def load_instruct(prompt_col, response_col):
    pass