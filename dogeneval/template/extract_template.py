import json
from huawei.llm.llms import get_azure_model

prompt = """下面我将提供给你一个评测题目的所属类别和题目文本，请你提取这个题目的模板。请注意，题目中可能包含一些针对大模型的提示说明，你需要识别出这些内容，将其作为模版的一部分，对于可能发生变动的部分，作为模板中的待填充字段，并给出字段的具体解释。

你的返回内容需要符合如下格式：

{{
    "能力定义": "给题目类别第一级对应的能力写一段定义文字"
    "模板介绍": "一段关于你生成的模板的介绍",
    "模板正文": "模板正文，用{{}}表示代填字段",
    "字段解释": "关于字段的解释"
}}


示例如下：

题目类别：代码\/MML生成-NL2MML-配置助理
====题目====
你是系统工程师，需要根据参数写业务脚本\n\n下面是一个例子：\n参数：\n#步骤获取NS索引：76；DNN名称：CMIOT5GDCDJ1NB.ZJ；SST标识：128-2C7155；客户：某某企业\n业务脚本：\nSTART\nADD PLMNNS: NSIDX=76, PLMNIDX=0, SST=128, SD=\"2C7155\", STATE=ACTIVE, DESC=\"某某企业\";\nADD NFNS: NFTYPE=NfAMF, NSIDX=76, DESC=\"某某企业\";\nADD LOCALNSDNN:SUBRANGE=HOME_USER, SST=128, SD=\"2C7155\", DNN=\"CMIOT5GDCDJ1NB.ZJ\", CORRECTTYPE=DNN_CORRECTION, DNNPLCY=Default_DNN_preferred, DISFAILPLCY=STANDARD_MODEL;\nEND\n\n根据参数，严格按例子中业务脚本格式，以START开始END结束，写业务脚本\n参数：\n#步骤获取NS索引：0；DNN名称：CMNET；SST标识：127-EEEEEE；客户：for eMBB
====答案====
START\nADD TACGROUPINNSSF: INDEX=6691, TACGROUPNAME=\"128-2C3248\", TACSTART=\"127002\", TACEND=\"127002\";\nADD TACGROUPINNSSF: INDEX=6692, TACGROUPNAME=\"128-2C3248\", TACSTART=\"127050\", TACEND=\"12705A\";\nADD TACGROUPINNSSF: INDEX=6693, TACGROUPNAME=\"128-2C3248\", TACSTART=\"1270B4\", TACEND=\"1270C1\";\nADD TACGROUPINNSSF: INDEX=6694, TACGROUPNAME=\"128-2C3248\", TACSTART=\"127118\", TACEND=\"127129\";\nADD TACGROUPINNSSF: INDEX=6695, TACGROUPNAME=\"128-2C3248\", TACSTART=\"12717C\", TACEND=\"127188\";\nADD TACGROUPINNSSF: INDEX=6696, TACGROUPNAME=\"128-2C3248\", TACSTART=\"1271E0\", TACEND=\"1271E6\";\nADD TACGROUPINNSSF: INDEX=6697, TACGROUPNAME=\"128-2C3248\", TACSTART=\"127244\", TACEND=\"12724B\";\nADD TACGROUPINNSSF: INDEX=6698, TACGROUPNAME=\"128-2C3248\", TACSTART=\"1272A8\", TACEND=\"1272BF\";\nADD TACGROUPINNSSF: INDEX=6699, TACGROUPNAME=\"128-2C3248\", TACSTART=\"12730C\", TACEND=\"127312\";\nADD TACGROUPINNSSF: INDEX=6700, TACGROUPNAME=\"128-2C3248\", TACSTART=\"127370\", TACEND=\"12737B\";\nEND
===========

{{
    "能力定义": "考察大模型生成代码以及MML的能力",
    "模板介绍": "这是一个关于代码\/MML生成-NL2MML-配置助理的模板",
    "模板正文": "你是系统工程师，需要根据参数写业务脚本\n\n下面是一个例子：\n参数:{{param_example}}\n业务脚本:{{script_example}}\n\n根据参数，严格按例子中业务脚本格式，以START开始END结束，写业务脚本\n参数：{{param_question}}",
    "字段解释": "param_example: 参数示例；script_example: 业务脚本示例；param_question: 参数问题""
}}


只返回json，不要包含其他内容。

题目类别：{category}
====题目====
{question}
====答案====
{answer}
===========
"""

def extract_template(question, answer, category, llm):
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import JsonOutputParser
    from langchain_core.exceptions import OutputParserException
    prompt_template = PromptTemplate(template=prompt, input_variables=["category", "question", "answer"])
    chain = prompt_template | llm | JsonOutputParser()
    try:
        result = chain.invoke({"category": category, "question": question, "answer": answer})
    except OutputParserException as err:
        result = err.llm_output
    return result

def load_questions():
    demo_file = "/home/junetheriver/datasets/huawei/raw/模型十大能力用例-demo.json"
    with open(demo_file, 'r') as f:
        data = json.load(f)
    return data

def main():
    llm = get_azure_model()
    questions = load_questions()
    templates = []
    from tqdm import tqdm
    for q in tqdm(questions):
        result = extract_template(q['Question'], q['Answer'], q['Category'], llm)
        if isinstance(result, dict):
            result['category'] = q['Category']
        else:
            result = {'category': q['Category'], 'output': result}
        templates.append(result)

        # 增量保存到文件中
        with open("templates.jsonl", 'at+') as f:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')

    with open("templates.json", 'w') as f:
        json.dump(templates, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()