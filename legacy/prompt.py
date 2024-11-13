import re, json

def get_example_prompt(examples):
    return '\n'.join([
        f"""Question: {example['Question']}\n\nAnswer: {example['Answer']}"""
        for example in examples
    ])

def get_prompt(content: dict, 
               doc_name: str,
               category: str, 
               examples: list, 
               example_cnt: int = 1):
    # main prompt
    prompt = f"""你需要根据给定语料生成通信领域大模型的评测集题目。

语料位于文档{doc_name}的{content['path']}路径下。

===========================================================================
【语料内容】开始
===========================================================================
{content['content']}
===========================================================================
【语料内容】结束
===========================================================================
【题目样例】开始
===========================================================================
{get_example_prompt(examples[:example_cnt])}
===========================================================================
【题目样例】结束
===========================================================================

现在，请你以问答对的形式，针对上面的语料内容以及题目样例，构建出一个测试模型{category}能力的问答对。

问题需要与类别结合，并尽可能根据上下文完整描述完整问题背景，回答需要能够完整地回答问题且不要篡改内容。

问题应当是self-contain且有意义的，不需要结合语料即可单独回答，错误问题示例：告警是什么级别的？告警的名字是什么？这个告警如何处理？。正确问题示例：发生在核心网部件中的名为503的告警的处置流程是什么？发生在核心网的告警10052应该如何处理？

如果该语料非常不完整（如语料中缺少关键的图表描述，或语料不完整），则直接输出空json字典。

以json格式输出。请直接输出json的内容，不要带markdown格式：
"""

    return prompt

def get_prompts(contents, doc_name, category, examples, example_cnt=1):
    prompts = []
    for content in contents:
        prompts.append({
            'prompt': get_prompt(content, doc_name, category, examples, example_cnt),
            'path': content['path'],
            'filename': content['filename'],
        })
    return prompts

if __name__ == "__main__":
    pass