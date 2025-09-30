# cart_system_gui PyCharm
# administrate Lenovo
# 2025/8/17 周日 下午6:07
import json

from PyQt5.QtWidgets import QApplication, QMainWindow
from pyfile.administratorwindow import Ui_AdministratorWindow
from logic_code.staffmanagement import StaffmanagementWindow
from logic_code.cargomanagement import CargomanagementWindow
from tool_code.loggerOut import logger_file


class AdministratorWindow(QMainWindow):
    def __init__(self):
        # 调用父类的初始化方法
        super(AdministratorWindow, self).__init__()
        self.admin = Ui_AdministratorWindow()
        self.admin.setupUi(self)
        self.staff_manage = StaffmanagementWindow()
        self.cargo = CargomanagementWindow()
        # logger_file('info',"管理员正在进行操作...")
        self.admin.staffpushButton.clicked.connect(self.start_staff)
        self.admin.cargopushButtnon.clicked.connect(self.start_cargo)
        self.admin.pushButton.clicked.connect(self.begin_page)

    def start_staff(self):
        self.close()
        self.staff_manage.show()
        logger_file('info',"管理员开始员工管理操作...")

    def start_cargo(self):
        self.close()
        self.cargo.show()
        logger_file('info', "管理员开始货物管理操作...")

    def begin_page(self):
        self.close()
        from logic_code.startpage import StartWindow
        self.begin = StartWindow()
        self.begin.show()
        logger_file('info', "管理员返回到主界面")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    login = AdministratorWindow()
    login.show()
    sys.exit(app.exec_())
