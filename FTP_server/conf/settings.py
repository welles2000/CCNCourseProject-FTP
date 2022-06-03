import os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#定义地址和端口
# IP='192.168.43.247'
# PORT=8080
IP='127.0.0.1'
PORT=9000


#指向账户文件路径；并且确定账号、密码
ACCOUNT_PATH = os.path.join(BASE_DIR,'conf','accounts.cfg')
