import pickle
import tkinter as tk
import base64
from FTP_client.FTP_client import ClientHandler
from tkinter import ttk
from tkinter.messagebox import showinfo
from FTP_client.GUI.Tree.win_tree import WinTree
from FTP_client.GUI.Tree.ftp_tree import FtpTree
import os

import tkinter.filedialog as fi

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

    300:'Username has existed',
    301:'Register success',

    800:'The file exist,but not enough, is continue?',
    801:'The file exist!',
    802:'Ready to receive datas',

    900:'md5 valdate sucess'
}

class TopMenuBar:
    def __init__(self, top_frame, path, win, win_search_path, ftp_list, xuanzhe_win_path, menubar, win_menu, ftp_menu, tree, ftptree, win_dir_entry, ftp_dir_entry, progressbarOne, storage_lab,scale):
        self.top_frame = top_frame
        self.path = path
        self.win = win
        self.win_search_path = win_search_path
        self.ftp_list = ftp_list
        self.xuanzhe_win_path = xuanzhe_win_path
        self.menubar = menubar
        self.win_menu = win_menu
        self.win_menu.add_command(label="上传", command=self.upload)
        self.menubar.add_command(label="创建目录", command=self.win_mkdir)
        self.menubar.add_command(label="创建文件", command=self.win_mkfile)
        self.win_menu.add_command(label="删除", command=self.win_del)
        self.ftp_menu = ftp_menu
        self.ftp_menu.add_command(label='下载', command=self.download)
        self.ftp_menu.add_command(label="删除", command=self.ftp_del)
        self.tree = tree
        self.ftptree = ftptree
        self.win_dir_entry = win_dir_entry
        self.ftp_dir_entry = ftp_dir_entry

        self.dir_img = tk.PhotoImage(file="../resources/dir_pic4.png")
        self.return_img = tk.PhotoImage(file="../resources/return_pic.png")
        self.file_img = tk.PhotoImage(file="../resources/file_pic.png")

        self.progressbarOne = progressbarOne
        self.progressbarOne['value'] = 0

        self.scale = scale

        self.storage_lab = storage_lab
        # top_frame.update()

    # 注册
    def register(self):
        def register_but():
            wind = tk.Tk()
            wind.geometry("400x370+500+200")
            wind.tk.call("source", "../../sun-valley.tcl")
            wind.tk.call("set_theme", "light")
            titile_lab = tk.Label(wind, text="ftp注册", font=("宋体", 19))
            titile_lab.place(x=150, y=30)

            user_name_lab = tk.Label(wind, text="用户名:", font=("宋体", 15))
            user_name_lab.place(x=55, y=90)
            user_name_entry = tk.Entry(wind, font=("宋体", 15))
            user_name_entry.place(x=130, y=90)

            pass_name_lab = tk.Label(wind, text="密码:", font=("宋体", 15))
            pass_name_lab.place(x=55, y=130)
            pass_name_entry = tk.Entry(wind, show="*", font=("宋体", 15))
            pass_name_entry.place(x=130, y=130)

            pass_name_lab_conf = tk.Label(wind, text="确认密码:", font=("宋体", 15))
            pass_name_lab_conf.place(x=35, y=170)
            pass_name_conf_entry = tk.Entry(wind, show="*", font=("宋体", 15))
            pass_name_conf_entry.place(x=130, y=170)

            def register_call():
                self.ftp_list.clear()
                user_name = str(user_name_entry.get())
                pass_name = str(pass_name_entry.get())
                pass_name_conf = str(pass_name_conf_entry.get())

                if pass_name_conf != pass_name:
                    tk.messagebox.showinfo("提示", "两次密码不一致，请重新输入")
                    register_but()
                else:
                    ftp_register = ClientHandler()
                    ftp_register.make_connection("127.0.0.1", 9000)
                    response = ftp_register._register_(user_name, pass_name_conf)
                    showinfo("注册", "状态码："+STATUS_CODE[response['status_code']]+"  "+"空间容量："+response['upper_storage_limit']+"MB")
                    # print(response['status_code'])
                    # print(response['upper_storage_limit'])
                    # print(response['used_size'])
                    # print(response['remain_size'])


                    wind.destroy()

            d_but = tk.Button(wind, text="注册", font=("宋体", 15), command=register_call)
            d_but.place(x=180, y=250)
            wind.mainloop()

        self.menubar.add_command(label='注册', command=register_but)




    # logo
    def logo(self):
        logo_lable = tk.Label(self.top_frame, text="FTP客户端", font=("微软雅黑", 20), fg="blue")
        logo_lable.place(x=5, y=3)

    # window目录选择按钮
    def local_mulu(self, win_path, tree):
        # 目录选择按钮的回调函数
        def mulu_button():
            self.xuanzhe_win_path.clear()
            DEF_PATH = ""
            newDir = fi.askdirectory(initialdir=DEF_PATH, title="打开目录").replace('/', '\\')
            print(newDir)
            DEF_PATH = newDir
            if len(newDir) == 0:
                return
            print(DEF_PATH)
            self.xuanzhe_win_path.append(DEF_PATH)
            # win_path.append(DEF_PATH)
            print(self.xuanzhe_win_path)
            os.environ['WIN_CURRENT_PATH'] = DEF_PATH
            os.environ['WIN_CURRENT_STATUS'] = "choosed"
            self.win_dir_entry.delete(0, 'end')
            self.win_dir_entry.insert(0, DEF_PATH)

            table = self.tree
            items = table.get_children()
            [table.delete(item) for item in items]
            self.wintree = WinTree(self.xuanzhe_win_path[0], win_path, self.tree, self.win_menu, self.win_dir_entry)
            self.wintree.show_wenjian()

        self.menubar.add_command(label='选择本地文件夹', command=mulu_button)


    # 打开文件按钮，未在主界面放置
    def open_wenjian(self):
        def open_wenjian_button():
            pass

        open_wenjian_but = tk.Button(self.top_frame, text="选择本地文件", font=("宋体", 13), command=open_wenjian_button,
                                     relief="flat")
        open_wenjian_but.place(x=220, y=30)

    # ip,port显示
    def name_ip(self, bieming, ip):
        name = bieming
        name_lable = tk.Label(self.top_frame, text=f"user: {name}", font=("宋体", 13))
        name_lable.place(x=400, y=5)
        ip = ip
        ip_lable = tk.Label(self.top_frame, text=f"ip: {ip}", font=("宋体", 13))
        ip_lable.place(x=580, y=5)

    # 登录按钮
    def login_in(self, ftp_path, ftp_list, ftp_tree_list):
        def login_in_button():
            wind = tk.Tk()
            wind.geometry("400x300+500+200")
            wind.tk.call("source", "../../sun-valley.tcl")
            wind.tk.call("set_theme", "light")
            titile_lab = tk.Label(wind, text="ftp登录", font=("宋体", 19))
            titile_lab.place(x=150, y=30)

            # self.ftp_list.clear()

            bieming_lab = tk.Label(wind, text="别名:", font=("宋体", 15))
            bieming_lab.place(x=60, y=90)
            bieming_entry = tk.Entry(wind, font=("宋体", 15))
            bieming_entry.place(x=130, y=90)

            user_name_lab = tk.Label(wind, text="用户名:", font=("宋体", 15))
            user_name_lab.place(x=40, y=130)
            user_name_entry = tk.Entry(wind, font=("宋体", 15))
            user_name_entry.place(x=130, y=130)

            pass_name_lab = tk.Label(wind, text="密码:", font=("宋体", 15))
            pass_name_lab.place(x=60, y=170)
            pass_name_entry = tk.Entry(wind, show="*", font=("宋体", 15))
            pass_name_entry.place(x=130, y=170)




            def d_button():
                self.ftp_list.clear()
                bieming = str(bieming_entry.get())
                user_name = str(user_name_entry.get())
                pass_name = str(pass_name_entry.get())
                ip_name = "127.0.0.1"
                port_name = 9000



                try:
                    # 打开被序列化文件
                    with open("../data/usr_info.pickle", "wb") as usr_file:
                        # 用户数据
                        usr_info = [base64.b64encode(bieming.encode("utf-8")),
                                    base64.b64encode(user_name.encode("utf-8")),
                                    base64.b64encode(pass_name.encode("utf-8")),
                                    base64.b64encode(ip_name.encode("utf-8")),
                                    base64.b64encode(str(port_name).encode("utf-8"))]
                        print(usr_info)
                        # 存储(序列化)数据
                        pickle.dump(usr_info, usr_file)
                except FileNotFoundError:
                    print("存储错误")

                self.name_ip(bieming, ip_name)

                self.ftp_list.clear()
                self.ftp = ClientHandler(self.progressbarOne, self.top_frame,self.scale)
                self.ftp.make_connection(ip_name, port_name) # 进行ftp连接

                response, dic = self.ftp.get_auth_result(user_name, pass_name)
                wind.destroy()
                if(response["status_code"] == 254):
                    print(dic)
                    tk.messagebox.showinfo("登录", "登录成功")
                    os.environ['FTP_CURRENT_STATUS'] = "login"

                    self.ftp_upper_storage_limit = int(response['upper_storage_limit'])
                    self.ftp_used_size = float(response['used_size'])
                    self.change_storage_lab(response['upper_storage_limit'], response['used_size'])

                    # usrpath = r"D:\PythonProjects\classproject-FTP\FTP_server\home"+r"/"+user_name
                    # os.makedirs(usrpath, exist_ok=True)
                    self.ftp_list.clear()
                    self.ftp_list.append(self.ftp)  # 先存起来，暂时没用

                    table = ftp_tree_list[0]
                    items = table.get_children()
                    [table.delete(item) for item in items]

                    self.ftptree = FtpTree(ftp_path, ftp_tree_list[0], self.ftp_list[0], self.ftp_menu, self.ftp_dir_entry)
                    self.ftptree.show_wenjian(dic)
                    ftp_current_dir = os.environ.get('FTP_CURRENT_PATH')
                    self.ftp_dir_entry.delete(0, "end")
                    self.ftp_dir_entry.insert(0, ftp_current_dir)
                    # self.ftptree.used_size = response['used_size']
                    # self.ftptree.upper_limit_size = response['upper_storage_limit']
                    # print('空间容量:', self.ftptree.upper_limit_size)
                    # print('已使用:', self.ftptree.used_size)
                    # print('剩余容量:', )


                else:
                    tk.messagebox.showinfo("登录", STATUS_CODE[self.ftp.get_auth_result(user_name, pass_name)])


            def default_button():
                # 先清除再添加，避免bug
                bieming_entry.delete(0, "end")
                user_name_entry.delete(0, "end")
                pass_name_entry.delete(0, "end")
                bieming_entry.insert(0, "lhy")
                user_name_entry.insert(0, "view")
                pass_name_entry.insert(0, int(123))


            d_but = tk.Button(wind, text="登录", font=("宋体", 15), command=d_button)
            d_but.place(x=60, y=230)
            default_but = tk.Button(wind, text="默认输入", font=("宋体", 15), command=default_button)
            default_but.place(x=200, y=230)

            wind.mainloop()

        self.menubar.add_command(label='登录', command=login_in_button)


    def dir_entry(self):
        self.win_dir_entry.bind("<Return>", self.win_cd)
        self.ftp_dir_entry.bind("<Return>", self.ftp_cd)

    # 本地entry切换目录
    def win_cd(self, ev=None): # 不知道为什么一定要传入俩参数，否则报错，第二个参数没用
        dir_path = str(self.win_dir_entry.get())
        # 先判断有没有点击过选择文件夹，只有点击过才有self.wintree.trere 否则需要重新创建
        if os.environ.get("WIN_CURRENT_PATH") == None:
            if os.path.isdir(dir_path):

                self.xuanzhe_win_path.clear()
                DEF_PATH = ""
                newDir = dir_path
                print(newDir)
                DEF_PATH = newDir
                if len(newDir) == 0:
                    return
                print(DEF_PATH)
                self.xuanzhe_win_path.append(DEF_PATH)
                # win_path.append(DEF_PATH)
                print(self.xuanzhe_win_path)
                os.environ['WIN_CURRENT_PATH'] = DEF_PATH
                os.environ['WIN_CURRENT_STATUS'] = "choosed"

                table = self.tree
                items = table.get_children()
                [table.delete(item) for item in items]
                self.wintree = WinTree(self.xuanzhe_win_path[0], None, self.tree, self.win_menu, self.win_dir_entry)
                self.wintree.show_wenjian()
            else:
                showinfo("注意", "请输入正确的文件夹路径！")
                print("未输入正确路径")
        else:
            print("正在切换目录")
            print("正在切换至" + dir_path)
            try:
                if os.path.isdir(dir_path):
                    print("目标路径存在")
                    # 刷新树
                    table = self.wintree.tree
                    items = table.get_children()
                    [table.delete(item) for item in items]
                    self.wintree.base_root = self.wintree.tree.insert("", "end", text='返回上一级', open=True, values=('返回上一级',),
                                                                      tags=('return',), image=self.return_img)
                    # self.wintree.dir_root = self.wintree.tree.insert("", "end",
                    #                                                  text=self.wintree.getlastpath(dir_path, ),
                    #                                                  open=True,
                    #                                                  values=(dir_path,), tags='dir', image=self.dir_img)
                    # self.wintree.tree.tag_configure('dir', background=self.wintree.dir_color_bg,
                    #                                 foreground=self.wintree.dir_color_fg)
                    self.wintree.loadtree('', dir_path)
                    os.environ['WIN_CURRENT_PATH'] = dir_path
                else:
                    showinfo("注意", "请输入正确的文件夹路径！")

            except:
                showinfo("注意", "请输入正确的文件夹路径！")
                print("异常退出")


    # 云端entry切换目录
    def ftp_cd(self, ev=None): # 不知道为什么一定要传入俩参数，否则报错，第二个参数没用
        dir_path = str(self.ftp_dir_entry.get())
        ftp_current_dir = os.environ.get('FTP_CURRENT_PATH')
        response = self.ftptree.dir_entry(dir_path)
        if response != 260:
            self.ftp_dir_entry.delete(0, "end")
            self.ftp_dir_entry.insert(0, ftp_current_dir)


    # 查看文件或文件夹大小是否超额
    def is_size_max(self,path):
        def calculate_size(path):
            size = 0
            if os.path.isdir(path):
                name_lst = os.listdir(path)
                for name in name_lst:
                    abs_path = os.path.join(path, name)
                    if os.path.isdir(abs_path):
                        size += calculate_size(abs_path)  # 当目标为路径时，递归
                    else:
                        size += os.path.getsize(abs_path)
            else:
                size += os.path.getsize(path)  # 当目标为文件时，计算文件大小
            return size

        size = calculate_size(path)
        size = size / 1024 / 1024
        if size <= self.ftp_upper_storage_limit - self.ftp_used_size :
            return True
        else:
            return False


    # 获得服务端磁盘配额信息
    def _get_quota(self):
        pass
    # 上传文件
    def upload(self):
        ftp_current_dir = os.environ.get('FTP_CURRENT_PATH')
        ftp_file_name = os.environ.get('FTP_CHOOSE_FILE')
        ftp_file_type = os.environ.get('FTP_CHOOSE_FILE_TYPE')
        win_current_dir = os.environ.get('WIN_CURRENT_PATH')


        ####******************
        win_file_name = os.environ.get('WIN_CHOOSE_FILE')
        win_file_type = os.environ.get('WIN_CHOOSE_FILE_TYPE')
        ftp_status = os.environ.get('FTP_CURRENT_STATUS')
        if ftp_status == 'login':
        # 判断文件类型
            if self.is_size_max(win_file_name) == True:  # 判断文件大小是否超过磁盘剩余容量
                if win_file_type == 'file':
                    client_handler = self.ftp_list[0]
                    cmd_list = ['put', win_file_name, ftp_current_dir]  # action, local_path, target_path
                    print('试图上传文件:' + 'from '+win_file_name + 'to ' + ftp_current_dir)
                    sign, dic, response = client_handler.put(cmd_list)  # sign 1表示传递成功 2表示本地路径不存在 3表示云端路径不存在
                    if sign == 1:
                        tk.messagebox.showinfo("文件上传", "上传成功")
                        self.ftp_upper_storage_limit = int(response['upper_storage_limit'])
                        self.ftp_used_size = float(response['used_size'])
                        self.change_storage_lab(response['upper_storage_limit'], response['used_size'])
                        # 刷新云端树
                        table = self.ftptree.tree
                        items = table.get_children()
                        [table.delete(item) for item in items]

                        self.ftptree.base_root = self.ftptree.tree.insert("", "end", text='返回上一级', open=True, values=('返回上一级',),
                                                          tags=('return',), image=self.return_img)
                        # self.ftptree.dir_root = self.ftptree.tree.insert("", "end", text=self.ftptree.getlastpath(dic['dirname'], ), open=True,
                        #                                  values=self.ftptree.getlastpath(dic['dirname'], ), tags='ftp_dir', image=self.dir_img)
                        # self.ftptree.tree.tag_configure('dir', background=self.ftptree.dir_color_bg, foreground=self.ftptree.dir_color_fg)
                        self.ftptree.loadtree('', dic)
                else:
                    client_handler = self.ftp_list[0]
                    local_dir = os.path.basename(win_file_name)
                    dir_path = os.path.dirname(win_file_name)
                    cmdlist = ['putdir',local_dir , ftp_current_dir]  # putdir local_dir target_path
                    response2, dic, storge_response = client_handler.handel_putdir(cmdlist, dir_path)
                    self.ftptree.update(dic)
                    self.ftp_upper_storage_limit = int(storge_response['upper_storage_limit'])
                    self.ftp_used_size = float(storge_response['used_size'])
                    self.change_storage_lab(storge_response['upper_storage_limit'], storge_response['used_size'])

            else:
                tk.messagebox.showwarning('警告', '云端空间不足，无法上传')
        else:
            tk.messagebox.showwarning('警告', '请先选择要上传的位置')

    # 下载文件
    def download(self):
        ftp_current_dir = os.environ.get('FTP_CURRENT_PATH')
        ftp_file_name = os.environ.get('FTP_CHOOSE_FILE')
        ftp_file_type = os.environ.get('FTP_CHOOSE_FILE_TYPE')
        win_current_dir = os.environ.get('WIN_CURRENT_PATH')
        win_file_name = os.environ.get('WIN_CHOOSE_FILE')
        # win_file_type = os.environ.get('WIN_CHOOSE_FILE_TYPE')
        win_status = os.environ.get('WIN_CURRENT_STATUS')

        # print('yjx'+file_name)
        # print('yjx'+file_type)
        # print('yjx'+current_dir)
        # print('lhy' + win_current_dir)

        if win_status == 'choosed':
            # 判断文件类型
            if ftp_file_type == 'file':
                client_handler = self.ftp_list[0]
                file = os.path.join(ftp_current_dir,ftp_file_name)
                cmd_list = ['get', ftp_current_dir, ftp_file_name, win_current_dir]   # action, target_path, file_name, local_path
                print('试图下载文件:'+os.path.join(ftp_current_dir,ftp_file_name))
                sign = client_handler.get(cmd_list) # sign 1表示传递成功 2表示云端路径不存在 3表示本地路径不存在 4表示不继续进行传输 5表示断点续传
                if sign == 1:
                    tk.messagebox.showinfo("文件下载", "下载成功")
                    # wintree = WinTree(win_current_dir, win_file_name, self.tree, self.win_menu)
                    # wintree.show_wenjian()
                    table = self.wintree.tree
                    items = table.get_children()
                    [table.delete(item) for item in items]
                    self.wintree.base_root = self.wintree.tree.insert("", "end", text='返回上一级', open=True, values=('返回上一级',),
                                                      tags=('return',), image=self.return_img)
                    # self.wintree.dir_root = self.wintree.tree.insert("", "end", text=self.wintree.getlastpath(win_current_dir, ), open=True,
                    #                                      values=(win_current_dir,), tags='dir', image=self.dir_img)
                    # self.wintree.tree.tag_configure('dir', background=self.wintree.dir_color_bg, foreground=self.wintree.dir_color_fg)
                    self.wintree.loadtree('', win_current_dir)


            else:
                client_handler = self.ftp_list[0]
                dir = os.path.join(ftp_current_dir,ftp_file_name)
                cmd_list = ['getdir', dir, win_current_dir]
                print('试图下载文件夹:' + dir)
                sign = client_handler.getdir(cmd_list)
                if sign == 1:
                    tk.messagebox.showinfo("文件夹下载", "下载成功")
                    # wintree = WinTree(win_current_dir, win_file_name, self.tree, self.win_menu)
                    # wintree.show_wenjian()
                    table = self.wintree.tree
                    items = table.get_children()
                    [table.delete(item) for item in items]
                    self.wintree.base_root = self.wintree.tree.insert("", "end", text='返回上一级', open=True,
                                                                      values=('返回上一级',),
                                                                      tags=('return',), image=self.return_img)
                    # self.wintree.dir_root = self.wintree.tree.insert("", "end", text=self.wintree.getlastpath(win_current_dir, ), open=True,
                    #                                      values=(win_current_dir,), tags='dir', image=self.dir_img)
                    # self.wintree.tree.tag_configure('dir', background=self.wintree.dir_color_bg, foreground=self.wintree.dir_color_fg)
                    self.wintree.loadtree('', win_current_dir)
                else:
                    print("文件夹已存在")

        else:
            tk.messagebox.showwarning('警告', '请先选择要下载的位置')

    # 创建目录
    def win_mkdir(self):
        current_win_path = os.environ.get("WIN_CURRENT_PATH")
        def mulu_but():  # 这个放在前面是因为后面有函数要调用它，放后面要报错
            try:
                mulu_name = str(mulu_entry.get())
                os.mkdir(current_win_path + "\\" + mulu_name)

                table = self.wintree.tree
                items = table.get_children()
                [table.delete(item) for item in items]

                self.wintree.base_root = self.wintree.tree.insert("", "end", text='返回上一级', open=True, values=('返回上一级',),
                                                                  tags=('return',), image=self.return_img)
                # self.wintree.dir_root = self.wintree.tree.insert("", "end",
                #                                                  text=self.wintree.getlastpath(current_win_path, ),
                #                                                  open=True,
                #                                                  values=(current_win_path,), tags='dir', image=self.dir_img)
                # self.wintree.tree.tag_configure('dir', background=self.wintree.dir_color_bg,
                #                                 foreground=self.wintree.dir_color_fg)
                self.wintree.loadtree('', current_win_path)

            except:
                showinfo("错误提示", "未选择路径或文件名重复")
            finally:
                cj_mulu_win.destroy()

        print(current_win_path)
        if current_win_path:  # 先判断有没有预先点选择本地目录，否则不知道在哪创建
            cj_mulu_win = tk.Tk()
            cj_mulu_win.geometry("300x170+500+350")
            cj_mulu_win.tk.call("source", "../../sun-valley.tcl")
            cj_mulu_win.tk.call("set_theme", "light")

            tk.Label(cj_mulu_win, text="创建目录", font=("宋体", 17)).place(x=100, y=15)
            tk.Label(cj_mulu_win, text="目录名:", font=("宋体", 13)).place(x=30, y=60)
            mulu_entry = tk.Entry(cj_mulu_win, width=17, font=("宋体", 13))
            mulu_entry.place(x=100, y=60)

            mulu_button = tk.Button(cj_mulu_win, text="确==========定", font=("宋体", 13), command=mulu_but)
            mulu_button.place(x=80, y=105)
            cj_mulu_win.mainloop()
        else:
            showinfo("错误提示", "请先选择要创建的位置！")

    # 创建文件
    def win_mkfile(self):
        current_win_path = os.environ.get("WIN_CURRENT_PATH")
        def wenjian_but():
            try:
                wenjian_name = str(wenjian_entry.get())
                f = open(current_win_path + "\\" + wenjian_name, "w")
                f.close()
                # 刷新树
                table = self.wintree.tree
                items = table.get_children()
                [table.delete(item) for item in items]

                self.wintree.base_root = self.wintree.tree.insert("", "end", text='返回上一级', open=True, values=('返回上一级',),
                                                                  tags=('return',), image=self.return_img)
                # self.wintree.dir_root = self.wintree.tree.insert("", "end",
                #                                                  text=self.wintree.getlastpath(current_win_path, ),
                #                                                  open=True,
                #                                                  values=(current_win_path,), tags='dir', image=self.dir_img)
                # self.wintree.tree.tag_configure('dir', background=self.wintree.dir_color_bg,
                #                                 foreground=self.wintree.dir_color_fg)
                self.wintree.loadtree('', current_win_path)

                # cj_wenjian_win.destroy()
            except:
                showinfo("错误提示", "未选择路径！")
            finally:
                cj_wenjian_win.destroy()

        if current_win_path:  # 先判断有没有预先点选择本地目录，否则不知道在哪创建
            cj_wenjian_win = tk.Tk()
            cj_wenjian_win.geometry("300x170+500+350")
            cj_wenjian_win.tk.call("source", "../../sun-valley.tcl")
            cj_wenjian_win.tk.call("set_theme", "light")

            tk.Label(cj_wenjian_win, text="创建文件", font=("宋体", 17)).place(x=100, y=15)
            tk.Label(cj_wenjian_win, text="文件名:", font=("宋体", 13)).place(x=30, y=60)
            wenjian_entry = tk.Entry(cj_wenjian_win, width=17, font=("宋体", 13))
            wenjian_entry.place(x=100, y=60)
            wenjian_button = tk.Button(cj_wenjian_win, text="确==========定", font=("宋体", 13), command=wenjian_but)
            wenjian_button.place(x=80, y=105)
        else:
            showinfo("错误提示", "请先选择要创建的位置！")

    # 删除文件/目录
    def win_del(self):
        current_win_path = os.environ.get("WIN_CURRENT_PATH")
        current_win_file = os.environ.get("WIN_CHOOSE_FILE")
        try:
            path = current_win_file # 点击后选择的文件/文件夹
            # 也可以递归删除文件
            def delAll(path):
                if os.path.isdir(path):
                    files = os.listdir(path)
                    # 遍历并删除文件
                    for file in files:
                        p = os.path.join(path, file)
                        if os.path.isdir(p):
                            # 递归
                            delAll(p)
                        else:
                            os.remove(p)
                    # 删除文件夹
                    os.rmdir(path)
                else:
                    os.remove(path)

            delAll(path)

            # 刷新树
            table = self.wintree.tree
            items = table.get_children()
            [table.delete(item) for item in items]

            self.wintree.base_root = self.wintree.tree.insert("", "end", text='返回上一级', open=True, values=('返回上一级',),
                                                              tags=('return',), image=self.return_img)
            # self.wintree.dir_root = self.wintree.tree.insert("", "end",
            #                                                  text=self.wintree.getlastpath(current_win_path, ),
            #                                                  open=True,
            #                                                  values=(current_win_path,), tags='dir', image=self.dir_img)
            # self.wintree.tree.tag_configure('dir', background=self.wintree.dir_color_bg,
            #                                 foreground=self.wintree.dir_color_fg)
            self.wintree.loadtree('', current_win_path)
        except:
            showinfo("错误提示", "未选择路径！")

        # ftp删除文件/目录
    def ftp_del(self):
        current_ftp_path = os.environ.get("FTP_CURRENT_PATH")
        current_ftp_file = os.environ.get("FTP_CHOOSE_FILE")
        # try:
        client_handler = self.ftp_list[0]
        path = os.path.join(current_ftp_path, current_ftp_file)  # 点击后选择的文件/文件夹
        cmd_list = ['rm',path]
        dic, response = client_handler.rm(cmd_list)
        self.ftp_upper_storage_limit = int(response['upper_storage_limit'])
        self.ftp_used_size = float(response['used_size'])
        self.change_storage_lab(response['upper_storage_limit'], response['used_size'])

        self.ftptree.update(dic)
        # except:
            # showinfo("错误提示", "未选择路径！")

    def change_storage_lab(self, upper_storage_limit, used_size): # 传进来的是str，要改成数字
        # limit = float(upper_storage_limit)
        used_size = float(used_size)
        if used_size < 1 :
            used_size = used_size * 1024
            str_used_size = str(used_size) + 'KB'
        elif used_size < 0.001:
            used_size = used_size * 1024 * 1024
            str_used_size = str(used_size) + 'B'
        else:
            str_used_size = str(used_size) + 'MB'

        text = '磁盘已使用空间：'  + str_used_size + ' / ' + upper_storage_limit + 'MB'
        self.storage_lab['text'] =  text

        self.win.update()


    # 用于创建确认操作框
    # def define_window(self, definition_text):
    #     self.definition = False # 默认为否
    #     wind = tk.Tk()
    #     wind.title("确认操作")
    #     wind.geometry("250x130+500+200")
    #     # wind.tk.call("source", "../../sun-valley.tcl")
    #     # wind.tk.call("set_theme", "light")
    #     # titile_lab = tk.Label(wind, text="确认操作", font=("宋体", 19))
    #     # titile_lab.place(x=150, y=30)
    #     bieming_lab = tk.Label(wind, text=definition_text, font=("宋体", 11))
    #     bieming_lab.place(x=20, y=30)
    #
    #     def definition_yes():
    #         self.definition = True
    #         wind.destroy()
    #
    #     def definition_no():
    #         self.definition = False
    #         wind.destroy()
    #
    #     yes_but = tk.Button(wind, text="是", font=("宋体", 11), command=definition_yes)
    #     yes_but.place(x=80, y=70)
    #     no_but = tk.Button(wind, text="否", font=("宋体", 11), command=definition_no)
    #     no_but.place(x=120, y=70)
    #
    #     wind.mainloop()

