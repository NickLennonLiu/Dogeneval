"""
10.15临时
"""

from dogeneval.utils.mongodb import load_results

import pandas as pd
import numpy as np

import json, re, os, sys, time, datetime, random

import matplotlib.pyplot as plt

def main1():
    template_file = "/home/junetheriver/codes/qa_generation/huawei/dogeneval/template/templates_1014_v2.json"
    with open(template_file) as f:
        templates = json.load(f)
    pattern_types = [f"{template['L1']}-{template['L2']}-{template['L3']}".replace("/", "") for template in templates if not template['弃用'] and template['L3'] != "其他"]

    print(pattern_types)
    # get_template_patterns

    kp_mapping_result = "kp_template_mapping"
    results = load_results(kp_mapping_result)
    # print(results[0])
    df = pd.DataFrame(results)
    # print(df.columns)

    df_types = pd.DataFrame(df[pattern_types]).copy(deep=True)

    print(df_types)

    print(df_types.columns)

    for pattern in pattern_types:
        print(pattern)
        assert pattern in df_types.columns
        df_types[pattern].fillna({"choose": False})
        df_types[pattern] = df_types[pattern].apply(lambda x: x['choose'] if not isinstance(x, float) else False)
    
    print(df_types)

    import matplotlib.pyplot as plt

    # 设置中文字体 (SimHei 是常用的中文字体之一)
    plt.rcParams['font.family'] = ['simhei']  # 用于正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False    # 用于正常显示负号

    # 1. 计算每列中True的数量并绘制柱状图
    def plot_true_counts_per_column(df):
        true_counts_columns = df.sum()  # 计算每列的True值数量
        plt.figure(figsize=(10, 6))
        true_counts_columns.plot(kind='bar', color='skyblue')
        plt.title('知识点匹配模板情况')
        plt.xlabel('模板类型')
        plt.ylabel('知识点匹配数')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("demo/true_counts_per_column.png")
        # plt.show()

    # 2. 计算每行中True的数量并绘制直方图
    def plot_true_counts_per_row(df):
        true_counts_rows = df.sum(axis=1)  # 计算每行的True值数量
        plt.figure(figsize=(10, 6))
        plt.hist(true_counts_rows, bins=range(0, df.shape[1] + 2), color='salmon', edgecolor='black', alpha=0.7)
        plt.title('知识点匹配模板个数直方图')
        plt.xlabel('匹配模板数')
        plt.ylabel('频率')
        plt.tight_layout()
        plt.savefig("demo/true_counts_per_row.png")
        # plt.show()

    plot_true_counts_per_column(df_types)

    plot_true_counts_per_row(df_types)

if __name__ == "__main__":
    results1 = load_results("Q2-10141807")
    results2 = load_results("Q2-10142039")

    results = results1 + results2

    df = pd.DataFrame(results)
    df = df[[
        'L1', 'L2', 'L3',
        'template', 'Q2_response_azure', 
        'kp_title', 'kp_content',
        'kp_type',
        
        'Q2_azure',
        'A2_azure',
        'error_azure',
        'match_azure',
        'reason_azure',
        'kp_path',
    ]]

    df.to_excel("demo/kpqa_1015.xlsx", index=False)

    df['name'] = df['L1'] + "-" + df['L2'] + "-" + df['L3']

    # 以df['name']为组，统计error_azure中出现"Parse"的行的数量
    df['error_azure'] = df['error_azure'].fillna("")
    df['parse_error'] = df['error_azure'].apply(lambda x: "KeyError in response" in x or 'JSON Parse Error' in x)

    df['reject'] = df['error_azure'].apply(lambda x: "Error in response" in x and "KeyError" not in x)

    df['not_match'] = df['match_azure'].apply(lambda x: not x)

    df['ok'] = df['match_azure'] & ~df['parse_error'] & ~df['reject']

    df_statics = df[[
        'name', 
        'reject',
        'parse_error',
        'not_match',
        'ok',
        'error_azure'
    ]]

    # 确认df_statics中每行有且只有一个True，否则报错输出该行

    for i, row in df_statics.iterrows():
        # 将row转换为Series，计算True的数量
        true_num = sum([row[col] for col in df_statics.columns if col != 'name' and col != 'error_azure'])
        if true_num != 1:
            print(row)
            raise ValueError("Error in row")

    df_statics = df_statics.drop(columns=['error_azure'])

    # 统计每个name的情况
    df_statics = df_statics.groupby('name').sum()

    print(df_statics)

    name = df_statics.index
    print(name)

    reject = np.array(df_statics['reject'])
    parse_error = np.array(df_statics['parse_error'])
    not_match = np.array(df_statics['not_match'])
    ok = np.array(df_statics['ok'])

    totals = reject + parse_error + not_match + ok

    percent_reject = reject / totals * 100
    percent_parse_error = parse_error / totals * 100
    percent_not_match = not_match / totals * 100
    percent_ok = ok / totals * 100

    # 绘制百分比堆叠柱状图
    import plotly.graph_objects as go

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=name,
        y=percent_ok,
        name='OK',
        marker=dict(color='green')
    ))

    fig.add_trace(go.Bar(
        x=name,
        y=percent_not_match,
        name='Not Match',
        marker=dict(color='red')
    ))

    fig.add_trace(go.Bar(
        x=name,
        y=percent_parse_error,
        name='Parse Error',
        marker=dict(color='blue')
    ))

    fig.add_trace(go.Bar(
        x=name,
        y=percent_reject,
        name='Reject',
        marker=dict(color='gray')
    ))

    fig.update_layout(barmode='stack')

    fig.write_image("demo/stacked_bar.png", width=1200, height=800, scale=2)


