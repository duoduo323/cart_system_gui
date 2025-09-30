# cart_system_gui PyCharm
# loggerOut Lenovo
# 2025/9/6 周六 下午6:18


import logging


def logger_file(level, message, set_level=logging.DEBUG):
    logging.basicConfig(
        level=set_level,
        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('./data/cart_system_operations.log',mode='a+', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    dic = {'info': logging.info, 'debug': logging.debug, 'error': logging.error,
           'warning': logging.warning, 'critical': logging.critical, }
    for k, v in dic.items():
        if level == k:
            level = v
            break
    else:
        return '请输入正确的日志级别'
    return level(message, stacklevel=2)