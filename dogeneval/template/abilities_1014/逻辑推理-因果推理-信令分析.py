full_template = '你的任务是严格按照推理规则给出分析结果和下一步,推导过程尽量简要。\n\n分析线索：{clue}\n业务知识：{business_knowledge}\n推理规则：{inference_rule}\n\n你需要按照格式回答，根据推理规则中规定的内容填写，回答格式如下：\n推导过程：\n分析结果：\n下一步：\n\n输出格式为json格式'
fields = [{'name': 'clue', 'description': '需要进行分析的线索'}, {'name': 'business_knowledge', 'description': '与问题相关的业务知识'}, {'name': 'inference_rule', 'description': '进行推理的规则'}]
examples = [{'Category': '逻辑推理-因果推理-信令分析', 'Level1': '逻辑推理', 'Level2': '因果推理', 'Field': '信令分析', 'Question': "分析线索：\n'时间':2024-03-01 14:33:14.965,'消息名称':PAGING失败,'方向':AMF发送到10.134.34.73\n'时间':2024-03-01 14:33:15.175,'消息名称':INVITE,'方向':ATS发送到S-CSCF\n'时间':2024-03-01 14:33:15.37,'消息名称':100 TRYING,'方向':S-CSCF发送到ATS\n'时间':2024-03-01 14:33:17.903,'消息名称':PAGING失败,'方向':AMF发送到RAN\n'时间':2024-03-01 14:33:20.92,'消息名称':PAGING失败,'方向':AMF发送到RAN\n'时间':2024-03-01 14:33:23.831,'消息名称':PAGING失败,'方向':AMF发送到RAN\n'时间':2024-03-01 14:33:25.162,'消息名称':CANCEL,'方向':ATS发送到S-CSCF,'携带':Reason原因码 18：No user responding\n'时间':2024-03-01 14:33:25.167,'消息名称':200 OK (CANCEL),'方向':S-CSCF发送到ATS\n\n业务知识：\n无\n\n推理规则：\n判断分析线索中，CANCEL之前是否有消息名称是Paging的消息。\n如果有Paging消息，提取最早的Paging消息。在“分析结果”中填写最早的Paging消息，格式为{'时间'：'','消息名称':'','方向':'','携带':''}。在“下一步”填写“分析发送该消息的原因”。\n如果没有Paging消息，在“分析结果”中填写“根因是被叫长时间未回180(Ringing)振铃消息导致主叫主动挂机，呼叫拆线，建议被叫侧排查终端或无线信号问题”。在“下一步”填写“结束”。\n\n你现在的任务是严格按照推理规则给出分析结果和下一步,推导过程尽量简要。\n你需要按照格式回答，根据推理规则中规定的内容填写，回答格式如下：\n推导过程：\n分析结果：\n下一步：", 'Answer': "推导过程：\n根据分析线索，发现有多个PAGING失败的消息，且这些消息的方向都是AMF发送到RAN或10.134.34.73。根据推理规则，需要提取最早的Paging消息。\n\n分析结果：\n{'时间':'2024-03-01 14:33:14.965','消息名称':'PAGING失败','方向':'AMF发送到10.134.34.73','携带':''}\n\n下一步：分析发送该消息的原因"}, {'Category': '逻辑推理-因果推理-信令分析', 'Level1': '逻辑推理', 'Level2': '因果推理', 'Field': '信令分析', 'Question': "分析线索：\n'时间':2024-02-29 10:03:44.23,'消息名称':INVITE,'方向':UE/MS发送到SGW\n'时间':2024-02-29 10:03:44.232,'消息名称':100 TRYING,'方向':SGW发送到UE/MS\n'时间':2024-02-29 10:03:45.007,'消息名称':PAGING失败,'方向':AMF发送到RAN\n'时间':2024-02-29 10:03:48.008,'消息名称':PAGING失败,'方向':AMF发送到RAN\n'时间':2024-02-29 10:03:51.006,'消息名称':PAGING失败,'方向':AMF发送到RAN\n'时间':2024-02-29 10:03:55.421,'消息名称':183 SESSION PROGRESS,'方向':SGW发送到UE/MS\n'时间':2024-02-29 10:03:55.47,'消息名称':PRACK,'方向':UE/MS发送到SGW\n'时间':2024-02-29 10:03:55.734,'消息名称':200 OK (PRACK),'方向':SGW发送到UE/MS\n'时间':2024-02-29 10:03:55.794,'消息名称':UPDATE,'方向':UE/MS发送到SGW\n'时间':2024-02-29 10:03:56.132,'消息名称':200 OK (UPDATE),'方向':SGW发送到UE/MS\n'时间':2024-02-29 10:04:04.864,'消息名称':181 CALL IS BEING FORWARDED,'方向':SGW发送到UE/MS\n'时间':2024-02-29 10:04:05.406,'消息名称':PAGING失败,'方向':AMF发送到RAN\n'时间':2024-02-29 10:04:05.806,'消息名称':183 SESSION PROGRESS,'方向':SGW发送到UE/MS,'携带':Reason原因码 18：No user responding\n'时间':2024-02-29 10:04:05.877,'消息名称':PRACK,'方向':UE/MS发送到SGW\n'时间':2024-02-29 10:04:06.124,'消息名称':200 OK (PRACK),'方向':SGW发送到UE/MS\n'时间':2024-02-29 10:04:08.408,'消息名称':PAGING失败,'方向':AMF发送到RAN\n'时间':2024-02-29 10:04:10.301,'消息名称':CANCEL,'方向':UE/MS发送到SGW\n'时间':2024-02-29 10:04:10.302,'消息名称':200 OK (CANCEL),'方向':SGW发送到UE/MS\n'时间':2024-02-29 10:04:10.339,'消息名称':487 REQUEST TERMINATED(Cause:487),'方向':SGW发送到UE/MS\n'时间':2024-02-29 10:04:10.366,'消息名称':ACK,'方向':UE/MS发送到SGW\n\n业务知识：\nCANCEL的含义是终止一个正在进行的会话\n\n推理规则：\n判断时间在CANCEL之前是否有消息名称是180 RINGING的消息。\n如果时间在CANCEL之前有180 RINGING消息，在“分析结果“中填写“有180 RINGING消息”，在“下一步”中填写“排查前序消息中是否存在携带原因码的18X消息”。\n如果时间在CANCEL之前没有180 RINGING消息，在”分析结果”填写“没有180 RINGING消息”，在”下一步“中填写“排查是否存在 180 RINGING超时情况”\n\n你现在的任务是严格按照推理规则给出分析结果和下一步,推导过程尽量简要。\n你需要按照格式回答，根据推理规则中规定的内容填写，回答格式如下：\n推导过程：\n分析结果：\n下一步：", 'Answer': '推导过程：\n根据提供的信令流程，检查时间在CANCEL之前的消息，未找到180 RINGING消息。\n\n分析结果：\n没有180 RINGING消息\n\n下一步：\n排查是否存在 180 RINGING超时情况'}, {'Category': '逻辑推理-因果推理-信令分析', 'Level1': '逻辑推理', 'Level2': '因果推理', 'Field': '信令分析', 'Question': "分析线索：\n'时间':2024-02-29 10:03:44.23,'消息名称':INVITE,'方向':UE/MS发送到SGW\n'时间':2024-02-29 10:03:44.232,'消息名称':100 TRYING,'方向':SGW发送到UE/MS\n'时间':2024-02-29 10:03:45.007,'消息名称':PAGING失败,'方向':AMF发送到RAN\n'时间':2024-02-29 10:03:48.008,'消息名称':PAGING失败,'方向':AMF发送到RAN\n'时间':2024-02-29 10:03:51.006,'消息名称':PAGING失败,'方向':AMF发送到RAN\n'时间':2024-02-29 10:03:55.421,'消息名称':183 SESSION PROGRESS,'方向':SGW发送到UE/MS\n'时间':2024-02-29 10:03:55.47,'消息名称':PRACK,'方向':UE/MS发送到SGW\n'时间':2024-02-29 10:03:55.734,'消息名称':200 OK (PRACK),'方向':SGW发送到UE/MS\n'时间':2024-02-29 10:03:55.794,'消息名称':UPDATE,'方向':UE/MS发送到SGW\n'时间':2024-02-29 10:03:56.132,'消息名称':200 OK (UPDATE),'方向':SGW发送到UE/MS\n'时间':2024-02-29 10:04:04.864,'消息名称':181 CALL IS BEING FORWARDED,'方向':SGW发送到UE/MS\n'时间':2024-02-29 10:04:05.406,'消息名称':PAGING失败,'方向':AMF发送到RAN\n'时间':2024-02-29 10:04:05.806,'消息名称':183 SESSION PROGRESS,'方向':SGW发送到UE/MS,'携带':Reason原因码 18：No user responding\n'时间':2024-02-29 10:04:05.877,'消息名称':PRACK,'方向':UE/MS发送到SGW\n'时间':2024-02-29 10:04:06.124,'消息名称':200 OK (PRACK),'方向':SGW发送到UE/MS\n'时间':2024-02-29 10:04:08.408,'消息名称':PAGING失败,'方向':AMF发送到RAN\n'时间':2024-02-29 10:04:10.301,'消息名称':CANCEL,'方向':UE/MS发送到SGW\n'时间':2024-02-29 10:04:10.302,'消息名称':200 OK (CANCEL),'方向':SGW发送到UE/MS\n'时间':2024-02-29 10:04:10.339,'消息名称':487 REQUEST TERMINATED(Cause:487),'方向':SGW发送到UE/MS\n'时间':2024-02-29 10:04:10.366,'消息名称':ACK,'方向':UE/MS发送到SGW\n\n业务知识：\n无\n\n推理规则：\n判断分析线索中，CANCEL之前是否有消息名称是Paging的消息。\n如果有Paging消息，提取最早的Paging消息。在“分析结果”中填写最早的Paging消息，格式为{'时间'：'','消息名称':'','方向':'','携带':''}。在“下一步”填写“分析发送该消息的原因”。\n如果没有Paging消息，在“分析结果”中填写“根因是被叫长时间未回180(Ringing)振铃消息导致主叫主动挂机，呼叫拆线，建议被叫侧排查终端或无线信号问题”。在“下一步”填写“结束”。\n\n你现在的任务是严格按照推理规则给出分析结果和下一步,推导过程尽量简要。\n你需要按照格式回答，根据推理规则中规定的内容填写，回答格式如下：\n推导过程：\n分析结果：\n下一步：", 'Answer': "推导过程：\n根据分析线索，发现有多个Paging失败消息， earliest one is {'时间': '2024-02-29 10:03:45.007', '消息名称': 'PAGING失败', '方向': 'AMF发送到RAN'}。\n\n分析结果：\n{'时间': '2024-02-29 10:03:45.007', '消息名称': 'PAGING失败','方向': 'AMF发送到RAN,'携带':''}\n\n下一步：分析发送该消息的原因"}]
