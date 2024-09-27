data = {
    "name": "任务规划",
    "definition": "任务规划能力指的是系统能够根据输入的信息，分析任务要求并制定出实现目标的步骤和分支路径。该能力要求系统对任务逻辑进行推理，明确每个步骤的执行条件，并生成符合任务需求的计划或方案，确保任务能够按照预期流程顺利进行。",
    "template": "你的任务是根据所有步骤名、当前步骤描述和当前步骤用于选择下一步分支的参数，以JSON格式生成下一步的所有分支情况。当下一步为诊断结束时，action请选择endNode。\n现在请开始回答问题：\n已知所有步骤编号和步骤名为\n{step_name}\n已知当前步骤描述为{current_step_desc}\n已知当前步骤的输出为{current_step_output}\n请根据所有步骤名、当前步骤描述和当前步骤用于选择下一步分支的参数，以JSON格式生成下一步的所有分支情况。当下一步为诊断结束时，action请选择endNode。\n请先分析分支情况。你的输出应该为：",
    "fields": [
        {
            "name": "step_name",
            "type": "string",
            "description": "步骤列表，包含步骤编号和步骤名"
        },
        {
            "name": "current_step_desc",
            "type": "string",
            "description": "当前步骤描述"
        },
        {
            "name": "current_step_output",
            "type": "string",
            "description": "当前步骤的输出"
        }
    ],
    "examples": [
        {"question": """你的任务是根据所有步骤名、当前步骤描述和当前步骤用于选择下一步分支的参数，以JSON格式生成下一步的所有分支情况。当下一步为诊断结束时，action请选择endNode。
举例如下：
***********************************************************************************************************************
例1.
	已知所有步骤编号和步骤名为
		步骤1：QueryWeather
		步骤2：VehicleInfo
		步骤3：ShipInfo
		步骤4：StartOut
		步骤5：StayHome
		步骤6：QueryHappy
	已知当前步骤描述为“查询天气情况，是否为好天气。是=>步骤 3。否=>步骤 2。”。其中每个“=>”后的内容为步骤编号，前面给出的步骤名一一对应。
	已知当前步骤的输出为QueryWeatherResult，用于选择下一步分支的参数定义为{""isWeatherWell"": ""是否为好天气，取值范围{\""是\"",\""否\""}""}。
	请根据所有步骤名、当前步骤描述和当前步骤用于选择下一步分支的参数，以JSON格式生成下一步的所有分支情况。当下一步为诊断结束时，action请选择endNode。
	“是=>步骤 3。否=>步骤 2。”两个“=>”表示next数组中有2个值，因此回答中有两个conditon、action组合。
	你的输出应该为：
	```
	{
		""next"": [
			{
				""condition"": ""${QueryWeatherResult.isWeatherWell == \""是\""}"",
				""action"": ""ShipInfo""
			},
			{
				""condition"": ""${QueryWeatherResult.isWeatherWell == \""否\""}"",
				""action"": ""VehicleInfo""
			}
		]
	}
	```
例2.
	已知所有步骤编号和步骤名为
		步骤1：StartOut
		步骤2：StayHome
		步骤3：QueryHappy
		步骤4：EatFood
	已知当前步骤描述为 “查询游玩后的心情是否正常。是=>步骤4。否=>告警将自动恢复，诊断结束。”。其中每个“=>”后的内容为步骤编号，前面给出的步骤名一一对应。
	已知当前步骤的输出为QueryHappyResult，用于选择下一步分支的参数定义为{""isHappy"": ""心情是否好，取值范围{\""正常\""，\""异常\""}""}。
	请根据所有步骤名、当前步骤描述和当前步骤用于选择下一步分支的参数，以JSON格式生成下一步的所有分支情况。当下一步为诊断结束时，action请选择endNode。
	“是=>步骤4。否=>诊断成功，任务结束。”两个“=>”表示next数组中有2个值，因此回答中有两个conditon、action组合。
	你的输出应该为：
	```
	{
		""next"": [
			{
				""condition"": ""${QueryHappyResult.isHappy == \""正常\""}"",
				""action"": ""EatFood""
			},
			{
				""condition"": ""${QueryHappyResult.isHappy == \""异常\""}"",
				""action"": ""endNode""
			}
		]
	}
	```
例3.
	已知所有步骤编号和步骤名为
		步骤1：StartOut
		步骤2：StayHome
		步骤3：QueryHappy
		步骤4：EatFood
	已知当前步骤描述为 “吃好吃的，给出吃的食物名。诊断结束。”。其中每个“=>”后的内容为步骤编号，前面给出的步骤名一一对应。
	已知当前步骤的输出为EatFoodResult，用于选择下一步分支的参数定义为{""foodName"": ""食物名，取值范围{\""正常\""}""}。
	请根据所有步骤名、当前步骤描述和当前步骤用于选择下一步分支的参数，以JSON格式生成下一步的所有分支情况。当下一步为诊断结束时，action请选择endNode。
	“是诊断成功，任务结束。”无“=>”表示next数组中只有1个值，因此回答中有2个conditon、action组合。
	你的输出应该为：
	```
	{
		""next"": [
			{
				""condition"": ""${EatFoodResult.foodName == \""正常\""}"",
				""action"": ""endNode""
			}
		]
	}
	```
******************************************************************************************************************
现在请开始回答问题：
已知所有步骤编号和步骤名为
	步骤1：UserCheck0
	步骤2：UserCheck1
	步骤3：UserCheck2
	步骤4：UserCheck3
	步骤5：UserCheck4
	步骤6：UserCheck5
	步骤7：UserCheck6
	步骤8：UserCheck7
	步骤9：informationCollection8
		
已知当前步骤描述为“进行人工操作，检查CloudCG和GSN之间是否有防火墙等。是 => 6。否 => 9。”。其中每个“=>”后的内容为步骤编号，前面给出的步骤名一一对应。
已知当前步骤的输出为UserCheck4Result，用于选择下一步分支的参数定义为{""result"":""CloudCG和GSN之间是否有防火墙 ，取值范围{\""是\""，\""否\""}""}。
请根据所有步骤名、当前步骤描述和当前步骤用于选择下一步分支的参数，以JSON格式生成下一步的所有分支情况。当下一步为诊断结束时，action请选择endNode。
请先分析分支情况。你的输出应该为：""",
        "answer": """{
  ""next"": [
   {
    ""condition"": ""${UserCheck4Result.result == \""是\""}"",
    ""action"": ""UserCheck5""
   },
   {
    ""condition"": ""${UserCheck4Result.result == \""否\""}"",
    ""action"": ""informationCollection8""
   }
  ]
}"""}
    ]
}