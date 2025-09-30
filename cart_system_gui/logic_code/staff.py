# cart_system_gui PyCharm
# staff.txt Lenovo
# 2025/8/16 周六 下午10:17

import json

from PyQt5.QtWidgets import QApplication, QMainWindow
from pyfile.staffwindow import Ui_StaffWindow
from logic_code.shopping import ShoppingWindow
from tool_code.loggerOut import logger_file


class StaffWindow(QMainWindow):
    def __init__(self):
        # 调用父类的初始化方法
        super(StaffWindow, self).__init__()
        self.staff = Ui_StaffWindow()
        self.staff.setupUi(self)

        self.shopping = ShoppingWindow()

        # logger_file('info',"该普通用户正在进行操作...")
        self.staff.shoppingButton.clicked.connect(self.start_shopping)
        self.staff.pushButton.clicked.connect(self.return_begin)

        # 设置限制访问
        self.staff.inquireButtnon.setEnabled(False)

    def start_shopping(self):
        self.close()
        self.shopping.show()
        logger_file('info',"该普通用户开始购物...")


    def start_inqure(self):
        pass

    def return_begin(self):
        self.close()
        from logic_code.startpage import StartWindow
        self.begin = StartWindow()
        self.begin.show()
        logger_file('info',"该普通用户返回到主界面")




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    staff = StaffWindow()
    staff.show()
    sys.exit(app.exec_())
