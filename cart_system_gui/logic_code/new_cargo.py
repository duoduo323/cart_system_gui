# cart_system_gui PyCharm
# new_cargo Lenovo
# 2025/9/6 周六 下午3:14

from PyQt5.QtWidgets import QApplication, QMainWindow
from pyfile.cargowindow2 import Ui_MainWindow
from tool_code.file_edit import file_read, file_write
from tool_code.loggerOut import logger_file


class NewCargoWindow(QMainWindow):
    def __init__(self):
        # 调用父类的初始化方法
        super(NewCargoWindow, self).__init__()
        self.cargo = Ui_MainWindow()
        self.cargo.setupUi(self)

        self.cargo.pushButton.clicked.connect(self.add_cargo)
        self.cargo.returnButton.clicked.connect(self.return_cargo)

    def add_cargo(self):
        try:
            name = self.cargo.productNameEdit.text()
            amount = self.cargo.amountLineEdit.text()
            price = self.cargo.priceLineEdit.text()

            item = {'name': name, 'quantity': amount, 'price': price}

            cargo = file_read('cargo.txt')

            for i in cargo:
                if name == i.get('name') and amount == i.get('quantity') and price == i.get('price'):
                    logger_file('error',f"添加的商品{name}已存在！")
                    break
            else:
                file_write('cargo.txt', [item])
                logger_file('warning',f"成功添加新商品{name}！")
                self.return_cargo()
                # self.cargo.productNameEdit.clear()
                # self.cargo.amountLineEdit.clear()
                # self.cargo.priceLineEdit.clear()
        except Exception as e:
            logger_file('error',f"新商品添加失败！错误为{e}")

    def return_cargo(self):
        self.close()
        from logic_code.cargomanagement import CargomanagementWindow
        self.cargomanage = CargomanagementWindow()
        self.cargomanage.show()
        logger_file('info',"管理员返回到货物管理界面")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    staff = NewCargoWindow()
    staff.show()
    sys.exit(app.exec_())
