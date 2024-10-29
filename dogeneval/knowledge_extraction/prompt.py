KNOWLEDGE_POINT_EXTRACT_PROMPT = """你是一名华为的通信领域专家，下面将提供给你一些通信领域的文档，我们将要基于这些文档进行评测集问题的生成，首先请你将这些文档进一步划分为一些知识点，这些知识点可能是文档中的：
1. 概念介绍
2. 事实陈述
3. 处理步骤
4. 表格
5. 代码
6. 具体案例

你提取的知识点内容中，不要对文档中的原文进行改动，只需要将文档原文作为知识点提取出来即可。但你对提取的知识点标题title和描述description需要尽可能包含上下文信息，让不是通信领域专家的人也能理解这个知识点在描述核心网的什么内容。

下面是几个文档的内容：

=========================
{docs_prompt}
=========================

你需要返回如下字段：

{{
    "knowledge_points": [
        {{
            "title": "知识点名称，需要包含涉及部件的名字，而不只是文档中的某个标题",
            "type": "知识点类型",
            "description": "介绍这个知识点描述的内容，需要结合整个文档，避免出现上下文不全的问题",
            "content": "知识点内容",
            "path": "知识点所对应的文档路径",
            "tags": ["标签1", "标签2", ...]
        }}, ...
    ]
}}

下面的输出示例供你参考：

{{
    "knowledge_points": [
        {{
            "title": "5GC网络自治的背景",
            "type": "事实描述",
            "description": "描述5G网络自治产生的背景",
            "content": "随着网络的演进，网络功能越来越多样，网络复杂度越来越高，对应的网络自治手段也需要适配演进",
            "path": "UNC_20.9.5/5G基础知识/一望5G/5G Core业务解决方案解读： NRF解决方案/zh-cn_topic_0242280637.txt",
            "tags": ["5G", "NRF", "背景"]
        }},
        {{
            "title": "5GC网络自治的优势",
            "type": "表格",
            "description": "描述5GC网络自治的优势",
            "content": "**表1** 5G网络相对4G网络优势对比\n| 5G网络 | 4G网络 |\n|---|---|\n| 维护成本 | SBA架构，水平组网免人工规划，可由NRF统一管理分配。 | 4G非SBA架构，某些业务需要根据对端信息进行点对点配置，数据需要人工规划。 |\n| 灵活注册和发现 | NF启动后仅向NRF自动注册，即可实现为网络可知可用。 | 4G网元为网络可用，需在DNS或DRA上增加记录，而DNS/DRA只有静态配置模式，没有自动接口能力，无法实现自发现。 |\n| 自优化 | NRF可实时感知各NF负荷及状态，并动态调整。 | DNS/DRA仅支持静态配置，不支持各网元动态信息获取及调整。 |",
            "path": "UNC_20.9.5/5G基础知识/一望5G/5G Core业务解决方案解读： NRF解决方案/zh-cn_topic_0242280637.txt",
            "tags": ["5G", "NRF", "优势"]
        }}
    ]
}}

请保证你输出的内容完整，你返回的内容开头不能是```json，直接返回json内容即可。
"""

def _form_docs_prompt(docs):
    merged = ""
    for doc in docs:
        merged += f"path: {doc['path']}\n"
        merged += "=========================\n"
        merged += f"{doc['content'].strip()}\n"
        merged += "=========================\n"
    return merged

def form_knowledge_point_extract_prompt(docs):
    if not isinstance(docs, list):
        docs = [docs]
    docs_prompt = _form_docs_prompt(docs)
    return KNOWLEDGE_POINT_EXTRACT_PROMPT.format(docs_prompt=docs_prompt)

if __name__ == "__main__":
    pass