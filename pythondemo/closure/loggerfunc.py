import logging

# 设置日志格式
import time

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)

logger = logging.getLogger()
# 设置日志级别
logger.setLevel('INFO')
# 新增控制台处理器
console_log = logging.StreamHandler()
console_log.setFormatter(formatter)
# 新增文件处理器
# file_log = logging.FileHandler('./log/log.txt')
# file_log.setFormatter(formatter)
# logger.addHandler(file_log)
logger.addHandler(console_log)


def log(module):
    def wrapper(func):
        def _wrapper(*args, **kwargs):
            logger.info('执行的方法是：{}'.format(module))
            start = time.time()
            ret = func(*args, **kwargs)
            logger.info(ret)
            end = time.time()
            logger.info('程序已完成，耗时：{}'.format(end - start))
            return ret
        return _wrapper
    return wrapper


@log('add')
def add(a, b):
    return a + b

"""
    执行步骤如下：
    1、执行 log('add') 方法
    2、add = wrapper(add) --> add = decorator()
    3、add(100,29) == decorator(100,29)
"""
add(100, 29)