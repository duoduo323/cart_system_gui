# cart_system_gui PyCharm
# shopping2 Lenovo
# 2025/9/5 周五 下午5:18

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QHBoxLayout, QLabel, QDialog, \
    QVBoxLayout, QPushButton, QTableWidget
from pyfile.shoppingwindow import Ui_ShoppingWindow
from tool_code.file_edit import file_read, file_write, file_rewrite,file_update
from tool_code.loggerOut import logger_file


class ShoppingWindow2(QMainWindow):
    def __init__(self):
        # 调用父类的初始化方法
        super(ShoppingWindow2, self).__init__()
        self.shopping = Ui_ShoppingWindow()
        self.shopping.setupUi(self)

        self.sale_table = self.shopping.salesTableWidget
        self.sale_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.cart_table = self.shopping.historyTableWidget
        self.num = 10

        self.shopping.returnButton.clicked.connect(self.start_return)
        self.shopping.selectButton.clicked.connect(self.add_cart)
        self.shopping.deleteButton.clicked.connect(self.delete_cart)
        self.shopping.settlementButton.clicked.connect(self.check_cart)

        self.fill_table()
        self.fill_cart()

    def start_return(self):
        self.close()
        from logic_code.staff2 import StaffWindow2
        self.staff2 = StaffWindow2()
        self.staff2.show()
        logger_file('info', "该职工用户返回到操作界面")

    def fill_table(self):
        # logger_file('info', "正在读取商品数据...")
        shopping_data = file_read('product.txt')

        self.sale_table.setRowCount(len(shopping_data))
        self.sale_table.setColumnCount(len(shopping_data[0]) - 1)
        # logger_file('info', "读取数据成功！正在展示商品...")
        headers = ['商品名称', '商品价格']
        self.sale_table.setHorizontalHeaderLabels(headers)

        for row, data in enumerate(shopping_data):
            for col, value in enumerate(data.values()):
                # print(row,col,value)
                if col == 0:
                    continue
                else:
                    col -= 1
                if col == 1:
                    # print(type(value)) ->float
                    if not str(value).startswith('￥'):
                        value = '￥' + str(value)
                self.sale_table.setItem(row, col, QTableWidgetItem(str(value)))

    def fill_cart(self):
        # logger_file('info', "正在读取购物车数据...")
        cart_data = file_read('cart.txt')
        if not cart_data:
            return
        self.cart_table.setRowCount(len(cart_data))
        self.cart_table.setColumnCount(len(cart_data[0]))
        # logger_file('info', "正在展示购物车...")
        headers = ['商品名称', '商品价格', '商品数量', '商品总计']
        self.cart_table.setHorizontalHeaderLabels(headers)

        for row, data in enumerate(cart_data):
            for col, value in enumerate(data.values()):
                self.cart_table.setItem(row, col, QTableWidgetItem(str(value)))

    def add_cart(self):
        self.item = self.sale_table.selectedItems()

        max_colnum = self.sale_table.columnCount()
        logger_file('info', "职工用户正在添加商品到购物车...")
        try:
            if self.item:
                if self.shopping.amountLineEdit.text() != '':
                    self.num = self.shopping.amountLineEdit.text()
                # print(type(self.num)) ->str
                if self.num.isdigit() and int(self.num) > 0 and self.num:
                    quantity = int(self.num)
                    lst = []
                    for col in range(max_colnum):  # 要保证点任意一列都是指同一物品，就循环列获取
                        # print(type(self.item)) ->list
                        row = self.item[0].row()  # 获取当前单元格所在的行号
                        col = col
                        # print(row,col)
                        cell = self.sale_table.item(row, col)
                        # print(cell.text())
                        lst.append(cell.text())
                    lst.append(quantity)
                    lst.append('￥' + str(float(lst[1][1:]) * quantity))
                    self.shopping.amountLineEdit.clear()
                    dic = dict(zip(['name', 'price', 'quantity', 'total'], lst))  # 同下
                    # dic = {'name':lst[0],'price':lst[1],'quantity':lst[2],'total':lst[3]}
                    file_write('cart.txt', [dic])
                    logger_file('warning', f"成功添加商品{lst[0]}到购物车并更新了数据库！")

            self.fill_cart()
        except Exception as e:
            logger_file('error', f"添加商品失败！错误为{e}")

    # def delete_cart(self):
    #     cart = file_read('cart.txt')
    #     select_item = self.cart_table.selectedItems()  # select_item是一个列表
    #     for i in select_item:
    #         name = i.text()
    #         for good in cart:
    #             if name == good.get('name'):
    #                 cart.remove(good)
    #         self.cart_table.removeRow(i.row())
    #     file_rewrite('cart.txt', cart)

    def delete_cart(self):
        try:
            # logger_file('info', "正在读取购物车数据...")
            cart = file_read('cart.txt')
            select_item = self.cart_table.selectedItems()

            # 获取所有要删除的行号（去重）
            rows_to_delete = set()
            for item in select_item:
                rows_to_delete.add(item.row())

            # 获取要删除的商品名称（只从第0列获取商品名称）
            items_to_delete = []
            items_to_num = []
            for row in rows_to_delete:
                name_item = self.cart_table.item(row, 0)  # 第0列是商品名称列
                quantify_item = self.cart_table.item(row, 2)
                if name_item:
                    items_to_delete.append(name_item.text())
                    items_to_num.append(quantify_item.text())
            self.update_num = dict(zip(items_to_delete, items_to_num))

            # 从数据中删除这些商品
            cart = [good for good in cart if good.get('name') not in items_to_delete]

            # 从表格中删除行（按行号从大到小删除）
            for row in sorted(rows_to_delete, reverse=True):
                self.cart_table.removeRow(row)

            file_rewrite('cart.txt', cart)
            for i in items_to_delete:
                logger_file('warning', f"成功从购物车中移除商品{i}并更新了数据库!")
        except Exception as e:
            logger_file('error', f"从购物车中移除商品失败！错误为{e}")

    def check_cart(self):
        logger_file('info',"该职工用户开始结算...")
        max_colnum = self.cart_table.columnCount()
        select_item = self.cart_table.selectedItems()
        total = 0
        for i in select_item:
            row = i.row()
            cell = self.cart_table.item(row, 1)
            total = total + float(cell.text()[1:])
        self.delete_cart()

        # 创建结算成功提示框
        dialog = QDialog(self)
        dialog.setWindowTitle("结算成功")
        dialog.setFixedSize(300, 150)

        layout = QVBoxLayout()

        # 显示总计信息
        total_label = QLabel(f'总计：￥{total:.2f}，已结清！')
        total_label.setAlignment(Qt.AlignCenter)
        total_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(total_label)

        dialog.setLayout(layout)
        dialog.exec_()
        for name,num in self.update_num.items():
            old = file_read('cargo.txt',f'name="{name}"')
            new = old[0].get("quantity")-int(num)
            file_update('cargo.txt',[{"quantity":new}],f'name="{name}"')
        logger_file('warning', f"该职工用户结算成功！成功消费￥{total:.2f}元")
        # print(f'总计：￥{total}，已结清！')


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    shopping = ShoppingWindow2()
    shopping.show()
    sys.exit(app.exec_())
