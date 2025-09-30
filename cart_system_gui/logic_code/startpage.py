# cart_system_gui PyCharm
# start Lenovo
# 2025/9/6 周六 下午10:07


from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer
from pyfile.startwindow import Ui_MainWindow
from tool_code.loggerOut import logger_file


class StartWindow(QMainWindow):
    def __init__(self):
        # 调用父类的初始化方法
        super(StartWindow, self).__init__()
        self.begin = Ui_MainWindow()
        self.begin.setupUi(self)

        self.begin.pushButton.clicked.connect(self.access_login)
        self.begin.pushButton_2.clicked.connect(self.access_login)
        self.begin.pushButton_3.clicked.connect(self.access_login)
        self.begin.pushButton_4.clicked.connect(self.exit_sys)

    def access_login(self):
        self.close()
        from logic_code.login import LoginWindow
        self.log = LoginWindow()
        self.log.show()
        logger_file('info', "用户进入登录界面")

    def exit_sys(self):
        """安全退出系统"""
        # 先询问用户确认
        reply = QMessageBox.question(
            self,
            '确认退出',
            "确定要退出购物车管理系统吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            logger_file('info', "用户退出了购物车系统！")
            # 安全退出方式
            QTimer.singleShot(100, self.quit_application)  # 延迟100毫秒退出
        else:
            logger_file('info', "用户取消退出购物车系统")

    def quit_application(self):
        """安全退出应用程序"""
        # 获取QApplication实例并退出
        app = QApplication.instance()
        if app:
            app.quit()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    start = StartWindow()
    start.show()
    sys.exit(app.exec_())
