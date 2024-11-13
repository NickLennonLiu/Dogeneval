"""
起一个gradio服务，以看板的形式展示一个df中的规定字段，每一行为一个卡片，按照指定列进行group
"""
from dogeneval.utils.mongodb import load_results_as_df
import gradio as gr
import pandas as pd

df = load_results_as_df("QA_GEN_11022040")

# 定义显示字段
display_fields = ["Question", "Answer", "match_reason"]

# 创建看板视图函数
def create_kanban(df, group_by_column, display_fields):
    grouped = df.groupby(group_by_column)
    kanban_html = "<div style='display: flex; flex-wrap: wrap;'>"

    for group_name, group_df in grouped:
        kanban_html += f"<div style='width: 100%; margin-top: 20px;'><h3>分组: {group_name}</h3></div>"
        for _, row in group_df.iterrows():
            kanban_html += "<div style='border: 1px solid #ccc; padding: 10px; margin: 10px; width: 200px;'>"
            for field in display_fields:
                kanban_html += f"<p><strong>{field}:</strong> {row[field]}</p>"
            kanban_html += "</div>"

    kanban_html += "</div>"
    return kanban_html

# Gradio 界面
def kanban_view(group_by_column):
    return create_kanban(df, group_by_column, display_fields)

# 设置 Gradio 接口
group_by_column_options = list(df.columns)  # 用于分组的列选项

gr.Interface(
    fn=kanban_view,
    inputs=gr.Dropdown(choices=group_by_column_options, label="选择分组列"),
    outputs="html",
    title="DataFrame 看板展示",
    description="选择一个列进行分组，查看每个组的卡片展示。"
).launch()