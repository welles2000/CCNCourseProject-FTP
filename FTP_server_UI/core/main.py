import optparse  #解析命令行命令的模块
import socketserver
from conf import settings  #存IP和端口的模块
from core import server  #存多线程通信类的模块
import configparser
import os

#参数处理
class ArgvHandler():
    def __init__(self):
        self.op=optparse.OptionParser()  #建立一个解析命令行命令的对象

        #获取命令,此处不需要，因为已经在settings文件中设置好了参数
        '''
        self.op.add_option("-s","--server",dest="server")  #获取ip地址
        self.op.add_option("-P","--port",dest="port")  #获取端口
        '''
        
        #参数解析
        options,args = self.op.parse_args()  #将解析结果赋给两个变量
        #输出测试
        '''
        print(type(options))  #并不是字典，而是一个被封装成了一个对象
        #print(options.server)  #所以取值应该用属性的方法来取，而不是键值对的方法取
        print(options)
        print(args)
        '''
        
        self.verify_args(options,args)  #验证参数

    #验证参数    
    def verify_args(self,options,args):  #将获取的参数传入
        cmd = args[0]  #获取启动命令

        #判断命令是否存在,存在就执行
        if hasattr(self,cmd):
            func = getattr(self,cmd)  #如果存在if就通过，然后获取该命令的函数名
            func()  #执行该命令函数

    #在之后无论定义多少个命令函数，都只验证一次就出结果，而不需要像if一样多次验证
    #启动就是启动socketserver，开始连接
    def start(self):
        print('the server is working!')
        s = socketserver.ThreadingTCPServer((settings.IP,settings.PORT),server.ServerHandler)
        s.serve_forever()  #开启多线程通信

    def help(self):
        pass

    def setspace(self):
        print('Setspacing...')
        username = input('Username:')
        spacelimit = input('Upper storage limit:')
        cfg = self.read_cfg()
        cfg.set(username, "Upper_storage_limit", spacelimit)  # 使用set直接修改指定字段值
        cfg.write(open(settings.ACCOUNT_PATH, 'w'))

    def database(self):
        #用户存储上限
        #剩余空间
        print('Users Information:')
        username = input('username:')
        cfg = self.read_cfg()
        print(cfg.read(settings.ACCOUNT_PATH))
        path = os.path.join(settings.BASE_DIR,'home',username)
        used_size = self.used_storage(path)
        print('used_size......',used_size)
        used_size = used_size / 1024 / 1024
        size = cfg.get(username,'Upper_storage_limit')
        remain_size = int(size) - used_size
        print(f'"{username}"的总空间为 {size}M，已使用空间为{used_size}M，剩余空间为{remain_size}M')


    def used_storage(self,path):
        print('当前路径:',path)
        size = 0
        name_lst = os.listdir(path)
        for name in name_lst:
            abs_path = os.path.join(path, name)
            if os.path.isfile(abs_path):
                size += os.path.getsize(abs_path)  # 当目标为文件时，计算文件大小
            else:
                size += used_storage(abs_path)  # 当目标为路径时，递归
        return size


    def read_cfg(self):
        cfg = configparser.ConfigParser()  # 取配置文件
        try:
            cfg.read(settings.ACCOUNT_PATH)  # 读取配置信息,就是保存账号密码的文件
        except Exception as e:
            print(e)
        return  cfg
