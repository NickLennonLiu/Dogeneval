# 查询对端NF服务实例的回调信息（LST PNFSRVNTFSUBS）

  * 命令功能
  * 注意事项
  * 参数说明
  * 使用实例
  * 输出结果说明



## 命令功能

**适用NF：AMF、SMF、NSSF、SMSF、NCG**

该命令用于查询本地配置的对端NF实例支持的服务实例回调信息。

## 注意事项

无

#### 操作用户权限

G_1，管理员级别命令组；G_2，操作员级别命令组；G_3，用户级别命令组

## 参数说明

参数标识 | 参数名称 | 参数说明  
---|---|---  
NFINSTANCEID | NF实例标识 |  可选必选说明：可选参数 参数含义：该参数用于指定NF实例标识。 数据来源：全网规划 取值范围：字符串类型，输入长度范围是0~50。NFINSTANCEID参数建议满足以下约束规则：1.如果输入为uuid格式（格式例如：a6a61c6f-0d3a-4221-b1da-424eda3ccf67）只能为A-F、a-f、0-9的字符。2.如果输入不为uuid格式，长度不能超过18且不允许输入只包含0-9和“.”的字符串，例如：1.2.3.4、不允许输入只包含十六进制数（A-F、a-f、0-9）和“:”的字符串，例如：1::2、FBFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF。 默认值：无 配置原则： 本参数取值与ADD PNFPROFILE命令中的“NF实例标识”参数取值保持一致时，关联关系生效。  
SRVINSTANCEID | 服务实例标识 |  可选必选说明：可选参数 参数含义：该参数用于指定服务实例标识。 数据来源：全网规划 取值范围：字符串类型，输入长度范围是0~50。 默认值：无 配置原则：无  
NTFICATIONTYPE | 回调URI通知类型 |  可选必选说明：可选参数 参数含义：该参数用于指定回调URI通知类型。 数据来源：全网规划 取值范围：
  * “NtfTypeINVALID（NtfTypeINVALID）”：NtfTypeINVALID
  * “N1Msg（N1Msg）”：N1Msg
  * “N2Info（N2Info）”：N2Info
  * “LocNty（Loc_Nty）”：Loc_Nty
  * “DataRmvNtf（DataRmvNtf）”：DataRmvNtf
  * “DataChgNtf（DataChgNtf）”：DataChgNtf
  * “NtfTypeMAX（NtfTypeMAX）”：NtfTypeMAX

默认值：无 配置原则：无  
CALLBACKURI | 回调URI |  可选必选说明：可选参数 参数含义：该参数用于指定回调URI。 数据来源：全网规划 取值范围：字符串类型，输入长度范围是0~1024。 默认值：无 配置原则：无  
N1MESSAGECLASS | N1消息类别 |  可选必选说明：可选参数 参数含义：该参数用于指定N1消息类别。 数据来源：全网规划 取值范围：

  * “EN1MsgINVALID（EN1MsgINVALID）”：EN1MsgINVALID
  * “N1Mm（N1Mm）”：N1Mm
  * “N1Sm（N1Sm）”：N1Sm
  * “Lpp（Lpp）”：Lpp
  * “Sms（Sms）”：Sms
  * “N1Updp（N1Updp）”：N1Updp
  * “N1Reserved1（N1Reserved1）”：N1Reserved1
  * “EN1MsgMAX（EN1MsgMAX）”：EN1MsgMAX

默认值：无 配置原则：无  
N2INFOCLASS | N2消息类别 |  可选必选说明：可选参数 参数含义：该参数用于指定N2消息类别。 数据来源：全网规划 取值范围：

  * “EN2MsgINVALID（EN2MsgINVALID）”：EN2MsgINVALID
  * “N2Sm（N2Sm）”：N2Sm
  * “Nrppa（Nrppa）”：Nrppa
  * “Pws（Pws）”：Pws
  * “PwsBcal（PwsBcal）”：PwsBcal
  * “PwsRf（PwsRf）”：PwsRf
  * “N2Ran（N2Ran）”：N2Ran
  * “N2Reserved1（N2Reserved1）”：N2Reserved1
  * “EN2MsgMAX（EN2MsgMAX）”：EN2MsgMAX

默认值：无 配置原则：无  
  
## 使用实例

查询对端NF的服务实例回调信息，NF实例标识为AMF_Instance_1，服务实例标识为Service_Instance_0，通知类型为N1Msg。
    
    
    %%LST PNFSRVNTFSUBS:;%%
    RETCODE = 0 操作成功
    
    结果如下
    ------------------------
         NF实例标识 = AMF_Instance_1
       服务实例标识 = Service_Instance_0
    回调URI通知类型 = N1Msg
            回调URI = http://192.168.217.1:5080/ngmlc-loc/hgmlc/v1/provide-location
         N1消息类别 = EN1MsgINVALID
         N2消息类别 = EN2MsgINVALID
    （结果个数 = 1）
    
    ----    END

## 输出结果说明

输出项名称 | 输出项解释  
---|---  
NF实例标识 | 该参数用于指定NF实例标识。  
服务实例标识 | 该参数用于指定服务实例标识。  
回调URI通知类型 | 该参数用于指定回调URI通知类型。  
回调URI | 该参数用于指定回调URI。  
N1消息类别 | 该参数用于指定N1消息类别。  
N2消息类别 | 该参数用于指定N2消息类别。  
  



