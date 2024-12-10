KNOWLEDGE_POINT_EXTRACT_PROMPT_ZH = """你是一名运维领域专家，下面将提供给你一些运维领域的文档，我们将要基于这些文档进行评测集问题的生成，首先请你将这些文档进一步划分为一些知识点，这些知识点可能是文档中的：
1. 事实陈述
2. 处理步骤
3. 列表
4. 表格
5. 代码
6. 具体案例

你提取的知识点内容中，不要对文档中的原文进行改动，只需要将文档原文作为知识点提取出来即可。但你对提取的知识点标题title和描述description需要尽可能包含上下文信息，让不是运维领域专家的人也能理解这个知识点在描述什么内容。

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

KNOWLEDGE_POINT_EXTRACT_PROMPT_EN = """You are an expert in the IT Operations field. Below, you will be provided with some documents related to IT Operations. Based on these documents, we aim to generate evaluation set questions. First, please divide these documents into specific knowledge points. These knowledge points may include:
 
1. Factual statement  
2. Processing step 
3. List  
4. Table  
5. Code  
6. Use case  

When extracting the content of knowledge points, do not modify the original text from the documents. Simply extract the text as-is from the documents. However, for the titles and descriptions of the extracted knowledge points, you must ensure they include sufficient context so that individuals who are not operations experts can understand what the knowledge point describes.

Below is the content of several documents:

=========================
{docs_prompt}
=========================

You need to return the following fields:

{{
    "knowledge_points": [
        {{
            "title": "The name of the knowledge point, which should include the related component's name, not just a title from the document",
            "type": "Type of knowledge point",
            "description": "A description of the knowledge point's content, providing enough context to avoid ambiguity",
            "content": "The content of the knowledge point",
            "path": "The document path corresponding to the knowledge point",
            "tags": ["Tag1", "Tag2", ...]
        }}, ...
    ]
}}

Here is an example of the expected output:

{{
    "knowledge_points": [
        {{
            "title": "Background of 5GC Network Autonomy",
            "type": "Factual statement",
            "description": "Describes the background of 5G network autonomy",
            "content": "With the evolution of networks, network functions have become increasingly diverse, and the complexity of the networks has grown, requiring autonomous methods to adapt to this evolution.",
            "path": "UNC_20.9.5/5G Basics/Overview of 5G/5G Core Business Solution Analysis: NRF Solution/zh-cn_topic_0242280637.txt",
            "tags": ["5G", "NRF", "Background"]
        }},
        {{
            "title": "Advantages of 5GC Network Autonomy",
            "type": "Table",
            "description": "Describes the advantages of 5GC network autonomy",
            "content": "**Table 1** Comparison of advantages between 5G and 4G networks\n| 5G Network | 4G Network |\n|---|---|\n| Maintenance Cost | SBA architecture, horizontal networking without manual planning, unified management and allocation by NRF. | Non-SBA architecture in 4G, where some services require point-to-point configuration based on counterpart information, with manual planning of data. |\n| Flexible Registration and Discovery | NF automatically registers with NRF upon startup, making it network-known and available. | For 4G network elements to be available, records must be added to DNS or DRA, which only supports static configurations without automatic interface capabilities, making self-discovery impossible. |\n| Self-Optimization | NRF can sense the load and status of each NF in real time and dynamically adjust. | DNS/DRA only supports static configurations and does not support the dynamic acquisition and adjustment of network element information. |",
            "path": "UNC_20.9.5/5G Basics/Overview of 5G/5G Core Business Solution Analysis: NRF Solution/zh-cn_topic_0242280637.txt",
            "tags": ["5G", "NRF", "Advantages"]
        }}
    ]
}}

Ensure your output is complete. Do not prepend the content with ```json. Directly return the JSON content.
"""

KNOWLEDGE_POINT_LABEL_PROMPT_ZH = """你是一名运维领域专家，下面将提供给你一个运维领域的知识片段，我们将要基于这些文档进行评测集问题的生成，请你对这个知识片段描述的内容进行总结，并对该知识点的类型进行归类，它可能是但不限于如下类型之一：
1. 事实陈述
2. 处理步骤
3. 列表
4. 表格
5. 代码
6. 具体案例

你总结的知识点标题title和描述description需要尽可能包含上下文信息，让不是运维领域专家的人也能理解这个知识点在描述什么内容。

下面是知识片段的内容：

=========================
{kp_prompt}
=========================

你需要返回如下字段：

{{
    "title": "知识点名称，需要包含涉及部件的名字，而不只是文档中的某个标题",
    "type": "知识点类型",
    "description": "介绍这个知识点描述的内容",
    "tags": ["标签1", "标签2", ...]
}}

下面的输出示例供你参考：

{{
    "title": "5GC网络自治的优势",
    "type": "表格",
    "description": "描述5GC网络自治的优势",
    "tags": ["5G", "NRF", "优势"]
}}

请保证你输出的内容完整，你返回的内容开头不能是```json，直接返回json内容即可。
"""

KNOWLEDGE_POINT_LABEL_PROMPT_EN = """You are an expert in the operations field. Below, you will be provided with a knowledge fragment from the operations domain. Based on this, we aim to generate evaluation set questions. Please summarize the content described in this knowledge fragment and classify the type of knowledge point. It may fall into, but is not limited to, one of the following types:

1. Factual statement  
2. Processing step 
3. List  
4. Table  
5. Code  
6. Use case 

For the title and description of the knowledge point you summarize, ensure they include sufficient context so that individuals who are not experts in the operations domain can understand what the knowledge point is about.

Below is the content of the knowledge fragment:

=========================
{kp_prompt}
=========================

You need to return the following fields:

{{
    "title": "The name of the knowledge point, which should include the name of the related component, not just a title from the document",
    "type": "Type of knowledge point",
    "description": "A description of the content of the knowledge point",
    "tags": ["Tag1", "Tag2", ...]
}}

Here is an example of the expected output:

{{
    "title": "Advantages of 5GC Network Autonomy",
    "type": "Table",
    "description": "Describes the advantages of 5GC network autonomy",
    "tags": ["5G", "NRF", "Advantages"]
}}

Ensure your output is complete. Do not prepend the content with ```json. Return the JSON content directly.
"""

def _form_docs_prompt(docs):
    merged = ""
    for doc in docs:
        merged += f"path: {doc['path']}\n"
        merged += "=========================\n"
        merged += f"{doc['content'].strip()}\n"
        merged += "=========================\n"
    return merged

def form_knowledge_point_extract_prompt(docs, lang="zh"):
    if not isinstance(docs, list):
        docs = [docs]
    docs_prompt = _form_docs_prompt(docs)
    if lang == "zh":
        return KNOWLEDGE_POINT_EXTRACT_PROMPT_ZH.format(docs_prompt=docs_prompt)
    else:
        return KNOWLEDGE_POINT_EXTRACT_PROMPT_EN.format(docs_prompt=docs_prompt)

def form_knowledge_point_label_prompt(kp, lang="zh"):
    doc_prompt = _form_docs_prompt([kp])
    if lang == "zh":
        return KNOWLEDGE_POINT_LABEL_PROMPT_ZH.format(kp_prompt=doc_prompt)
    else:
        return KNOWLEDGE_POINT_LABEL_PROMPT_EN.format(kp_prompt=doc_prompt)

if __name__ == "__main__":
    pass