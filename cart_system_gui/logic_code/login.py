# cart_system_gui PyCharm
# login Lenovo
# 2025/8/15 周五 上午11:16
import json

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from pyfile.loginwindow import Ui_LoginWindow
from logic_code.staff import StaffWindow
from logic_code.staff2 import StaffWindow2
from logic_code.register import RegistrationWindow
# from tool_code.file_edit import file_read

from logic_code.administrate import AdministratorWindow

from tool_code.loggerOut import logger_file

from tool_code.mysql_connect import user_table,staff_table


class LoginWindow(QMainWindow):
    def __init__(self):
        # 调用父类的初始化方法
        super(LoginWindow, self).__init__()
        self.login = Ui_LoginWindow()
        self.login.setupUi(self)

        # logger_file('info',"用户开始登录")
        self.login.pushButton.clicked.connect(self.start_login)
        self.login.pushButton_2.clicked.connect(self.star_return)
        self.login.pushButton_3.clicked.connect(self.to_register)
        # .connect() 方法需要的是一个可调用对象（函数或方法）
        # 当按钮被点击时，Qt 框架会自动调用这个函数
        # 如果加上括号 ()，会在连接时就立即执行函数，而不是在点击时执行

        self.staff = StaffWindow()

        self.staff2 = StaffWindow2()
        self.register = RegistrationWindow()

        self.admin = AdministratorWindow()

        self.message = None
        self.begin = None

        # 测试的时候设置预定值，这样不用每次都输入了
        # self.login.usernamelineEdit.setText('zxd')
        # self.login.passwordlineEdit.setText('123')

    def start_login(self):

        username = self.login.usernamelineEdit.text()
        password = self.login.passwordlineEdit.text()

        if username == 'admin' and password == '123456':
            # print('管理员登录成功！')
            self.close()
            self.admin.show()
            logger_file('info',f"管理员用户{username}登录成功！")
            return

        # staff = file_read('staff.txt')
        # # with open('../data/user.txt', 'r', encoding='utf-8') as f:
        # user = file_read('user.txt')
        if user_table.verify_user('user.txt',f'{username}', f'{password}'):
            self.close()  # 关闭窗口
            self.staff.show()
            logger_file('info', f"普通用户{username}登录成功！")
        elif staff_table.verify_user('staff.txt',f'{username}', f'{password}'):
            self.close()  # 关闭窗口
            self.staff2.show()
            logger_file('info', f"职工用户{username}登录成功！")

        # for i in user:
        #
        #     if username == i.get('username') and password == i.get('password'):
        #         self.close()  # 关闭窗口
        #         self.staff.show()
        #         logger_file('info', f"普通用户{username}登录成功！")
        #         break
        #     for i in staff:
        #         if username == i.get('username') and password == i.get('password'):
        #             self.close()  # 关闭窗口
        #             self.staff2.show()
        #             logger_file('info', f"职工用户{username}登录成功！")
        #             break
        #     else:
        #         continue
        #     break
        else:
            logger_file('error',f"用户{username}登录失败！！")
            try:
                self.message = QMessageBox.critical(self, '提示', '请先注册！', QMessageBox.Yes | QMessageBox.No,
                                                    QMessageBox.Yes)
                # print(self.message)
            except Exception as e:
                print(e)

            if self.message == 16384:
                self.to_register()

    def to_register(self):
        self.close()  # 关闭窗口
        self.register.show()
        logger_file('info', "用户进入注册界面")

    def star_return(self):
        self.close()
        from logic_code.startpage import StartWindow
        self.begin = StartWindow()
        self.begin.show()
        logger_file('info',"用户返回主界面")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
