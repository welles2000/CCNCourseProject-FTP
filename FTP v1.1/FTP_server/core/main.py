import optparse  #解析命令行命令的模块
import socketserver
from conf import settings  #存IP和端口的模块
from core import server  #存多线程通信类的模块

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

        
