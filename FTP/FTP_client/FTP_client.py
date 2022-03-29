import socket
import optparse
import configparser  #做记录用的模块，用来做文件处理
import json
import zipfile
import os,sys
import time

#存放状态码的大字典
STATUS_CODE = {
    250:"Invalid cmd format, e.g:{'action':'get','filename':'test.py','size':344}",
    251:'Invalid cmd',
    252:'Invalide auth data',
    253:'Wrong username or password',
    254:'Password authentication',
    255:"Filename doesn't provided",
    256:"Filename donen't exist on server",
    257:'ready to send file',
    258:'md5 verification',

    800:'The file exist,but not enough, is continue?',
    801:'The file exist!',
    802:'Ready to receive datas',

    900:'md5 valdate sucess'
}


class ClientHandler():
    def __init__(self):
        self.op=optparse.OptionParser()  #创建一个optparse对象

        #命令解析
        self.op.add_option('-s','--server',dest='server', default = '127.0.0.1')  #IP地址
        self.op.add_option('-P','--port',dest='port', default = '9000')  #端口
        self.op.add_option('-u','--username',dest='username', default = 'view')  #用户名
        self.op.add_option('-p','--password',dest='password', default = '123')  #登陆密码

        self.options,self.args = self.op.parse_args()  #接收解析结果,赋给两个属性变量

        self.verify_args(self.options,self.args)
        self.make_connection()  #开始连接服务端
        self.mainPath = os.path.dirname(os.path.abspath(__file__))  #存放当前执行文件的绝对路径

    #校验参数
    def verify_args(self,options,args):
        server = options.server  #取4个解析结果
        port = options.port
        #username = options.username
        #password = options.password
        if int(port)>0 and int(port)<65535:  #判断端口是否书写正确
            return True  #没错就返回True，继续往下运行
        else:
            exit('您输入的端口格式错误！')  #用exit退出并且输出错误信息

    #开始连接服务端
    def make_connection(self):
        self.sock = socket.socket()  #创建socket对象
        self.sock.connect((self.options.server,int(self.options.port)))  #连接IP和端口


    #交互
    def interactive(self):
        print('正在开始进入交互......')
        if self.authenticate():  #首先开始验证
                 #功能大循环
            while True:
                cmd_info = input('[%s]'%self.current_dir).strip()  #获取命令信息

                cmd_list = cmd_info.split()  #放到命令清单里面
                #判断是否在定义的命令里面
                if hasattr(self,cmd_list[0]):
                    func = getattr(self,cmd_list[0])
                    if cmd_list[0] == 'put':
                        action, local_path, target_path = cmd_list  # 分别存放操作名，文件名，目标路径名
                        func(action, local_path, target_path)
                    elif cmd_list[0] == 'putDir':
                        action, local_path, target_path = cmd_list  # 分别存放操作名，文件名，目标路径名
                        func(action, local_path, target_path)
                    else:
                        func(*cmd_list)  #执行命令,传入的是个元组

    # Download
    def get(self, *cmd_list):  # 传入的是个元组
        action, target_path, file_name, local_path = cmd_list  #分别存放操作名，文件名，目标路径名
        if target_path == '.':
            target_path = ''
        if local_path == '.':
            local_path = ''

        data_send = {
            'action': 'get',
            'file_name': file_name,
            'target_path': target_path
        }
        self.sock.sendall(json.dumps(data_send).encode('utf-8'))  # 发送输入的文件信息给服务端


        file_info = self.sock.recv(1024).strip()  # 接收
        file_info = json.loads(file_info.decode('utf-8'))  # 将数据变成json字符串来传输
        print(file_info)

        file_name = file_info.get('file_name')
        file_size = file_info.get('file_size')

        abs_path = os.path.join(self.mainPath, local_path, file_name)
        has_received = 0

        if os.path.exists(abs_path):  # 判断文件是否存在,已存在就考虑要不要断点续传
            file_has_size = os.stat(abs_path).st_size  # 获取已经存在文件的大小
            if file_has_size < file_size:  # 已存在小于原文件大小，说明需要断点续传
                self.sock.sendall('800'.encode('utf-8'))  # 文件存在但不完全的状态码
                choice = input('这个文件已存在部分，需要断点续传吗？（Y/N）').strip()
                if choice == 'Y' or 'y':
                    self.sock.sendall('Y'.encode('utf-8'))  # 接收用户是否续传的指令
                    has_received += file_has_size  # 将已经存在的部分加到以接收变量中
                    self.sock.sendall(str(file_has_size).encode('utf-8'))  # 把已经存在的部分发给客户端
                    f = open(abs_path, 'ab')  # 以追加的方式打开

                else:
                    f = open(abs_path, 'wb')
                    # 以写二进制的方式打开,然后就会进入while写入文件

            else:  # 说明已经存在完整的文件
                self.sock.sendall('801'.encode('utf-8'))  # 文件已经存在的状态码
                choice = input('文件已存在，是否覆盖？（Y/N）').strip()
                if choice == 'Y' or 'y':
                    self.sock.sendall('Y'.encode('utf-8'))
                    f = open(abs_path, 'wb')  # 以写二进制的方式打开
                elif choice == 'N' or 'n':
                    self.sock.sendall('N'.encode('utf-8'))
                    return
                else:
                    return

        else:  # 不存在就直接写入
            self.sock.sendall('802'.encode('utf-8'))  # 文件不存在的状态码，不存在文件就直接上传
            f = open(abs_path, 'wb')  # 以写二进制的方式打开

        # 写入文件
        while has_received < file_size:
            # 做一异常处理，根据系统不同值有可能会为空
            try:
                data = self.sock.recv(1024)
            except Exception as e:
                break
                # 如果捕捉到空，就跳出循环,这样就算客户端终止了，服务端也不会报错，会正常运行
            f.write(data)
            has_received += len(data)
            self.show_progress(has_received, file_size)

        f.close()
        print('完毕！')




    # Upload
    def put(self, action, local_path, target_path):  #传入的是个元组
        # action,local_path,target_path = cmd_list  #分别存放操作名，文件名，目标路径名
        if target_path == '.':
            target_path = ''
        #把绝对路径与相对路径拼接，组成本地路径的绝对路径
        local_path = os.path.join(self.mainPath,local_path)

        file_name = os.path.basename(local_path)  #获取目录下的文件名
        file_size = os.stat(local_path).st_size  #获取文件大小

        #打包信息
        data={
            'action':'put',
            'file_name':file_name,
            'file_size':file_size,
            'target_path':target_path
        }

        self.sock.send(json.dumps(data).encode('utf-8'))  #发送输入的文件信息给服务端

        #接收客户端判断文件是否存在的回应
        is_exist = self.sock.recv(1024).decode('utf-8')

        has_sent = 0  #记录光标位置
        if is_exist == '800':
            #文件不完整
            choice = input('这个文件已存在部分，需要断点续传吗？（Y/N）').strip()
            if choice == 'Y' or 'y':
                # self.sock.sendall('Y'.decode('utf-8'))
                self.sock.sendall('Y'.encode('utf-8'))
                #记录存在的位置
                continue_position = self.sock.recv(1024).decode('utf-8')  #接收已经存在的部分的长度
                has_sent += int(continue_position)  #加到已经发送的文件
                
            else:
                self.sock.sendall('N'.encode('utf-8'))
            

        elif is_exist == '801':
            #文件完全存在
            choice = input('文件已存在，是否覆盖？（Y/N）').strip()
            if choice == 'Y' or 'y':
                self.sock.sendall('Y'.encode('utf-8'))
            elif choice == 'N' or 'n':
                self.sock.sendall('N'.encode('utf-8'))
            else:
                return

        else:  #状态码为802的情况
            #文件完全不存在，就从0开始上传
            pass

        #读取文件
        f = open(local_path,'rb')
        f.seek(has_sent)
        #定位光标到已经发送的部分的尾部，再用while传给客户端剩下需要写入的部分
        while has_sent<file_size:
            data = f.read(1024)
            self.sock.sendall(data)
            has_sent += len(data)
            #传输过程中调用进度条显示,传入已经接受的大小和完整文件大小
            self.show_progress(has_sent,file_size)
            
            
        f.close()
        
        print("完毕！")

    def putDir(self, action, local_dir, target_path):
        # 递归
        if target_path == '.':
            target_path = ''
        if not os.path.isdir(local_dir):
            return
        src_target = os.path.join(target_path, local_dir)
        cmd_list = [src_target]
        self.mkdir(self, *cmd_list)
        time.sleep(0.1)
        for file in os.listdir(local_dir):
            src = os.path.join(local_dir, file)
            if os.path.isfile(src):
                self.put('put', src, src_target)
                time.sleep(0.1)
            elif os.path.isdir(src):
                try:
                    self.putDir('putDir', src, target_path)
                except:
                    return

    # 打印进度条
    def show_progress(self,has,total):
        rate = float(has)/float(total)
        rate_num = int(rate*100)  #将进度百分比乘100
        sys.stdout.write("%s%% %s\r" %(rate_num,"#"*rate_num))

    # ls查看文件夹内的文件
    def ls(self,*cmd_list):
        data = {
            "action":"ls"
            }
        self.sock.send(json.dumps(data).encode('utf-8'))  #传输指令
        data = self.sock.recv(1024).decode('utf-8')  #接收结果
        print('当前目录下的文件有：',data)


    #cd切换文件夹功能
    def cd(self,*cmd_list):
        data={
            "action":"cd",
            "dirname":cmd_list[1]  #输入的是一个列表，取列表的第2个元素，用下标1
            }
        self.sock.send(json.dumps(data).encode('utf-8'))  #传输指令
        data = self.sock.recv(1024).decode('utf-8')  #接收结果
        print('当前所在目录：',os.path.basename(data))  #传来的是所在的绝对路径，basename取得最后一级的路径
        #让前标不是家目录，而是cd过后的那个目录
        self.current_dir = os.path.basename(data)


    #创建文件mkdir功能
    def mkdir(self,*cmd_list):
        data = {
            "action":"mkdir",
            "dirname":cmd_list[1]
            }
        self.sock.send(json.dumps(data).encode('utf-8'))  #传输指令
        data = self.sock.recv(1024).decode('utf-8')  #接收结果
        print(data)

        
    #登陆验证
    def authenticate(self):
        if self.options.username is None or self.options.password is None:
            #如果账号密码为空的话就要求用户重新输入一遍
            username=input('Username：')
            password=input('Password：')
            return self.get_auth_result(username,password)  #输入后就返回
        #如果账号密码本身就有值，就直接返回
        return self.get_auth_result(self.options.username,self.options.password)

    #处理服务端的回应信息
    def response(self):
        data = self.sock.recv(1024).decode('utf-8')  #接收信息
        data = json.loads(data)  #将json字符串解码
        return data  #返回处理后的信息

    #获取回应信息
    def get_auth_result(self,user,pwd):
        #将数据发给服务端
        data={
                'action':'auth',
                'username':user,
                'password':pwd
            }
        self.sock.send(json.dumps(data).encode('utf-8'))  #发送账号密码给服务端
        response = self.response()
        print('状态码:',response['status_code'])

        #登陆成功
        if response['status_code'] == 254:  #如果验证成功的话
            self.user = user  #user就代表了通过验证的user
            self.current_dir = user
            print(STATUS_CODE[254])  #输出验证成功的状态
            return True  #并返回代表登陆成功的布尔值
        else:
            print(STATUS_CODE[response['status_code']])
        

ch = ClientHandler()  #实例化对象

ch.interactive()  #调用交互的方法
