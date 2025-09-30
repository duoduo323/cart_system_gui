# cart_system_gui PyCharm
# mysql_connect Lenovo
# 2025/9/4 周四 上午10:26

import time
import pymysql
from typing import List, Dict
from tool_code.loggerOut import logger_file
from tool_code.password_tool import PasswordUtils


class SqlOperation:
    def __init__(self, host: str, port: int, user: str, password: str, database: str,
                 charset: str = 'utf8'):
        """

        :param host: 要连接的数据库地址
        :param port: 要连接的数据库端口
        :param user: 使用哪个 用户名 去 连接数据库
        :param password: 用户名的密码
        :param database: 使用的数据库
        :param charset: 数据库的编码格式
        """

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.client = None
        self.cursor = None
        logger_file('info', f"初始化数据库连接对象: host={host}, port={port}, database={database}, user={user}")

    def connect(self) -> bool:
        try:
            start_time = time.time()
            self.client = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                          database=self.database, charset=self.charset,
                                          cursorclass=pymysql.cursors.DictCursor)
            elapsed_time = time.time() - start_time
            self.cursor = self.client.cursor()
            logger_file('info', f"数据库连接成功! 连接耗时: {elapsed_time:.3f}秒")
            return True
        except pymysql.Error as e:  # 具体的错误后面多的话直接.Error
            logger_file('error', f"连接数据库失败: {e}")
            return False

    def select_data(self, table_name: str, columns: List[str], where: str = None) -> List[Dict]:
        try:
            columns = ','.join(columns)
            if where:
                sentence = f'SELECT {columns} FROM {table_name} WHERE {where}'
            else:
                sentence = f'SELECT {columns} FROM {table_name}'

            # logger_file('info', f"执行查询：{sentence}")
            # start_time = time.time()
            self.cursor.execute(sentence)  # 简写，用sentence引用
            result = self.cursor.fetchall()
            # elapsed_time = time.time() - start_time

            # logger_file('info', f"查询成功，获取到{len(result)}条记录，耗时: {elapsed_time:.3f}秒")

            return result
        except pymysql.Error as e:
            # logger_file('error', f"执行查询失败: {sentence}, 错误: {e}")
            return []

    def insert_data(self, table_name: str, data: List[Dict[str, str | int]]) -> str:
        """

        :param table_name: 要插入数据的表名
        :param data: 要插入的数据
        :return: 返回‘插入成功’
        """
        try:
            # logger_file('info', f"开始向表{table_name}插入{len(data)}条数据")
            success_count = 0

            for i, record in enumerate(data):
                column = ','.join(record.keys())
                if len(record) == 1:
                    sentence = f'INSERT {table_name}({column}) VALUES ({tuple(record.values())[0]})'  # 后边插入的值可写({i.get(columns)})
                else:
                    sentence = f'INSERT {table_name}({column}) VALUES {tuple(record.values())}'

                try:
                    self.cursor.execute(sentence)
                    success_count += 1
                    # logger_file('debug', f"成功插入第{i + 1}条记录: {sentence}")
                except pymysql.Error as e:
                    print(f'插入数据失败: {e}')
                    # logger_file('error', f"插入第{i + 1}条记录失败: {sentence}, 错误: {e}")

            self.client.commit()  # 建立一次连接可以提交多次
            # logger_file('info', f"数据插入完成，成功{success_count}条，失败{len(data) - success_count}条")

            return f'数据添加成功!成功插入{success_count}条记录'
        except pymysql.Error as e:
            # logger_file('error', f"插入数据过程中发生错误: {e}")
            self.client.rollback()
            return f'数据添加失败: {e}'

    def update_data(self, table_name: str, data: List[Dict[str, str | int]], where: str = None) -> str:
        """

        :param table_name: 要修改表的名字
        :param data: 要修改的数据
        :param where: 修改数据的条件
        :return: 返回’修改成功‘
        """
        try:
            # logger_file('info', f"开始更新表{table_name}的数据，条件: {where if where else '无条件'}")
            success_count = 0

            for i, record in enumerate(data):
                value = list(record.values())[0]
                if where:
                    sentence = f'UPDATE {table_name} SET {tuple(record.keys())[0]}="{value}" where {where}'
                else:
                    sentence = f'UPDATE {table_name} SET {tuple(record.keys())[0]}="{value}"'

                try:
                    self.cursor.execute(sentence)
                    affected_rows = self.cursor.rowcount
                    success_count += affected_rows
                    # logger_file('debug', f"执行更新: {sentence}, 影响行数: {affected_rows}")
                except pymysql.Error as e:
                    print(f'更新数据失败: {e}')
                    # logger_file('error', f"更新第{i + 1}条记录失败: {sentence}, 错误: {e}")

            self.client.commit()
            # logger_file('info', f"数据更新完成，成功更新{success_count}条记录")
            return f'数据修改成功! 共更新{success_count}条记录'
        except pymysql.Error as e:
            # logger_file('error', f"更新数据过程中发生错误: {e}")
            self.client.rollback()
            return f'数据修改失败: {e}'

    def delete_data(self, table_name: str, where: str = None) -> str:
        """

        :param table_name: 要删除数据的表名称
        :param where: 要删除数据的条件
        :return: 返回’删除成功‘
        """
        try:
            if where:
                sentence = f'DELETE FROM {table_name} WHERE {where}'
            else:
                sentence = f'DELETE FROM {table_name}'

            # logger_file('warning', f"执行删除操作: {sentence}")
            self.cursor.execute(sentence)
            affected_rows = self.cursor.rowcount
            self.client.commit()

            # logger_file('info', f"删除操作完成，删除了{affected_rows}条记录")
            return f'数据删除成功! 共删除{affected_rows}条记录'
        except pymysql.Error as e:
            # logger_file('error', f"删除数据失败: {sentence}, 错误: {e}")
            self.client.rollback()
            return f'数据删除失败: {e}'

    def __del__(self):  # 当对象被销毁时自动调用，类中全执行完才执行
        """当对象被销毁时自动调用，安全地关闭数据库连接"""
        # 只进行必要的清理操作，避免日志记录
        try:
            # 先关闭游标
            if hasattr(self, 'cursor') and self.cursor is not None:
                try:
                    self.cursor.close()
                except:
                    pass  # 静默处理游标关闭异常
        except:
            pass  # 静默处理属性访问异常

        try:
            # 再关闭数据库连接
            if hasattr(self, 'client') and self.client is not None:
                try:
                    self.client.close()
                except:
                    pass  # 静默处理连接关闭异常
        except:
            pass  # 静默处理属性访问异常


class ConnectTable:
    """数据表操作类"""

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.sql_operation = SqlOperation(host='localhost', port=3306, user='root', password='123456',
                                          database='spt2507')
        logger_file('info', f"正在将文件{table_name}与数据库建立连接")
        if not self.sql_operation.connect():
            raise ConnectionError(f"无法连接到数据库表: {table_name}")


    def select_product(self, where: str = None) -> List[Dict]:
        """获取所有商品"""
        return self.sql_operation.select_data(f'{self.table_name}', ['*'], where)

    def insert_product(self, data: List[Dict[str, str | int]]):
        """向表中添加数据"""
        self.sql_operation.insert_data(f'{self.table_name}', data)

    def delete_product(self, where: str = None):
        """对表中数据做删除"""
        self.sql_operation.delete_data(f'{self.table_name}', where)

    def update_product(self, data: List[Dict[str, str | int]], where: str = None):
        """更新表中数据"""
        self.sql_operation.update_data(f'{self.table_name}', data, where)

    # 用户相关特殊方法
    @staticmethod
    def create_user(table_name: str, name: str, username: str, password: str) -> bool:
        """创建用户（自动加密密码）"""
        try:
            hashed_password = PasswordUtils.hash_password(password)
            user_data = [{
                'name': name,
                'username': username,
                'password': hashed_password,
            }]
            from tool_code.file_edit import file_write
            file_write(table_name, user_data)
            return True
        except Exception as e:
            logger_file('error', f"创建用户失败: {e}")
            return False

    @staticmethod
    def verify_user(table_name: str, username: str, password: str) -> bool:
        """验证用户密码"""
        try:
            # users = self.sql.select_data('user', [f'{password}'], f'username = {username}')
            from tool_code.file_edit import file_read
            users = file_read(table_name, f'username = "{username}"')
            if not users:
                return False

            stored_password = users[0]['password']
            return PasswordUtils.verify_password(password, stored_password)
        except Exception as e:
            logger_file('error', f"验证用户失败: {e}")
            return False


product_table = ConnectTable('product')
user_table = ConnectTable('user')
cargo_table = ConnectTable('cargo')
cart_table = ConnectTable('cart')
staff_table = ConnectTable('staff')

# if __name__ == '__main__':
# c = ConnectTable('shopping')
# print(c.get_all_product())
# product = [{"id": 1, "name": "笔记本电脑", "price": 7999.99},
#            {"id": 2, "name": "无线鼠标", "price": 89.5},
#            {"id": 3, "name": "冰箱", "price": 3600},
#            {"id": 4, "name": "洗衣机", "price": 1500}]
# # c.insert_product(product)
# # c.delete_product('id>3')
# c.update_product([{'name': '洗衣机'}, {'price': 1500}], 'id = 2')
# print(c.get_all_product())

# b = ConnectTable('user')
# print(b.get_all_product())
# user = [{"name": "张三", "username": "zhangsan", "password": "123123"},
#         {"name": "李四", "username": "lisi", "password": "456456"},
#         {"name": "王五", "username": "wangwu", "password": "789789"},
#         {"name": "赵六", "username": "zhaoliu", "password": "123789"}]
# # b.insert_product(user)
# # b.delete_product('name="张三"')
# b.update_product([{'username': 'lili'}, {'password': '555555'}], 'name = "李四"')
# print(b.get_all_product())

# cargo = [{"name": "笔记本电脑", "quantity": 100, "price": 7999.99},
#          {"name": "无线鼠标", "quantity": 100, "price": 89.5},
#          {"name": "蓝牙耳机", "quantity": 100, "price": 399.0},
#          {"name": "冰箱", "quantity": 50, "price": "3600"},
#          {"name": "洗衣机", "quantity": 100, "price": "1500"}]
# print(cargo_table.get_all_product())
# cargo_table.insert_product(cargo)
# print(cargo_table.get_all_product())

# cart = [{"name": "冰箱", "price": "￥3600", "quantity": 2, "total": "￥7200.0"},
#         {"name": "无线鼠标", "price": "￥89.5", "quantity": 10, "total": "￥895.0"}]
# print(cart_table.get_all_product())
# cart_table.insert_product(cart)
# print(cart_table.get_all_product())

# staff = [{"name": "小明", "username": "xiaoming", "password": "111111"},
#          {"name": "小红", "username": "xiaohong", "password": "222222"},
#          {"name": "小黄", "username": "xiaohuang", "password": "333333"},
#          {"name": "小白", "username": "xiaobai", "password": "444444"}]
# print(staff_table.get_all_product())
# staff_table.insert_product(staff)
# print(staff_table.get_all_product())

# c = SqlOperation(host='192.168.8.235', port=3306, user='zxd', password='111111', database='spt2507')
# if c.connect():
#     print(c.show_tables())
#     print(c.desc_table('money'))
# print(c.select_data('money',['*'],where='id<2'))
# print(c.insert_data('money',[{'id':1,'mon':10},{'id':2,'mon':20},{'mon':30},{'mon':40}]))
# print(c.insert_data('money',[{'id':100,'mon':0},{'mon':100001}]))
# print(c.select_data('money', ['*']))
# print(c.delete_data('money', 'id>100'))
# print(c.update_data('money',[{'mon':11},{'id':11111}],'id=1'))
# print(c.update_data('money',[{'mon':1}]))
# print(c.select_data('money', ['*']))
