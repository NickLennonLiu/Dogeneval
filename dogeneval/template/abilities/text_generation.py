data = {
    "name": "文本生成",
    "definition": "文本生成能力指的是系统能够根据输入的文本描述或要求，生成符合指定格式、内容和结构的文本输出。该能力要求系统理解输入内容的语义，并按照预定义的模板或规则，输出逻辑清晰、结构化的文本，如将自然语言描述转换为特定格式的JSON文本。",
    "template": "【任务要求】\n在这个任务中，你是一个核心网专家，现在有一段关于核心网MML命令配置的文本描述，每个step内由命令意图、命令内容及其参数解释三部分组成，参数解释中清晰地定义步骤间跳转逻辑和部分参数取值来源。\n你的目标是将给定的文本描述按照step拆解出来，并转换成json格式输出，json格式要求[{{\"node id\":\"\",\"node name\":\"\",\"MML\":\"\",\"description\":\"\",\"next id1\":\"\",\"condition1\":\"\",\"next id2\":\"\",\"condition2\":\"\"}}]。【你的任务】：\n现在请开始回答问题：\n你的目标是将给定的文本描述按照step拆解出来，并转换成json格式的输出，形如[{{\"node id\":\"\",\"node name\":\"\",\"MML\":\"\",\"description\":\"\",\"next id1\":\"\",\"condition1\":\"\",\"next id2\":\"\",\"condition2\":\"\"}}]。必须严格按照上述格式输出json文本。\n关于核心网MML命令配置的文本描述1为：\n\n    {text_question}",
    "fields": [
        {
            "name": "text_question",
            "type": "string",
            "description": "需要生成流程模板的文本问题"
        }
    ],
    "examples": [
        {"question": """************************************************************
【任务要求】
在这个任务中，你是一个核心网专家，现在有一段关于核心网MML命令配置的文本描述，每个step内由命令意图、命令内容及其参数解释三部分组成，参数解释中清晰地定义步骤间跳转逻辑和部分参数取值来源。
你的目标是将给定的文本描述按照step拆解出来，并转换成json格式输出，json格式要求[{"node id":"","node name":"","MML":"","description":"","next id1":"","condition1":"","next id2":"","condition2":""}]。
请仔细遵循以下更新和澄清的指示：
    1.文本解析与命令识别：仔细识别每一条MML命令及其后续参数取值解释。确保理解每个参数的含义及其预期来源（例如，工单中的特定字段）。
    2.node id分配：每个步骤应分配一个唯一的node id，按照出现顺序递增。首个步骤从1开始，最大到100。
    3.node name构造：node name应为当前step中第二行中冒号前的命令，并把空格替换为_。例如，输入'ADD L3VPNINST：aa,sd;'，转换成输出{"node name":"ADD_L3VPNINST"}。
    4.MML构造：MML应当直接采用当前step中第二行的整条命令，以';'结束。
    5.description撰写：description字段应直接采用每个步骤前的意图描述，去除注释符号（如//step），仅仅保留意图内容，并保持语句通顺、完整。
    6.next id1与condition1,next id2与condition2构造逻辑：除非文本明确指出基于特定条件跳转至不同步骤，否则默认情况下，每个步骤的next id1为当前node id加一，其中只有最后一个step直接指向end-node，对应condition1字段为''，其中只有最后一个step直接指向end-node，对应condition1字段为''。
      若存在条件分支，请明确指出判断逻辑及所依赖的变量状态，并把结果储存在{$判断条件}变量中，条件满足时的condition1为{$判断条件}，对应的next id1为跳转的step编号；条件不满足时的condition2为!{$判断条件}，对应的next id2为下一步的step编号。
      条件表达式应直接反映文本描述中的逻辑，如“如果VRFNAME已经在系统中存在，则跳过创建步骤”。注意，文本中未明确提到的条件不应假设存在。
    7.参数处理：文本中提及的参数及其来源（如“工单中‘VPN名称’”）应被视为静态描述，不直接体现在流程模板中作为条件判断。但需确保模型理解这些参数的用途，并在描述中适当反映其意义。
    8.json格式：确保一段文本描述生成的json严格以[start]开头，以[end]结尾，且每一步骤格式正确无遗漏。
        
************************************************************
这里有几个例子供你学习：
  
        【待生成流程模板的文本样例】：待生成流程模板的文本样例：其中//后面表示该step的意图描述
            //step1：检查现网INDEX使用情况以及切片是否已存在
            LST AMFSETID;
            记录现网情况，使用的index应小于1000，1000以上为自动化平台下发;如果参数index存在，请跳转step3

            //step2:配置网络配置的NSSAI。
            ADD CFGSNSSAI:INDEX=139, MCC="460",MNC="00", SST=128, SD="2C7155", DESC="128-2C7155", ISACTIVE=TRUE;
            参数VRFNAME，名称为VPN实例名称，取值为工单中“VPN名称”;参数VRFRD，名称为路由标识，取值为工单中“L3VPNVRFRD”;

            //step3：配置一个支持相同SST/SD的TACGROUP
            ADD TACGROUPINNSSF:INDEX=2255, TACGROUPNAME="128-2C7155", TACSTART="123068", TACEND="123068";
            参数TACGROUPNAME，名称为路由标识，取值为工单中“L3VPNVRFRD”;
        【结果】：
            [start]
            [
            {"node id": 1 ,"node name": "LST_AMFSETID,"MML": "LST AMFSETID;","description": "检查现网INDEX使用情况以及切片是否已存在", "next id1": "3","condition1": "{$is_index}","next id2": "2","condition2": "!{$is_index}"},
            {"node id": 2 ,"node name": "ADD_CFGSNSSAI,"MML": "ADD CFGSNSSAI: INDEX=139, MCC=\"460\",MNC=\"00\", SST=128, SD=\"2C7155\", DESC=\"128-2C7155\", ISACTIVE=TRUE;", "description": "配置网络配置的NSSAI。","next id1": "3", "condition1":"","next id2": "","condition2":""},
            {"node id": 3 ,"node name": "ADD_TACGROUPINNSSF,"MML": "ADD TACGROUPINNSSF: "INDEX=2255, TACGROUPNAME=\"128-2C7155\", TACSTART=\"123068\", TACEND=\"123068\";","description": "配置一个支持相同SST/SD的TACGROUP", "next id1": "end-node","condition1":"","next id2": "","condition2":""}
            ]
            [end]         
************************************************************
【你的任务】：
现在请开始回答问题：
你的目标是将给定的文本描述按照step拆解出来，并转换成json格式的输出，形如[{"node id":"","node name":"","MML":"","description":"","next id1":"","condition1":"","next id2":"","condition2":""}]。必须严格按照上述格式输出json文本。
关于核心网MML命令配置的文本描述1为：

    //step1:配置用户面Profile实例。
    ADD PNFPROFILE:NFINSTANCEID="UPF_Instance_0", NFTYPE=NfUPF, NFSTATUS=Registered, FQDN="upf00.node.mnc003.mcc123.3gppnetwork.org", IPADDRESSTYPE=IPTypeV4, IPV4ADDRESS1="192.168.126.11", PORT=8080;
    参数NFINSTANCEID，名称为NF实例标识，取值：工单中“NF ID”;参数FQDN，名称为域名，取值：工单中“域名”;参数IPV4ADDRESS1，名称为IPV4地址1，取值：工单中“IP”;参数PORT，名称为端口号，取值：工单中“端口号”;
    //step2:配置用户面节点支持的切片。
    ADD PNFNS: INDEX=3, NFINSTANCEID="UPF_Instance_0", SST=1, SD="000001";
    参数NFINSTANCEID，名称为NF实例标识，取值：工单中“NF ID”;参数SD，名称为切片分类器，取值：工单中“切片业务标识”的'-'后面部分，如128-4C7013，取4C7013;
    //step3:配置用户面节点支持的DNN信息。
    ADD PNFDNN:INDEX=5, NFINSTANCEID="UPF_Instance_0", DNN="APN1", PNFNSINDEX=3;
    参数NFINSTANCEID，名称为NF实例标识，取值：工单中“NF ID”;
    //step4:配置用户面节点的位置特征和分流能力。
    ADD UPNODE:NFINSTANCENAME="UPF_Instance_0", LOCATION=Central, UPFUNCTION=None, LOCK=FALSE, VPNNAME="VRF_CP";
    参数NFINSTANCENAME，名称为UPF实例名称，取值：工单中“UPF名称”;参数VPNNAME，名称为VPN实例名称，取值：工单中“VPN名称”;
    //step5:配置用户面节点的位置区信息
    ADD UPAREA:AREANAME="UPAREA1", AREATYPE=N2TAI;
    参数AREANAME，名称为UPF服务区名称，取值：工单中“服务区名称”;
    //step6:将位置区与TAI绑定。
    ADD UPAREABINDN2TAI:AREANAME="UPAREA1", N2BEGINTAI="12301000001", N2ENDTAI="12301123456";
    参数AREANAME，名称为UPF服务区名称，取值：工单中“服务区名称”;参数N2BEGINTAI，名称为UPF服务区名称支持的5G TAI范围的起始值，取值：工单中“TAI范围起始值”;参数N2ENDTAI，名称为UPF服务区名称支持的5G TAI范围的结束值，取值：工单中“TAI范围结束值”;
    //step7:配置用户面节点支持的为SMF提供服务区域的信息。
    ADD PNFSMFSERAREA:NFINSTANCEID="UPF_Instance_0", SMFSERVINGAREA="UPAREA1";
    参数NFINSTANCEID，名称为NF实例标识，取值：工单中“NF ID”;
    //step8:配置用户面与EPS的互通以及支持的PDU会话类型。
    ADD PNFUPFINFO: NFINSTANCEID="UPF_Instance_0", IWKEPSIND=TRUE, PDUSESSIONTYPE=IPV4-1&IPV6-1&IPV4V6-1&UNSTRUCTURED-1&ETHERNET-1;
    参数NFINSTANCEID，名称为NF实例标识，取值：工单中“NF ID”;
    //step9:配置SMF到UPF的心跳探测并开启故障场景下去活该UPF上用户会话的功能。
    SET PFCPPARA: HBINTERVAL=30,HBT1=3,HBN1=5,DEACTIVEFLAG=ENABLE,DACTINTERVAL=900;
    
    //step10:配置故障场景下对用户会话的去活速率。
    SET DEACTIVERATE: RATE=1000;
""",
        "answer": """[start]
[
{"node id": 1, "node name": "ADD_PNFPROFILE", "MML": "ADD PNFPROFILE:NFINSTANCEID="UPF_Instance_0", NFTYPE=NfUPF, NFSTATUS=Registered, FQDN="upf00.node.mnc003.mcc123.3gppnetwork.org", IPADDRESSTYPE=IPTypeV4, IPV4ADDRESS1="192.168.126.11", PORT=8080;", "description": "配置用户面Profile实例。", "next id1": "2", "condition1": "", "next id2": "", "condition2": ""}, 
{"node id": 2, "node name": "ADD_PNFNS", "MML": "ADD PNFNS: INDEX=3, NFINSTANCEID="UPF_Instance_0", SST=1, SD="000001";", "description": "配置用户面节点支持的切片。", "next id1": "3", "condition1": "", "next id2": "", "condition2": ""}, 
{"node id": 3, "node name": "ADD_PNFDNN", "MML": "ADD PNFDNN:INDEX=5, NFINSTANCEID="UPF_Instance_0", DNN="APN1", PNFNSINDEX=3;", "description": "配置用户面节点支持的DNN信息。", "next id1": "4", "condition1": "", "next id2": "", "condition2": ""}, 
{"node id": 4, "node name": "ADD_UPNODE", "MML": "ADD UPNODE:NFINSTANCENAME="UPF_Instance_0", LOCATION=Central, UPFUNCTION=None, LOCK=FALSE, VPNNAME="VRF_CP";", "description": "配置用户面节点的位置特征和分流能力。", "next id1": "5", "condition1": "", "next id2": "", "condition2": ""}, 
{"node id": 5, "node name": "ADD_UPAREA", "MML": "ADD UPAREA:AREANAME="UPAREA1", AREATYPE=N2TAI;", "description": "配置用户面节点的位置区信息", "next id1": "6", "condition1": "", "next id2": "", "condition2": ""}, 
{"node id": 6, "node name": "ADD_UPAREABINDN2TAI", "MML": "ADD UPAREABINDN2TAI:AREANAME="UPAREA1", N2BEGINTAI="12301000001", N2ENDTAI="12301123456";", "description": "将位置区与TAI绑定。", "next id1": "7", "condition1": "", "next id2": "", "condition2": ""}, 
{"node id": 7, "node name": "ADD_PNFSMFSERAREA", "MML": "ADD PNFSMFSERAREA:NFINSTANCEID="UPF_Instance_0", SMFSERVINGAREA="UPAREA1";", "description": "配置用户面节点支持的为SMF提供服务区域的信息。", "next id1": "8", "condition1": "", "next id2": "", "condition2": ""}, 
{"node id": 8, "node name": "ADD_PNFUPFINFO", "MML": "ADD PNFUPFINFO: NFINSTANCEID="UPF_Instance_0", IWKEPSIND=TRUE, PDUSESSIONTYPE=IPV4-1&IPV6-1&IPV4V6-1&UNSTRUCTURED-1&ETHERNET-1;", "description": "配置用户面与EPS的互通以及支持的PDU会话类型。", "next id1": "9", "condition1": "", "next id2": "", "condition2": ""}, 
{"node id": 9, "node name": "SET_PFCPPARA", "MML": "SET PFCPPARA: HBINTERVAL=30,HBT1=3,HBN1=5,DEACTIVEFLAG=ENABLE,DACTINTERVAL=900;", "description": "配置SMF到UPF的心跳探测并开启故障场景下去活该UPF上用户会话的功能。", "next id1": "10", "condition1": "", "next id2": "", "condition2": ""}, 
{"node id": 10, "node name": "SET_DEACTIVERATE", "MML": "SET DEACTIVERATE: RATE=1000;", "description": "配置故障场景下对用户会话的去活速率。", "next id1": "end-node", "condition1": "", "next id2": "", "condition2": ""}
]
[end]"""}
    ]
}