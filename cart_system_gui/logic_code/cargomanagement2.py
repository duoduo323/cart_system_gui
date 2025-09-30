# cart_system_gui PyCharm
# cargomanagement2 Lenovo
# 2025/9/5 周五 下午5:24


# cart_system_gui PyCharm
# cargomanagement Lenovo
# 2025/8/17 周日 下午9:59

import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from pyfile.cargomanagementwindow import Ui_CargomanagementWindow
from tool_code.file_edit import file_read, file_write, file_rewrite
from logic_code.new_cargo import NewCargoWindow
from tool_code.loggerOut import logger_file


class CargomanagementWindow2(QMainWindow):
    def __init__(self):
        # 调用父类的初始化方法
        super(CargomanagementWindow2, self).__init__()
        self.cargomanage = Ui_CargomanagementWindow()
        self.cargomanage.setupUi(self)

        self.sale_table = self.cargomanage.purchaseTableWidget_2
        self.purchase_table = self.cargomanage.purchaseTableWidget
        self.cargomanage.pushButton.clicked.connect(self.return_main)
        self.startsale()
        self.fill_purchase()
        self.cargomanage.putButton.clicked.connect(self.push)
        self.cargomanage.pushButton_2.clicked.connect(self.delete)
        self.cargomanage.updateButton.clicked.connect(self.addcargo)
        self.cargomanage.returnButton_2.clicked.connect(self.delcargo)
        self.cargomanage.addButton.clicked.connect(self.alladd)
        self.new_cargo = NewCargoWindow()

        # 设置限制访问
        self.cargomanage.putButton.setEnabled(False)
        self.cargomanage.updateButton.setEnabled(False)
        self.cargomanage.returnButton_2.setEnabled(False)
        self.cargomanage.addButton.setEnabled(False)
        self.cargomanage.pushButton_2.setEnabled(False)

    def alladd(self):
        lst = []
        purchase = file_read('cargo.txt')
        product = file_read('product.txt')
        for i in purchase:
            if i.get('name') not in [j.get('name') for j in product]:
                lst.append(i)
        for i in lst:
            d = file_read('product.txt')
            id_ = len(d) + 1
            file_write('product.txt', [{'id': id_, 'name': i.get('name'), 'price': i.get('price')}])
        self.startsale()


    def addcargo(self):
        self.close()
        self.new_cargo.show()

    def delcargo(self):
        cargo = file_read('cargo.txt')
        select_item = self.purchase_table.selectedItems()

        # 获取所有要删除的行号（去重）
        rows_to_delete = set()
        for item in select_item:
            rows_to_delete.add(item.row())
        # 获取要删除的商品名称（只从第0列获取商品名称）
        items_to_delete = []
        for row in rows_to_delete:
            name_item = self.purchase_table.item(row, 0)  # 第0列是商品名称列
            if name_item:
                items_to_delete.append(name_item.text())
        # 从数据中删除这些商品
        cargo = [good for good in cargo if good.get('name') not in items_to_delete]

        # 从表格中删除行（按行号从大到小删除）
        for row in sorted(rows_to_delete, reverse=True):
            self.purchase_table.removeRow(row)

        file_rewrite('cargo.txt', cargo)

    def delete(self):
        self.item = self.sale_table.selectedItems()
        if self.item:
            row = self.item[0].row()
            name = self.sale_table.item(row, 0).text()
            lst = file_read('product.txt')
            lst1 = []
            for data in lst:
                if data['name'] != name:
                    lst1.append(data)
            file_rewrite('product.txt', lst1)
        self.startsale()

    def push(self):
        self.items = self.purchase_table.selectedItems()
        if self.items:
            row = self.items[0].row()
            name = self.purchase_table.item(row, 0).text()
            price = self.purchase_table.item(row, 2).text()
            d = file_read('product.txt')
            id_ = len(d) + 1
            file_write('product.txt', [{'id': id_, 'name': name, 'price': price}])
            self.startsale()

    def fill_purchase(self):
        shopping_data = file_read('cargo.txt')
        self.purchase_table.setRowCount(len(shopping_data))
        self.purchase_table.setColumnCount(len(shopping_data[0]))
        headers = ['商品名称', '商品库存', '商品价格']
        self.purchase_table.setHorizontalHeaderLabels(headers)
        for i, data in enumerate(shopping_data):
            for j, value in enumerate(data.values()):
                if j == 2:
                    # print(type(value)) ->float
                    value = '￥' + str(value)
                self.purchase_table.setItem(i, j, QTableWidgetItem(str(value)))
            # for col in range(2):
            #     if col == 0:
            #         self.purchase_table.setItem(i, col, QTableWidgetItem(list(data.values())[0]))
            #     else:
            #         self.purchase_table.setItem(i, col, QTableWidgetItem(str(list(data.values())[2])))

    def startsale(self):
        shopping_data = file_read('product.txt')

        self.sale_table.setRowCount(len(shopping_data))
        self.sale_table.setColumnCount(len(shopping_data[0]) - 1)

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
                    if str(value).startswith('￥'):
                        value = str(value)
                    else:
                        value = '￥' + str(value)
                self.sale_table.setItem(row, col, QTableWidgetItem(str(value)))

    def return_main(self):
        self.close()
        from logic_code.staff2 import StaffWindow2
        self.staff2 = StaffWindow2()
        self.staff2.show()
        logger_file('info',"该职工用户返回到操作界面")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    cargomanage = CargomanagementWindow2()
    cargomanage.show()
    sys.exit(app.exec_())
