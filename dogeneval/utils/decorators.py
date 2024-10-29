"""
定义一系列装饰器
"""

import time
import inspect
import os
from loguru import logger
from functools import wraps

def retry(max_retries=3, sleep_time=20, default_return_value=None):
    """
    重试装饰器，当发生异常中断时，重试一定次数
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            file_path = inspect.getfile(func)
            filename = os.path.basename(file_path)
            for _ in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"[{filename}] Error: {e}")
                    time.sleep(sleep_time)
                    return default_return_value
        return wrapper
    return decorate