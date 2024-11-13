task_ability_dt = {
    "LogicAnalysis": "逻辑推理",
    "InformationExtraction": "语义理解",
    "TextSummary": "语义理解",
    "QuestionAnswering": "知识储备",
    "ReadingComprehension": "文本生成",
    "MultipleChoice": "知识储备",
    "MMLGenerate": "代码/MML生成",
    "TextClassification": "语义理解",
    "JsonFormat": "格式遵从",
    "NextStepSelection": "任务规划",
    "ParamRegex": "格式遵从",
    "ParamExtract": "格式遵从",
    "IssueRewrite": "文本生成",
    "ToolSelection": "工具使用",
    "AlarmCheck": "任务规划",
    "MathCalculation": "数学计算"
}

task_abbr_dt = {
    "LogicAnalysis": "逻辑推理",
    "InformationExtraction": "信息提取",
    "TextSummary": "文本摘要",
    "QuestionAnswering": "问答题",
    "ReadingComprehension": "阅读理解",
    "MultipleChoice": "选择题",
    "MMLGenerate": "NL2MML",
    "TextClassification": "工单分类",
    "JsonFormat": "Json格式",
    "NextStepSelection": "任务规划",
    "ParamRegex": "参数正则化",
    "ParamExtract": "参数提取",
    "IssueRewrite": "工单改写",
    "ToolSelection": "工具使用",
    "AlarmCheck": "告警检查",
    "MathCalculation": "数学计算"
}

qa_col_name_zh_dt = {
    "ability": "能力",  
    "task": "任务",
    "Question": "题目",
    "Answer": "答案",
    "explanation": "解题思路",
    "match": "答案匹配情况",
    "match_reason": "匹配原因",
    "kp_type": "知识点类型",
    "kp_title": "知识点标题",
    "kp_content": "知识点内容",
    "kp_path": "知识点路径",
    "template": "模板",
    "is_zeroshot": "是否零样本",
    "require_scene": "是否需要场景",
    "example": "示例",
    "quality_score": "质量评分",
    "quality_reason": "质量评分原因",
    "Model_Answer": "模型答案",
    "error": "错误信息",
    "qa_gen_response": "原始输出内容",
    "qa_gen_time": "生成时间"
    }

export_order = [
    "ability",
    "task",
    "Question",
    "Model_Answer",
    "explanation",
    "kp_type",
    "kp_title",
    "kp_content",
    "kp_path",
]

def task_to_ability(df):
    return df['task'].apply(lambda x: task_ability_dt[x])

def task_to_abbr(df):
    return df['task'].apply(lambda x: task_abbr_dt[x])

def df_col_rename(df):
    return df.rename(columns=qa_col_name_zh_dt, errors="ignore")