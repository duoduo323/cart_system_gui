# cart_system_gui PyCharm
# new_staff Lenovo
# 2025/9/6 周六 下午1:59

from PyQt5.QtWidgets import QApplication, QMainWindow
from pyfile.cargowindow import Ui_CargoWindow
from tool_code.file_edit import file_read, file_write
from tool_code.loggerOut import logger_file
from tool_code.mysql_connect import staff_table


class NewStaffWindow(QMainWindow):
    def __init__(self):
        # 调用父类的初始化方法
        super(NewStaffWindow, self).__init__()
        self.cargo = Ui_CargoWindow()
        self.cargo.setupUi(self)

        self.cargo.pushButton.clicked.connect(self.add_staff)
        self.cargo.returnButton.clicked.connect(self.return_staff)

    def add_staff(self):
        try:
            name = self.cargo.productNameEdit.text()
            username = self.cargo.amountLineEdit.text()
            password = self.cargo.priceLineEdit.text()

            item = [{'name': name, 'username': username, 'password': password}]

            # cargo = file_read('staff.txt')
            if staff_table.verify_user('staff.txt', f'{username}', f'{password}'):
                logger_file('error', f"添加的用户{name}已存在！")
            # for i in cargo:
            #     if name == i.get('name') and username == i.get('quantity') and password == i.get('price'):
            #         logger_file('error',f"添加的用户{name}已存在！")
            #         break
            else:
                staff_table.create_user('staff.txt',item[0].get('name'), item[0].get('username'), item[0].get('password'))
                # file_write('staff.txt', item)
                logger_file('warning', f"成功添加新用户{name}！")
                self.return_staff()
                # self.cargo.productNameEdit.clear()
                # self.cargo.amountLineEdit.clear()
                # self.cargo.priceLineEdit.clear()
        except Exception as e:
            logger_file('error', f"新用户添加失败！错误为{e}")

    def return_staff(self):
        self.close()
        from logic_code.staffmanagement import StaffmanagementWindow
        self.staff = StaffmanagementWindow()
        self.staff.show()
        logger_file('info', "管理员返回到员工管理界面")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    staff = NewStaffWindow()
    staff.show()
    sys.exit(app.exec_())
