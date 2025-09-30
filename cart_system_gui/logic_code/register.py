# cart_system_gui PyCharm
# registre Lenovo
# 2025/8/16 周六 下午6:32

# cart_system_gui PyCharm
# login Lenovo
# 2025/8/15 周五 上午11:16
import json

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from pyfile.registrationwindow import Ui_RegistrationWindow
from tool_code.file_edit import file_read, file_write
from tool_code.loggerOut import logger_file
from tool_code.mysql_connect import user_table


class RegistrationWindow(QMainWindow):
    def __init__(self):
        # 调用父类的初始化方法
        super(RegistrationWindow, self).__init__()
        self.register = Ui_RegistrationWindow()
        self.register.setupUi(self)
        # logger_file('info', "用户开始注册信息")
        self.register.pushButton.clicked.connect(self.start_register)
        self.register.pushButton_2.clicked.connect(self.to_login)
        self.message = None

    def start_register(self):

        name = self.register.namelineEdit.text()
        username = self.register.usernamelineEdit.text()
        password = self.register.passwordlineEdit.text()

        item = [{'name': name, 'username': username, 'password': password}]

        if name == '' or username or '' or password == '':
            self.message = QMessageBox.warning(self, '提示', '注册信息不能为空！', QMessageBox.Yes)
            return
        # user = file_read('user.txt')
        if user_table.verify_user('user.txt', f'{username}', f'{password}'):
            print('已注册，请登录')
            logger_file('warning', f"用户{username}已经注册!返回登录界面")
            self.close()  # 关闭窗口
            from login import LoginWindow
            self.login = LoginWindow()
            self.login.show()
        # for i in user:
        #     if name == i.get('name') and username == i.get('username') and password == i.get('password'):
        #         print('已注册，请登录')
        #         logger_file('warning', f"用户{username}已经注册!返回登录界面")
        #         self.close()  # 关闭窗口
        #         from login import LoginWindow
        #         self.login = LoginWindow()
        #         self.login.show()
        #         break
        else:
            user_table.create_user('user.txt', item[0].get('name'), item[0].get('username'), item[0].get('password'))
            # file_write('user.txt', item)
            logger_file('info', f"用户{username}注册成功！返回登录页面")
            self.close()
            from logic_code.login import LoginWindow
            self.login = LoginWindow()
            self.login.show()

    def to_login(self):
        self.close()
        from logic_code.login import LoginWindow
        self.login = LoginWindow()
        self.login.show()
        logger_file('info', f"用户返回登录页面")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    register = RegistrationWindow()
    register.show()
    sys.exit(app.exec_())
