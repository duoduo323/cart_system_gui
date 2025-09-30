# cart_system_gui PyCharm
# staff2 Lenovo
# 2025/9/5 周五 下午5:04


from PyQt5.QtWidgets import QApplication, QMainWindow
from pyfile.staffwindow import Ui_StaffWindow
from logic_code.shopping2 import ShoppingWindow2
from logic_code.cargomanagement2 import CargomanagementWindow2
from tool_code.loggerOut import logger_file


class StaffWindow2(QMainWindow):
    def __init__(self):
        # 调用父类的初始化方法
        super(StaffWindow2, self).__init__()
        self.staff = Ui_StaffWindow()
        self.staff.setupUi(self)
        self.shopping2 = ShoppingWindow2()
        # logger_file('info',"该职工用户正在进行操作...")
        self.staff.shoppingButton.clicked.connect(self.start_shopping)
        self.staff.inquireButtnon.clicked.connect(self.start_inqure)
        self.staff.pushButton.clicked.connect(self.return_begin)
        self.cargo = CargomanagementWindow2()

    def start_shopping(self):
        self.close()
        self.shopping2.show()
        logger_file('info',"该职工用户开始购物...")

    def start_inqure(self):
        self.close()
        self.cargo.show()
        logger_file('info',"该职工用户正在查看采购清单和正在销售的货物...")

    def return_begin(self):
        self.close()
        from logic_code.startpage import StartWindow
        self.begin = StartWindow()
        self.begin.show()
        logger_file('info',"该职工用户返回到主界面")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    staff = StaffWindow2()
    staff.show()
    sys.exit(app.exec_())
