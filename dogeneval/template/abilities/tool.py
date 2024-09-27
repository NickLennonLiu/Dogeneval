data = {
    "name": "工具选择",
    "definition": "工具使用能力指的是系统能够根据用户的问题和工具的描述，选择适当的工具来解决问题。该能力要求系统理解用户的需求，熟悉各种工具的功能，并在解决问题时灵活应用这些工具，从而高效地完成任务。",
    "template": "你可以调用各种用户自定义的工具来解决用户问题。你的任务是根据<工具描述>解决<用户问题>。\n<工具描述>:\n{tools_description}\n<用户问题>:\n{user_question}",
    "fields": [
        {
            "name": "tools_description",
            "type": "list",
            "description": "一个列表描述可使用的工具信息"
        },
        {
            "name": "user_question",
            "type": "string",
            "description": "用户的问题描述"
        }
    ],
    "examples": [
        {"question": """你可以调用各种用户自定义的工具来解决用户问题。你的任务是根据<工具描述>解决<用户问题>
<工具描述>：
{""name"": ""DSP_PAENODE"", ""description"": ""通过微服务实例名称获取微服务所在POD的名称."", ""arguments"": {""meid"": ""String 网元ID"", ""cellinstance"": ""String 微服务实例名称""}, ""results"": ""微服务相关信息""}
{""name"": ""GetInstanceIdByAlarm"", ""description"": ""根据告警ID获取微服务实例ID.  请在用户的问题需要检索定位根因时，调用该工具根据告警ID获取微服务实例名称以便进一步分析，如\'网元上报了xx告警，请分析告警上报的原因\'."", ""arguments"": {""alarmId"": ""String 告警ID""}, ""results"": ""String 告警相关信息，包括微服务实例号、端口名称""}
{""name"": ""DSP_POD"", ""description"": ""通过POD名称获取该POD所在NODE的名称. "", ""arguments"": {""meid"": ""String 网元ID"", ""podName"": ""String POD名称""}, ""results"": ""POD相关信息""}
{""name"": ""DSP_NODE"", ""description"": ""通过NODE名称获取该NODE所在主机的名称. "", ""arguments"": {""meid"": ""String 网元ID"", ""nodeName"": ""String NODE名称""}, ""results"": ""NODE相关信息""}
{""name"": ""GetPhysicSwitchName"", ""description"": ""通过主机名称获取该主机所连接物理交换机的名称. "", ""arguments"": {""hostName"": ""String 主机名称""}, ""results"": ""String 物理交换机名称""}
{""name"": ""DSP_MSSPORTPMDDRV"", ""description"": ""获取端口PMD驱动的丢包信息. "", ""arguments"": {""meid"": ""String 网元ID"", ""celltype"": ""String 微服务类型"", ""cellinstance"": ""String 微服务实例名称"", ""portname"": ""String 端口名称""}, ""results"": ""端口PMD驱动的丢包信息""}
{""name"": ""GetPhysicSwitchDiscard"", ""description"": ""获取物理交换机的丢包信息. "", ""arguments"": {""switchName"": ""String 物理交换机名称""}, ""results"": ""String 物理交换机的丢包信息""}
{""name"": ""GetVswitchDiscard"", ""description"": ""获取虚拟交换机的丢包信息. "", ""arguments"": {""hostName"": ""String 主机名称""}, ""results"": ""String 虚拟交换机的丢包信息""}
{""name"": ""GetPhysicNicDiscard"", ""description"": ""获取物理网卡的丢包信息. "", ""arguments"": {""hostName"": ""String 主机名称""}, ""results"": ""String 物理网卡的丢包信息""}
{""name"": ""DSP_PAEDISCARD"", ""description"": ""获取微服务实例所在POD的丢包信息. 在获取POD名称、NODE名称、主机名称和物理交换机名称后，查询微服务实例所在POD的丢包信息时调用此工具."", ""arguments"": {""meid"": ""String 网元ID"", ""celltype"": ""String 微服务类型"", ""cellinstance"": ""String 微服务实例名称""}, ""results"": ""微服务丢包信息""}
{""name"": ""Final Answer"", ""description"": ""回答用户的问题"", ""arguments"": {""final_answer"": ""String 答案内容""}}

<用户问题>:
使用GetInstanceIdByAlarm工具，根据告警ID(100340)获取微服务实例ID，并按照JSON格式输出<用户问题>对应参数的结果""",
        "answer": """ """}
    ]
}