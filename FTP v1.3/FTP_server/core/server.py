import socketserver
import json
import configparser  #引入配置模块
import struct

from conf import settings
import os

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


class ServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        #接收验证消息
        while True:
            data = self.recvd()
            # obj = self.request.recv(4)
            # header_size = struct.unpack('i', obj)[0]
            # data = self.request.recv(header_size).strip()  #接收
            # data = json.loads(data.decode('utf-8'))  #将数据变成json字符串来传输
            '''
                {
                    'action':'auth',
                    'pwd':234,
                    'username':'ViewIn'
                }
            '''
            if data.get('action'):   #判断命令有无值
                
                #判断命令是否存在定义的命令里
                if hasattr(self,data.get('action')):  #还需传入发来命令的值
                    func = getattr(self,data.get('action'))
                    func(**data)  #运行该命令,并传入所有定义的命令
                else:
                    print('你的action没有对应的值！')
            else:
                print('你的action没有内容！')

    def sendd(self, data):
        header_json = json.dumps(data).encode('utf-8')
        self.request.sendall(struct.pack('i', len(header_json)))  # 发送输入的文件信息给服务端
        self.request.sendall(header_json)

    def recvd(self):
        obj = self.request.recv(4)
        header_size = struct.unpack('i', obj)[0]
        file_info = self.request.recv(header_size).strip()  # 接收
        file_info = json.loads(file_info.decode('utf-8'))  # 将数据变成json字符串来传输
        return file_info

    #给客户端返回信息
    def send_response(self,state_code):
        response={'status_code':state_code}  #存放状态码

        # self.request.sendall(json.dumps(response).encode('utf-8'))  #发送一个存状态码的键值对
        self.sendd(response)
    
    #登陆验证
    def auth(self,**data):
        print('data:',data)  #输出客户端发来的消息
        username=data['username']  #用键值对取对方发来的消息的值
        password=data['password']

        #开始验证
        user = self.authendicate(username,password)  #运行判断函数
        if user:  #保证密码不是空
            self.send_response(254)  #254验证成功的状态码，调用response发送状态码
        else:
            self.send_response(253)  #验证失败的状态码

    #账号密码匹配验证
    def authendicate(self,user,pwd):
        cfg = configparser.ConfigParser()  #取配置文件
        cfg.read(settings.ACCOUNT_PATH)  #读取配置信息,就是保存账号密码的文件

        #判断用户名是否在配置文件中
        if user in cfg.sections():  #如果在里面就比较密码是否正确
            if cfg[user]['Password'] == pwd:  #取配置文件中的密码,pwd的接收的密码
                self.user = user  #登陆成功后user就代表了传来的user
                self.mainPath = os.path.join(settings.BASE_DIR,'home',self.user)
                #拼接成用户文件的相对路径
                print('登陆成功！')
                return user  #如果成功就返回用户名

    def get(self, **data):
        print('data:', data)  # 打印传来的文件相关信息,是一个字典
        # 解析字典
        file_name = data.get('file_name')
        target_path = data.get('target_path')
        # 拼接成绝对路径
        local_path = os.path.join(self.mainPath, target_path, file_name)

        if not os.path.exists(local_path):
            self.request.sendall('0'.encode('utf-8'))
            return
        else:
            self.request.sendall('1'.encode('utf-8'))

        file_name = os.path.basename(local_path)  # 获取目录下的文件名
        file_size = os.stat(local_path).st_size  # 获取文件大小

        data = {
            'action': 'get',
            'file_name': file_name,
            'file_size': file_size
        }

        # header_json = json.dumps(data).encode('utf-8')
        # self.request.sendall(struct.pack('i', len(header_json)))  # 发送输入的文件信息给服务端
        # self.request.sendall(header_json)
        self.sendd(data)

        flag = self.request.recv(1).decode('utf-8')
        if flag == '0':
            return
        else:
            pass

        is_exist = self.request.recv(3).decode('utf-8')
        has_sent = 0  # 记录已下载的文件的大小

        if is_exist == '800':
            # 文件不完整
            choice = self.request.recv(1).decode('utf-8')  # 接收用户是否续传的指令
            if choice == 'Y' or 'y':
                # 记录存在的位置
                # obj = self.request.recv(4)
                # header_size = struct.unpack('i', obj)[0]
                # data = self.request.recv(header_size).strip()  # 接收
                # data = json.loads(data.decode('utf-8'))  # 将数据变成json字符串来传输
                data = self.recvd()
                continue_position = data.get('file_has_size')

                # continue_position = self.request.recv(1024).decode('utf-8')  # 接收已经存在的部分的长度
                has_sent += int(continue_position)  # 加到已经发送的文件

            else:
                return

        elif is_exist == '801':
            # 文件完全存在
            choice = self.request.recv(1).decode('utf-8')  #接收用户是否覆盖的指令
            if choice == 'Y' or 'y':
                pass
            else:
                return

        else:  # 状态码为802的情况
            # 文件完全不存在，就从0开始上传
            pass

        # 读取文件

        f = open(local_path, 'rb')
        f.seek(has_sent)
        # 定位光标到已经发送的部分的尾部，再用while传给客户端剩下需要写入的部分
        while has_sent < file_size:
            data = f.read(file_size - has_sent)
            self.request.sendall(data)
            has_sent += len(data)

        f.close()

    #文件交互——存放文件
    def put(self,**data):
        print('data:',data)  #打印传来的文件相关信息,是一个字典
        #解析字典
        file_name = data.get('file_name')
        file_size = data.get('file_size')
        target_path = data.get('target_path')

        flag = self.request.recv(1).decode('utf-8')
        if flag == '0':
            return
        else:
            pass
        #拼接成绝对路径
        abs_path = os.path.join(self.mainPath,target_path,file_name)

        if not os.path.exists(abs_path):
            self.request.send('0'.encode('utf-8'))
            return
        else:
            self.request.send('1'.encode('utf-8'))


        has_received = 0  #记录已上传的文件的大小
        
        #传入文件
        if os.path.exists(abs_path):  #判断文件是否存在,已存在就考虑要不要断点续传
            file_has_size = os.stat(abs_path).st_size  #获取已经存在文件的大小
            if file_has_size<file_size:  #已存在小于原文件大小，说明需要断点续传
                self.request.sendall('800'.encode('utf-8'))  #文件存在但不完全的状态码
                choice = self.request.recv(1).decode('utf-8')  #接收用户是否续传的指令
                if choice == 'Y':
                    data = {
                        'file_has_size': file_has_size
                    }
                    # self.request.sendall(str(file_has_size).encode('utf-8'))  #把已经存在的部分发给客户端
                    self.sendd(data)
                    has_received += file_has_size  #将已经存在的部分加到以接收变量中
                    

                    f = open(abs_path,'ab')  #以追加的方式打开
                else:
                    f = open(abs_path,'wb')
                    #以写二进制的方式打开,然后就会进入while写入文件
                
            else:  #说明已经存在完整的文件
                self.request.sendall('801'.encode('utf-8'))  #文件已经存在的状态码
                choice = self.request.recv(1).decode('utf-8')  # 接收用户是否续传的指令
                if choice == 'N':
                    return  # 并且直接返回，不运行下面写入文件操作
                else:
                    has_received = 0
                    f = open(abs_path, 'wb')  # 以写二进制的方式打开

        
        else:  #不存在就直接写入
            self.request.sendall('802'.encode('utf-8'))  #文件不存在的状态码，不存在文件就直接上传
            f = open(abs_path,'wb')  #以写二进制的方式打开

        #写入文件
        while has_received < file_size:
            #做一异常处理，根据系统不同值有可能会为空
            try:
                data = self.request.recv(file_size - has_received)
            except Exception as e:
                break
                #如果捕捉到空，就跳出循环,这样就算客户端终止了，服务端也不会报错，会正常运行
            f.write(data)
            has_received += len(data)

        f.close()

    #ls查看文件夹下的文件
    def ls(self,**data):  #因为传入的是一个字典，所以用**data
        file_list = os.listdir(self.mainPath)  #查看传入的登陆用户路径下的所有文件
        file_str = '\n'.join(file_list)  #一行一个文件名，拼接字符串，每一个文件用一个换行来连接
        if not len(file_list):
            file_str="<空文件夹！>"
        file_str_dic = {
            'file_str_dic': file_str
        }
        self.sendd(file_str_dic)
        # self.request.sendall(file_str.encode('utf-8'))

    def lsall(self, **data):  #因为传入的是一个字典，所以用**data
        nl = []
        allfilelist = []
        allfilelist_rel = []
        basepath = data.get('basepath')
        basepath = os.path.join(self.mainPath, basepath)
        file_list = os.listdir(basepath)  #查看传入的登陆用户路径下的所有文件
        for file in file_list:
            nl.append(os.path.join(basepath, file))
        for file in nl:
            allfilelist.append(file)
            if os.path.isdir(file):
                for f in os.listdir(file):
                    nl.append(os.path.join(file, f))
        del_str = self.mainPath + '\\'
        for file in allfilelist:
            allfilelist_rel.append(file.replace(del_str, ''))
        dic = {}
        dic['index'] = allfilelist_rel

        # header_json = json.dumps(dic).encode('utf-8')
        # self.request.sendall(struct.pack('i', len(header_json)))  # 发送输入的文件信息给服务端
        # self.request.sendall(header_json)
        self.sendd(dic)

    #cd切换路径
    def cd(self,**data):
        dirname = data.get("dirname")  #获取目录名
        if dirname=='..':  #如果是..就返回上一级目录
            self.mainPath = os.path.dirname(self.mainPath)
        else:
            #进行路径拼接,得到绝对路径
            self.mainPath = os.path.join(self.mainPath,dirname)
        data = {
            'mainPath': self.mainPath
        }
        # self.request.sendall(self.mainPath.encode('utf-8'))
        self.sendd(data)

    #mkdir创建目录
    def mkdir(self,**data):
        dirname = data.get('dirname')
        path = os.path.join(self.mainPath,dirname)  #拼接路径（成绝对路径）
        if not os.path.exists(path):  #如果文件夹存在的话
            #开始创建文件夹
            if '/' in dirname:  #如果你输入了多级目录，就创建多级目录
                os.makedirs(path)
            else:
                os.mkdir(path)  #否则就创建单级目录
            self.request.sendall('目录创建成功！'.encode('utf-8'))
        else:
            self.request.sendall('目录已经存在！'.encode('utf-8'))
