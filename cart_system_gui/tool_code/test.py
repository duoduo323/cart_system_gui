# cart_system_gui PyCharm
# test Lenovo
# 2025/9/6 周六 上午10:17
import os.path
import json
from tool_code.mysql_connect import *

conn = {'user.txt': user_table, 'staff.txt': staff_table, 'product.txt': product_table,
        'cart.txt': cart_table, 'cargo.txt': cargo_table}


def file_read(file_name):
    for k, v in conn.items():
        if file_name == k:
            return v.get_all_product()


# print(file_read('cart.txt'))

def file_write(file_name, content):
    for k, v in conn.items():
        if file_name == k:
            v.insert_product(content)


file_write('product.txt', [{"id": 1, "name": "笔记本电脑", "price": "7999.99"},
                           {"id": 2, "name": "无线鼠标", "price": "89.5"},
                           {"id": 3, "name": "冰箱", "price": "3600"},
                           {"id": 4, "name": "洗衣机", "price": "1500"}])
print(file_read('product.txt'))


def file_rewrite(file_name, lst: List[Dict]):
    for k, v in conn.items():
        if file_name == k:
            v.delete_product()
            v.insert_product(lst)

# file_rewrite('cargo.txt', [{"name": "笔记本电脑", "quantity": 200000, "price": "7999.99"},
#                            {"name": "无线鼠标", "quantity": 500000, "price": "89.5"},
#                            {"name": "蓝牙耳机", "quantity": 1000000, "price": "399.0"},
#                            {"name": "冰箱", "quantity": 300000, "price": "3600"},
#                            {"name": "洗衣机", "quantity": 200000, "price": "1500"}])
#
# print(file_read('cargo.txt'))
