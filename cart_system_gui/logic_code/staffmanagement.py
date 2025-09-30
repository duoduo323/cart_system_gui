# cart_system_gui PyCharm
# staffmanagement Lenovo
# 2025/8/17 周日 下午6:31

import json

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from pyfile.staffmanagementwindow import Ui_StaffmanagementWindow
from tool_code.file_edit import file_read, file_rewrite
from logic_code.new_staff import NewStaffWindow
from tool_code.loggerOut import logger_file


class StaffmanagementWindow(QMainWindow):
    def __init__(self):
        # 调用父类的初始化方法
        super(StaffmanagementWindow, self).__init__()
        self.staff = Ui_StaffmanagementWindow()
        self.staff.setupUi(self)
        self.new_staff = NewStaffWindow()

        self.fill_table()

        self.staff.addpushButton.clicked.connect(self.add_staff)
        # self.staff.addpushButton_2.clicked.connect(self.)
        self.staff.deletepushButton.clicked.connect(self.delete_staff)
        self.staff.returnpushButton.clicked.connect(self.return_main)

    def fill_table(self):
        try:
            # logger_file('info',"正在读取员工数据...")
            staff_data = file_read('staff.txt')

            self.staff.tableWidget.setRowCount(len(staff_data))
            self.staff.tableWidget.setColumnCount(len(staff_data[0]))

            headers = ['名字', '用户名', '密码']
            self.staff.tableWidget.setHorizontalHeaderLabels(headers)

            for row, data in enumerate(staff_data):
                for col, value in enumerate(data.values()):
                    self.staff.tableWidget.setItem(row, col, QTableWidgetItem(str(value)))
            # logger_file('info',"成功读取员工数据！")
            # 自动调整列宽以适应内容
            self.staff.tableWidget.resizeColumnsToContents()

            # 自动调整行高以适应内容
            self.staff.tableWidget.resizeRowsToContents()

            # 可选：设置最小列宽，确保标题也显示完整
            self.staff.tableWidget.horizontalHeader().setMinimumSectionSize(100)
        except Exception as e:
            logger_file('error',f"读取员工数据失败，错误为{e}")

    def add_staff(self):
        self.close()
        self.new_staff.show()
        logger_file('warning',"管理员开始添加新员工...")

    def delete_staff(self):
        try:
            # logger_file('info', "正在读取员工数据...")
            staff = file_read('staff.txt')
            select_item = self.staff.tableWidget.selectedItems()

            # 获取所有要删除的行号（去重）
            rows_to_delete = set()
            for item in select_item:
                rows_to_delete.add(item.row())
            # 获取要删除的员工名称（只从第0列获取名称）
            names_to_delete = []
            for row in rows_to_delete:
                name_item = self.staff.tableWidget.item(row, 0)  # 第0列是名称列
                if name_item:
                    names_to_delete.append(name_item.text())
            # 从数据中删除这些员工
            staff = [person for person in staff if person.get('name') not in names_to_delete]
            # 从表格中删除行（按行号从大到小删除）
            for row in sorted(rows_to_delete, reverse=True):
                self.staff.tableWidget.removeRow(row)

            file_rewrite('staff.txt', staff)
            for i in names_to_delete:
                logger_file('info', f"管理员成功删除员工{i}并更新了数据库！")
        except Exception as e:
            logger_file('error', f"管理员删除员工数据失败，错误为{e}")

    def return_main(self):
        self.close()
        from logic_code.administrate import AdministratorWindow
        self.admin = AdministratorWindow()
        self.admin.show()
        logger_file('info',"管理员返回到操作界面")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    staff = StaffmanagementWindow()
    staff.show()
    sys.exit(app.exec_())
