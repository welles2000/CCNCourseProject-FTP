import socket
import optparse
import configparser  #做记录用的模块，用来做文件处理
import json
import zipfile
import os,sys
import struct
import time
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel

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

    259:'Invalid dir',
    260:'Correct dir',

    270:'Succefully delete file or dir',

    280: 'Succefully put file or dir',

    300:'Username has existed',
    301:'Register success',

    800:'The file exist,but not enough, is continue?',
    801:'The file exist!',
    802:'Ready to receive datas',

    900:'md5 valdate sucess'
}


class ClientHandler():
    def __init__(self, progressbarOne=None, frame=None, scale = None):
        self.op=optparse.OptionParser()  #创建一个optparse对象

        #命令解析
        self.op.add_option('-s','--server',dest='server', default = '127.0.0.1')  #IP地址
        self.op.add_option('-P','--port',dest='port', default = '9000')  #端口
        self.op.add_option('-u','--username',dest='username', default = 'view')  #用户名
        self.op.add_option('-p','--password',dest='password', default = '123')  #登陆密码
        self.op.add_option('-r', '--registerFlag', dest='registerFlag', default=0) #注册用户参数，默认不注册

        self.options,self.args = self.op.parse_args()  #接收解析结果,赋给两个属性变量
        self.definition = False

        # self.verify_args(self.options,self.args)
        # self.make_connection()  #开始连接服务端
        self.mainPath = os.path.dirname(os.path.abspath(__file__))  #存放当前执行文件的绝对路径
        self.progressbarOne = progressbarOne
        self.frame = frame
        self.scale = scale


    def sendd(self, data):
        header_json = json.dumps(data).encode('utf-8')
        self.sock.sendall(struct.pack('i', len(header_json)))  # 发送输入的文件信息给服务端
        self.sock.sendall(header_json)

    def recvd(self):
        obj = self.sock.recv(4)
        header_size = struct.unpack('i', obj)[0]
        file_info = self.sock.recv(header_size).strip()  # 接收
        file_info = json.loads(file_info.decode('utf-8'))  # 将数据变成json字符串来传输
        return file_info

    # def isexist_s(self, abs_path):
    #     if not os.path.exists(abs_path):
    #         print('路径不存在')
    #         self.sock.send('0'.encode('utf-8'))
    #         return
    #     else:
    #         self.sock.send('1'.encode('utf-8'))
    #
    # def isexist_r(self):
    #     flag = self.sock.recv(1).decode('utf-8')
    #     if flag == '0':
    #         print('路径不存在')
    #         return
    #     else:
    #         pass

    #校验参数
    def verify_args(self, options, args):
        server = options.server  #取4个解析结果
        port = options.port
        #username = options.username
        #password = options.password
        if int(port)>0 and int(port)<65535:  #判断端口是否书写正确
            return True  #没错就返回True，继续往下运行
        else:
            exit('您输入的端口格式错误！')  #用exit退出并且输出错误信息

    #开始连接服务端
    """myw初始版本"""
    # def make_connection(self):
    #     self.sock = socket.socket()  #创建socket对象
    #     self.sock.connect((self.options.server,int(self.options.port)))  #连接IP和端口

    """lhy适配界面版本"""
    def make_connection(self, ip, port):
        self.sock = socket.socket()  #创建socket对象
        self.sock.connect((ip, int(port)))  #连接IP和端口


    # 注册
    def _register_(self, username, password):
        data = {
            'action': 'register',
            'username': username,
            'password': password
        }

        self.sendd(data)

        response = self.response()
        print('状态码:', response['status_code'])
        print('空间容量:', response['upper_storage_limit'])
        print('已使用:', response['used_size'])
        print('剩余容量:', response['remain_size'])

        return response

    #交互
    def interactive(self):
        print('正在开始进入交互......')

        if int(self.options.registerFlag):
            #开始注册
            print('开始注册')
            print(self.options.username, self.options.password)

            self._register_(self.options.username, self.options.password)
            return
        if self.authenticate():  #首先开始验证
                 #功能大循环
            while True:
                cmd_info = input('[%s]'%self.current_dir).strip()  #获取命令信息

                cmd_list = cmd_info.split()  #放到命令清单里面
                #判断是否在定义的命令里面
                if hasattr(self,cmd_list[0]):
                    func = getattr(self, cmd_list[0])
                    func(*cmd_list)  #执行命令,传入的是个元组
                else:
                    print('不存在该命令，现有get, getdir, put, putdir, ls, lsall, cd, mkdir, ll, rm')

    # Download
    def get(self, cmd_list):  # 传入的是个元组
        sign = 1 # 1表示传递成功 2表示云端路径不存在 3表示本地路径不存在 4表示不继续进行传输 5表示断点续传
        # dic = None
        # if len(cmd_list) != 4:
        #     print('错误命令，应为: get target_path file_name local_path')
        #     sign = 0
        #     return sign
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
        # header_json = json.dumps(data_send).encode('utf-8')
        # self.sock.sendall(struct.pack('i', len(header_json)))  # 发送输入的文件信息给服务端
        # self.sock.sendall(header_json)
        self.sendd(data_send)

        flag = self.sock.recv(1).decode('utf-8')
        if flag == '0':
            print('target_path路径不存在')
            sign = 2
            return sign
        else:
            pass

        # obj = self.sock.recv(4)
        # header_size = struct.unpack('i', obj)[0]
        # file_info = self.sock.recv(header_size).strip()  # 接收
        # file_info = json.loads(file_info.decode('utf-8'))  # 将数据变成json字符串来传输
        file_info = self.recvd()

        print(file_info)

        file_name = file_info.get('file_name')
        file_size = file_info.get('file_size')

        abs_path = os.path.join(self.mainPath, local_path, file_name)
        abs_path1 = os.path.join(self.mainPath, local_path)

        if not os.path.exists(abs_path1):
            self.sock.sendall('0'.encode('utf-8'))
            print('local_path路径不存在')
            sign = 3
            return sign
        else:
            self.sock.sendall('1'.encode('utf-8'))

        has_received = 0

        if os.path.exists(abs_path):  # 判断文件是否存在,已存在就考虑要不要断点续传
            file_has_size = os.stat(abs_path).st_size  # 获取已经存在文件的大小
            if file_has_size < file_size:  # 已存在小于原文件大小，说明需要断点续传
                self.sock.sendall('800'.encode('utf-8'))  # 文件存在但不完全的状态码
                # choice = input('这个文件已存在部分，需要断点续传吗？（Y/N）').strip()
                choice = askokcancel(title='确认选择', message='这个文件已存在部分，需要断点续传吗？')
                if choice == True:
                    self.sock.sendall('Y'.encode('utf-8'))  # 接收用户是否续传的指令
                    has_received += file_has_size  # 将已经存在的部分加到以接收变量中
                    data_has_size = {
                        'file_has_size': file_has_size
                    }
                    # header_json = json.dumps(data_has_size).encode('utf-8')
                    # self.sock.sendall(struct.pack('i', len(header_json)))  # 发送输入的文件信息给服务端
                    # self.sock.sendall(header_json)
                    self.sendd(data_has_size)

                    f = open(abs_path, 'ab')  # 以追加的方式打开

                else:
                    f = open(abs_path, 'wb')
                    # 以写二进制的方式打开,然后就会进入while写入文件

            else:  # 说明已经存在完整的文件
                self.sock.sendall('801'.encode('utf-8'))  # 文件已经存在的状态码
                # choice = input('文件已存在，是否覆盖？（Y/N）').strip()
                choice = askokcancel(title='确认选择', message='文件已存在，是否覆盖？')
                if choice == True:
                    self.sock.sendall('Y'.encode('utf-8'))
                    f = open(abs_path, 'wb')  # 以写二进制的方式打开
                    sign = 5
                elif choice == False:
                    self.sock.sendall('N'.encode('utf-8'))
                    sign = 4
                    return sign
                else:
                    sign = 4
                    return sign

        else:  # 不存在就直接写入
            self.sock.sendall('802'.encode('utf-8'))  # 文件不存在的状态码，不存在文件就直接上传
            f = open(abs_path, 'wb')  # 以写二进制的方式打开

        # 写入文件
        while has_received < file_size:
            # 做一异常处理，根据系统不同值有可能会为空
            try:
                data = self.sock.recv(file_size - has_received)
            except Exception as e:
                break
                # 如果捕捉到空，就跳出循环,这样就算客户端终止了，服务端也不会报错，会正常运行
            f.write(data)
            has_received += len(data)
            self.progressbarOne['value'] = has_received / file_size
            # self.show_progress(has_received, file_size)
            # time.sleep(0.1)
            print('has_received' + str(has_received))
            print('file_size' + str(file_size))

        f.close()
        self.progressbarOne['value'] = 0
        print('完毕！')
        return sign

    def getdir(self, cmd_list):
        sign = 1  # 1表示下载成功 2表示不替换文件夹
        # if len(cmd_list)!= 3:
        #     print('错误命令，应为: getdir target_path local_path')
        #     return
        action, target_path, local_path = cmd_list
        dirname = os.path.basename(target_path)
        dirpath = os.path.join(local_path, dirname)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        else:
            question = askokcancel(title = '确认选择',message='文件夹已存在，是否选择替换')
            print(question)
            if question == False:
                sign = 2
                # print(sign)
                return sign
        cmd_l = ['lsall', target_path]
        file_list = self.lsall(cmd_l)
        print('file_list:{}'.format(file_list))
        for file in file_list:
            name = os.path.basename(file)
            if '.' in name:
                dir = os.path.join('home', self.current_dir, os.path.dirname(file))
                c_list = ['get', dir, name, os.path.join(local_path, os.path.dirname(file))]
                # print(c_list)
                self.get(c_list)
            else:
                dirpath = os.path.join(local_path, file)
                if not os.path.exists(dirpath):
                    os.makedirs(dirpath)
                else:
                    pass

        print("文件夹下载完毕！")
        return sign


    # Upload
    def put(self, cmd_list):  #传入的是个元组
        dic = None
        response = None
        sign = 1
        print(cmd_list)
        # if len(cmd_list)!= 3:
        #
        #     print('错误命令，应为: put local_path target_path')
        #     return
        action, local_path, target_path = cmd_list  #分别存放操作名，文件名，目标路径名
        if target_path == '.':
            target_path = ''
        #把绝对路径与相对路径拼接，组成本地路径的绝对路径
        # local_path = os.path.join(self.mainPath,local_path)
        file_name = os.path.basename(local_path)  #获取目录下的文件名
        if os.path.exists(local_path):
            file_size = os.stat(local_path).st_size  #获取文件大小
        else:
            file_size = 0

        #打包信息
        data={
            'action':'put',
            'file_name':file_name,
            'file_size':file_size,
            'target_path':target_path
        }
        print(data)
        # self.sock.send(json.dumps(data).encode('utf-8'))  #发送输入的文件信息给服务端
        self.sendd(data)

        if not os.path.exists(local_path):
            print('local_path路径不存在')
            sign = 2
            self.sock.send('0'.encode('utf-8'))
            return sign, dic, response
        else:
            self.sock.send('1'.encode('utf-8'))

        flag = self.sock.recv(1).decode('utf-8')
        if flag == '0':
            print('target_path路径不存在')
            sign = 3
            return sign, dic, response
        else:
            pass

        #接收客户端判断文件是否存在的回应
        is_exist = self.sock.recv(3).decode('utf-8')
        has_sent = 0  #记录光标位置
        if is_exist == '800':
            #文件不完整
            # choice = input('这个文件已存在部分，需要断点续传吗？（Y/N）').strip()
            choice = askokcancel(title='确认选择', message='这个文件已存在部分，需要断点续传吗？')
            if choice == 'Y' or 'y':
                # self.sock.sendall('Y'.decode('utf-8'))
                self.sock.sendall('Y'.encode('utf-8'))
                #记录存在的位置
                continue_position = self.recvd().get('file_has_size')
                # continue_position = self.sock.recv(1024).decode('utf-8')  #接收已经存在的部分的长度
                has_sent += int(continue_position)  #加到已经发送的文件
            else:
                self.sock.sendall('N'.encode('utf-8'))
        elif is_exist == '801':
            #文件完全存在
            # choice = input('文件已存在，是否覆盖？（Y/N）').strip()
            choice = askokcancel(title='确认选择', message='文件已存在，是否覆盖？')
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
        f = open(local_path, 'rb')
        f.seek(has_sent)
        #定位光标到已经发送的部分的尾部，再用while传给客户端剩下需要写入的部分
        # speed = (int)((file_size - has_sent) * scale.get() / 100)
        # speed = (int)((file_size - has_sent) * self.scale.get() / 100)
        speed = (int)((file_size - has_sent) * self.scale.get() / 100)
        if speed <=0:
            speed = 1
        while has_sent < file_size:
            try:
                # print(speed)
                data = f.read(speed)
                # print('c1:%d' % len(data))
            except:
                speed = 1
                data = f.read(1)
                print('c2:%d' % len(data))
            sp={
                "speed":speed,
                "len":len(data)
            }
            self.sendd(sp)
            self.sock.sendall(data)
            has_sent += len(data)
            self.progressbarOne['value'] = has_sent / file_size
            self.frame.update()
            #传输过程中调用进度条显示,传入已经接受的大小和完整文件大小
            self.show_progress(has_sent,file_size)
            # time.sleep(0.1)

            print('has_sent'+str(has_sent))
            print('file_size'+str(file_size))

        f.close()
        print("文件上传完毕！")
        response = self.response()
        # print('状态码:', response['status_code'])
        # print('空间容量:', response['upper_storage_limit'])
        # print('已使用:', response['used_size'])
        # print('剩余容量:', response['remain_size'])
        self.progressbarOne['value'] = 0
        dic = self.recvd()
        return sign, dic, response


    # Upload Dir
    def putdir(self, cmd_list):
        if len(cmd_list)!= 3:
            print('错误命令，应为: putdir local_dir target_path')
            return
        action, local_dir, target_path = cmd_list

        # 递归
        if target_path == '.':
            target_path = ''
        if not os.path.isdir(os.path.join(self.dir_path, local_dir)):
            print('带前缀的local_dir: '+os.path.join(self.dir_path, local_dir))
            print('找不到local_dir')
            return
        src_target = os.path.join(target_path, local_dir)
        cmd_list = ['mkdir', src_target]
        self.mkdir(cmd_list)
        # time.sleep(0.1)
        abs_path = os.path.join(self.dir_path, local_dir)
        for file in os.listdir(abs_path):
            src = os.path.join(local_dir, file)
            abs_src = os.path.join(self.dir_path, local_dir, file)
            print('src: '+src)
            print('abs_src: '+abs_src)
            print('src_target: '+src_target)
            if os.path.isfile(abs_src):
                cmd_l = ['put', abs_src, src_target]
                print(cmd_l)
                self.put(cmd_l)
                # time.sleep(0.1)
            elif os.path.isdir(abs_src):
                try:
                    cmd_l = ['putdir', src, target_path]
                    print(cmd_l)
                    self.putdir(cmd_l)
                except:
                    return

    # putdir的处理函数
    def handel_putdir(self, cmdlist, local_path):
        self.dir_path = local_path

        self.putdir(cmdlist)

        response2, dic = self.cd(cmdlist[2])
        return response2, dic, self.storge_response

    # 打印进度条
    def show_progress(self,has,total):
        rate = float(has)/float(total)
        rate_num = int(rate*100)  #将进度百分比乘100
        sys.stdout.write("%s%% %s\r" %(rate_num,"#"*rate_num))

    def lsall(self, basepath):
        # print(cmd_list)
        # action, basepath = cmd_list
        data = {
            "action": "lsall",
            "basepath": basepath
        }
        # header_json = json.dumps(data).encode('utf-8')
        # self.sock.sendall(struct.pack('i', len(header_json)))  # 发送输入的文件信息给服务端
        # self.sock.sendall(header_json)
        self.sendd(data)

        # obj = self.sock.recv(4)
        # header_size = struct.unpack('i', obj)[0]
        # data = self.sock.recv(header_size).strip()  # 接收
        # data = json.loads(data.decode('utf-8'))  # 将数据变成json字符串来传输
        data = self.recvd()

        print(data.get('index'))
        return data.get('index')

    # ls查看文件夹内的文件
    def ls(self,*cmd_list):
        data = {
            "action":"ls"
            }
        # self.sock.send(json.dumps(data).encode('utf-8'))  #传输指令
        self.sendd(data)
        # data = self.sock.recv(1024).decode('utf-8')  #接收结果
        data = self.recvd().get('file_str_dic')
        print('当前目录下的文件有：',data)

    #cd切换文件夹功能
    def cd(self, dir_name):
        data={
            "action":"cd",
            "dirname":dir_name  #输入的是一个列表，取列表的第2个元素，用下标1
            }
        # self.sock.send(json.dumps(data).encode('utf-8'))  #传输指令
        self.sendd(data)

        response = self.response()
        self.storge_response = response   # lpx的代码导致要这样做，只能这么做
        print('状态码:', response['status_code'])
        dic = None

        # 登陆成功
        if response['status_code'] == 260:  # 如果文件夹存在的话
            print(STATUS_CODE[260])  # 输出验证成功的状态
            dic = self.recvd()
            return response['status_code'], dic  # 并返回代表登陆成功的布尔值
        else:
            print(STATUS_CODE[response['status_code']])
            return response['status_code'], dic



        # data = self.sock.recv(1024).decode('utf-8')  #接收结果

        # print('当前所在目录：',os.path.basename(data))  #传来的是所在的绝对路径，basename取得最后一级的路径
        #让前标不是家目录，而是cd过后的那个目录
        # self.current_dir = os.path.basename(data)

    #创建文件mkdir功能
    def mkdir(self,cmd_list):
        data = {
            "action":"mkdir",
            "dirname":cmd_list[1]
            }
        self.sendd(data)
        # self.sock.send(json.dumps(data).encode('utf-8'))  #传输指令
        data = self.sock.recv(21).decode('utf-8')  #接收结果
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
        data = self.recvd()
        # data = self.sock.recv(1024).decode('utf-8')  #接收信息
        # data = json.loads(data)  #将json字符串解码
        return data  #返回处理后的信息

    #显示磁盘配额
    def show_disk(self,data):
        print('空间容量:', data['upper_storage_limit'])
        print('已使用:', data['used_size'])
        print('剩余容量:', data['remain_size'])


    #获取回应信息
    def get_auth_result(self,user,pwd):
        #将数据发给服务端
        data={
                'action':'auth',
                'username':user,
                'password':pwd
            }
        # header_json = json.dumps(data).encode('utf-8')
        # self.sock.send(struct.pack('i', len(header_json)))  #发送账号密码给服务端
        # self.sock.sendall(header_json)
        self.sendd(data)

        response = self.response()
        print('状态码:',response['status_code'])

        self.show_disk(response)
       # *******************************
        dic = None

        #登陆成功
        if response['status_code'] == 254:  #如果验证成功的话
            self.user = user  #user就代表了通过验证的user
            self.current_dir = user
            print(STATUS_CODE[254])  #输出验证成功的状态
            dic = self.recvd()
            return response, dic  #并返回代表登陆成功的布尔值
        else:
            print(STATUS_CODE[response['status_code']])
            return response, dic

    # ll得到所有目录下文件的详细信息
    def ll(self, *cmd_list):
        action, basepath = cmd_list
        data = {
            "action": "ll",
            "basepath": basepath
        }
        # header_json = json.dumps(data).encode('utf-8')
        # self.sock.sendall(struct.pack('i', len(header_json)))  # 发送输入的文件信息给服务端
        # self.sock.sendall(header_json)
        self.sendd(data)

        # obj = self.sock.recv(4)
        # header_size = struct.unpack('i', obj)[0]
        # data = self.sock.recv(header_size).strip()  # 接收
        # data = json.loads(data.decode('utf-8'))  # 将数据变成json字符串来传输
        data = self.recvd()

        print(data.get('index'))
        return data.get('index')

    def rm(self, cmd_list):
        action, basepath = cmd_list
        data = {
            "action": "rm",
            "basepath": basepath
        }
        self.sendd(data)
        response = self.response()
        print('状态码:', response['status_code'])
        print('空间容量:', response['upper_storage_limit'])
        print('已使用:', response['used_size'])
        print('剩余容量:', response['remain_size'])
        dic = self.recvd()
        return dic, response


        

# ch = ClientHandler()  #实例化对象
#
# ch.interactive()  #调用交互的方法
