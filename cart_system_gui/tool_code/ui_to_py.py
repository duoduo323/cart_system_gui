# cart_system_gui PyCharm
# ui_to_py Lenovo
# 2025/8/15 周五 上午9:40


import os

path_qt = os.path.abspath('../qtfile')  # 文件路径
lst = os.listdir(path_qt)   # 文件名全称
# print(lst)
path_py = os.path.abspath('../pyfile')
# print(os.path.abspath('../pyfile/administratorwindow.py'))
for i in lst:
    print(path_qt)
    print(i)
    path_x = os.path.join(path_qt,i)
    path_y = os.path.join(path_py,i.split('.')[0])
    command = f'pyuic5 -x {path_x} -o {path_y}.py'
    # print(command)
    os.system(command)
