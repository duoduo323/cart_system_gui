import sys
from PyQt5.Qt import QApplication
from logic_code.startpage import StartWindow
from tool_code.loggerOut import logger_file


# 注意需要在tool_code.mysql_connect.py的ConnectTable类中初始化定义时改一下连接数据库的ip、数据库名、密码等

def run():
    app = QApplication(sys.argv)
    start = StartWindow()
    start.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    logger_file('info', "=================欢迎来到购物车管理系统主界面！=================")
    run()
