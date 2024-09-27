data = {
    "name": "代码MML生成",
    "definition": "代码/MML生成能力指的是系统能够根据提供的参数或描述，自动生成符合特定格式和规范的代码或模型标记语言（MML）脚本的能力。该能力要求系统理解输入的参数，并基于既定的模板或示例，生成结构化且符合业务需求的脚本。",
    "template": "你是系统工程师，需要根据参数写业务脚本\n\n根据参数，严格按例子中业务脚本格式，以START开始END结束，写业务脚本\n参数：{param_question}",
    "fields": [
        {
            "name": "param_question",
            "type": "string",
            "description": "参数问题"
        }
    ],
    "examples": [
        {"question": """你是系统工程师，需要根据参数写业务脚本

下面是一个例子：
参数：
#步骤区域组索引：2255，2372；TACGROUP名称：128-XY7155；TAC区域段：12480A-12480E，121423-123068
业务脚本：
START
ADD TACGROUPINNSSF:INDEX=2255, TACGROUPNAME=""128-XY7155"", TACSTART=""12480A"", TACEND=""12480E"";
ADD TACGROUPINNSSF:INDEX=2372, TACGROUPNAME=""128-XY7155"", TACSTART=""121423"", TACEND=""123068"";
END

根据参数，严格按例子中业务脚本格式，以START开始END结束，写业务脚本
参数：
#步骤区域组索引：2435；TACGROUP名称：128-2C90A0；TAC区域段：123076-123076""",
        "answer": """START
ADD TACGROUPINNSSF:INDEX=2435, TACGROUPNAME=""128-2C90A0"", TACSTART=""123076"", TACEND=""123076"";
END"""}
    ]
}