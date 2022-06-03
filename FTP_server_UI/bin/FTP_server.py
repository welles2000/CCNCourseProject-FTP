import os, sys

#core不是与FTP_server在同一级目录下，直接这样写from core import main就是错误的
#必须要自行添加环境变量
PATH=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  #获取需要添加的环境地址
sys.path.append(PATH)  #追加环境变量
from core import main  #导入main模块

if __name__ == '__main__':
    main.ArgvHandler()  #调用main下的类
