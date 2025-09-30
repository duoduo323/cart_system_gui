# cart_system_gui PyCharm
# file_edit Lenovo
# 2025/8/17 周日 上午9:32
import os.path
import json
from typing import List, Dict
from tool_code.mysql_connect import user_table, staff_table, product_table, cargo_table, cart_table

conn = {'user.txt': user_table, 'staff.txt': staff_table, 'product.txt': product_table,
        'cart.txt': cart_table, 'cargo.txt': cargo_table}


def file_read(file_name, where: str = None):
    # with open(os.path.join('./data', file_name), 'r', encoding='utf-8') as f:
    #     message = [json.loads(i.strip()) for i in f]
    # return message
    for k, v in conn.items():
        if file_name == k:
            return v.select_product(where)


def file_write(file_name: str, content: List[Dict]):
    # with open(os.path.join('./data', file_name), 'a', encoding='utf-8') as f:
    #     for i in content:
    #         json.dump(i, f, ensure_ascii=False)
    #         # f.write(json.dumps(data, ensure_ascii=False) + '\n')  # 或者这么写
    #         f.write('\n')
    for k, v in conn.items():
        if file_name == k:
            v.insert_product(content)


def file_rewrite(file_name, lst: List[Dict]):
    # with open(os.path.join('./data', file_name), 'w', encoding='utf-8') as f:
    #     for i in lst:
    #         json.dump(i, f, ensure_ascii=False)
    #         # f.write(json.dumps(data, ensure_ascii=False) + '\n')  # 或者这么写
    #         f.write('\n')
    for k, v in conn.items():
        if file_name == k:
            v.delete_product()
            v.insert_product(lst)


def file_update(file_name, lst: List[Dict], where: str = None):
    for k, v in conn.items():
        if file_name == k:
            return v.update_product(lst, where)
