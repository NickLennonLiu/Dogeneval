"""
比较直白地从数据库的结果中显示各种统计信息
"""
import pandas as pd
from dogeneval.utils.mongodb import load_results_as_df
import plotly.express as px


def plot_bar_plot_from_db(collection_name, field_name, title, filter=None):
    df = load_results_as_df(collection_name)
    df = df[df[field_name].notna()]
    if filter:
        df = filter(df)

    # 统计field_name各个值有多少，用plotly画图
    df_statics = df[field_name].value_counts().reset_index()
    df_statics.columns = [field_name, "count"]
    fig = px.bar(df_statics, x=field_name, y="count", title=title)
    fig.show()


def plot_stacked_bar_chart_from_db(collection_name, group_name, label_name, title, filter=None, preprocess=None, percentage=False, color_palette=None, ylabel=None, xlabel=None):
    """
    1. filter df
    2. preprocess df (often for generating the 'label_name' column)
    3. group by 'group_name' and plot stacked bar chart
    4. if percentage is True, all the count will be divided by the total count of the group
    """
    df = load_results_as_df(collection_name)
    if filter:
        df = filter(df)
    if preprocess:
        df = preprocess(df)
    df_statics = df.groupby(group_name)[label_name].value_counts().reset_index()
    df_statics.columns = [group_name, label_name, "count"]
    y_label = "count" if ylabel is None else ylabel
    x_label = group_name if xlabel is None else xlabel
    if percentage:
        total_count = df_statics.groupby(group_name)["count"].sum()
        df_statics["count"] = df_statics.apply(lambda row: row["count"] / total_count[row[group_name]], axis=1)
        y_label="percentage" if y_label is None else y_label

    # group_name按照label_name为'合格'的值大小排序
    df_statics = df_statics.sort_values(by=["count", label_name], ascending=[False, True])

    fig = px.bar(
        df_statics,
        x=group_name,
        y="count",
        color=label_name,
        barmode="stack",
        title=title,
        color_discrete_sequence=color_palette
    )
    fig.update_layout(yaxis_title=y_label, xaxis_title=x_label)
    fig.show()


def plot_pie_chart_from_db(collection_name, field_name, title, filter=None):
    df = load_results_as_df(collection_name)
    if filter:
        df = filter(df)
    df = df[df[field_name].notna()]
    
    df_statics = df[field_name].value_counts().reset_index()
    df_statics.columns = [field_name, "count"]
    fig = px.pie(df_statics, values="count", names=field_name, title=title)
    fig.show()