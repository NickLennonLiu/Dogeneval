from .code_generation import data as code_data # 代码/MML生成
from .text_generation import data as text_generation_data # 文本生成
from .tool import data as tool_data  # 工具使用
from .format import data as format_data # 格式遵从
from .task import data as task_data # 任务规划
from .math_calculation import data as math_data # 数学计算
from .semantic import data as semantic_data # 语义理解
from .logic import data as logic_data # 逻辑推理


ability_templates = [
    code_data,
    text_generation_data,
    tool_data,
    format_data,
    task_data,
    math_data,
    semantic_data,
    logic_data
]