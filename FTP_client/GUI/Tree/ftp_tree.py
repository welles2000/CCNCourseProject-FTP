import os
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showwarning
from ftplib import FTP  # 加载ftp模块
import sys

class FtpTree:

    def __init__(self, ftp_path,  tree_ftp, client_ftp, ftp_menu, ftp_dir_entry):

        self.tree = tree_ftp
        self.ftp_path = ftp_path
        self.client_ftp = client_ftp
        self.ftp_menu = ftp_menu
        self.ftp_dir_entry = ftp_dir_entry
        self.dir_color_bg = "white"
        self.dir_color_fg = "black"

        self.dir_img = tk.PhotoImage(file="../resources/dir_pic4.png")
        self.return_img = tk.PhotoImage(file="../resources/return_pic.png")
        self.file_img = tk.PhotoImage(file="../resources/file_pic.png")
        self.used_size = None  # 已经使用的空间大小
        self.upper_limit_size = None  # 最大空间上限


        # # 滚动条
        # sy = tk.Scrollbar(self.right_frame)
        # sy.pack(side=tk.LEFT, fill=tk.Y)
        # sy.config(command=self.tree.yview)
        # self.tree.config(yscrollcommand=sy.set)

        # 绑定事件
        self.tree.bind("<<TreeviewSelect>>", self.func)
        self.tree.bind("<Double-Button-1>", self.double_click_func)
        self.tree.bind('<Button-3>', self.popout)
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.ev = tk.Variable()
        print(self.ev)

    def popout(self, event):
        # 先判断选的这个是文件or文件夹
        self.v = event.widget.selection()
        print(self.v)
        txt = self.tree.item(self.v[0], 'tags')
        print(txt)
        self.ftp_menu.post(event.x_root, event.y_root)
        if txt == ('dir',):
            pass

    def double_click_func(self, event):
        self.sel = event.widget.selection()  # 'I001'、'I002'
        for sv in self.sel:
            # apath = self.base_dir + f"\" +self.tree.item(sv)["text"]
            apath = os.path.join(self.current_dir,self.tree.item(sv)["text"])

        if self.sel:
            txt = self.tree.item(self.sel[0], 'tags')
            print(self.sel, '  ', txt)
            if txt == ('dir',):
                print('试图切换至路径：' + apath)
                response, dic = self.client_ftp.cd(apath)
                if (response == 260):
                    self.current_dir = apath
                    os.environ['FTP_CURRENT_PATH'] = apath
                    # print(dic)
                    table = self.tree
                    items = table.get_children()
                    [table.delete(item) for item in items]
                    print("complete clean!")

                    self.base_root = self.tree.insert("", "end", text='返回上一级', open=True, values=('返回上一级',),
                                                      tags=('return',), image=self.return_img)
                    # self.dir_root = self.tree.insert("", "end", text=self.getlastpath(dic['dirname'], ), open=True,
                    #                                  values=(apath,),tags='ftp_dir', image=self.dir_img)
                    # self.tree.tag_configure('ftp_dir', background=self.dir_color_bg, foreground=self.dir_color_fg)
                    self.loadtree('', dic)
                    self.ftp_dir_entry.delete(0, "end")
                    self.ftp_dir_entry.insert(0, apath)
                else:
                    # tk.messagebox.showinfo("登录", STATUS_CODE[self.ftp.get_auth_result(user_name, pass_name)])
                    result = showwarning('警告', '无法找到对应的文件夹')
                    print(f'警告:{result}')

            elif txt == 'file':
                pass


    def show_wenjian(self, dic):
        self.base_root = self.tree.insert("", "end", text='返回上一级', open=True, values=('返回上一级',),
                            tags=('return',), image=self.return_img)
        # self.root = self.tree.insert("", "end", text=self.getlastpath(dic['dirname']), open=True, values=(dic['dirname'],), tags='ftp_dir', image=self.dir_img)
        self.current_dir = dic['dirname'] # 当前所在文件夹路径
        os.environ['FTP_CURRENT_PATH'] = dic['dirname']
        # self.tree.tag_configure('ftp_dir', background=self.dir_color_bg, foreground=self.dir_color_fg)
        self.loadtree('', dic)

    def func(self, event):
        # widget触发事件的构建
        self.v = event.widget.selection()
        for sv in self.v:
            file = self.tree.item(sv)["text"].replace('/', '\\')
            self.ev.set(file)
            apath = self.tree.item(sv)["values"][0].replace('/', '\\')
            self.ftp_path.clear()
            self.ftp_path.append(apath)
            # print(self.ftp_path)
            print(apath)

        if apath == '返回上一级' :
            try_dir_path = os.path.dirname(self.current_dir)
            print('试图切换至路径：' + try_dir_path)
            response, dic = self.client_ftp.cd(try_dir_path)
            if (response == 260):
                self.current_dir = try_dir_path
                os.environ['FTP_CURRENT_PATH'] = try_dir_path
                # print(dic)
                table = self.tree
                items = table.get_children()
                [table.delete(item) for item in items]
                print("complete clean!")

                self.base_root = self.tree.insert("", "end", text='返回上一级', open=True, values=('返回上一级',),
                                                  tags=('return',), image=self.return_img)
                # self.dir_root = self.tree.insert("", "end", text=self.getlastpath(dic['dirname'], ), open=True,
                #                                  values=(try_dir_path,),tags='ftp_dir', image=self.dir_img)
                # self.tree.tag_configure('dir', background=self.dir_color_bg, foreground=self.dir_color_fg)
                self.loadtree('', dic)
                self.ftp_dir_entry.delete(0, "end")
                self.ftp_dir_entry.insert(0, try_dir_path)
            else:
                # tk.messagebox.showinfo("登录", STATUS_CODE[self.ftp.get_auth_result(user_name, pass_name)])
                result = showwarning('警告', '无法找到对应的文件夹')
                print(f'警告:{result}')
        else:
            os.environ['FTP_CHOOSE_FILE'] = apath
            type = self.tree.item(self.v[0], 'tags')[0]
            os.environ['FTP_CHOOSE_FILE_TYPE'] = type


    def loadtree(self, parent, dic):
        direname = dic['dirname']
        filelist = dic['filelist']
        isdir = dic['isdir']
        filesize = dic['filesize']
        for i in range(len(filelist)):
            if isdir[i] == True:
                # 插入树枝
                treey = self.tree.insert(parent, "end", text=self.getlastpath(filelist[i]), values=(self.getlastpath(filelist[i]), ), tags='dir', image=self.dir_img)
                self.tree.tag_configure('dir', background=self.dir_color_bg, foreground=self.dir_color_fg)
            else:
                treey = self.tree.insert(parent, "end", text=self.getlastpath(filelist[i]), values=(self.getlastpath(filelist[i]), ), tags='file', image=self.file_img)


            # # 判断是否是目录，是的话，递归调用
            # if os.path.isdir(absPath):
            #
            #     self.loadtree(treey, absPath)

    def getlastpath(self, path):

        pathList = os.path.split(path) # 把path分解了，取最后一级别目录
        return pathList[-1]

    def dir_entry(self, apath):
        response, dic = self.client_ftp.cd(apath)
        if (response == 260):
            self.current_dir = apath
            os.environ['FTP_CURRENT_PATH'] = apath
            # print(dic)
            table = self.tree
            items = table.get_children()
            [table.delete(item) for item in items]
            print("complete clean!")

            self.base_root = self.tree.insert("", "end", text='返回上一级', open=True, values=('返回上一级',),
                                              tags=('return',), image=self.return_img)
            # self.dir_root = self.tree.insert("", "end", text=self.getlastpath(dic['dirname'], ), open=True,
            #                                  values=(apath,),tags='ftp_dir', image=self.dir_img)
            # self.tree.tag_configure('ftp_dir', background=self.dir_color_bg, foreground=self.dir_color_fg)
            self.loadtree('', dic)
            return response
        else:
            # tk.messagebox.showinfo("登录", STATUS_CODE[self.ftp.get_auth_result(user_name, pass_name)])
            result = showwarning('警告', '无法找到对应的文件夹')
            print(f'警告:{result}')
            return response

    def update(self,dic): # 用于更新树
        # print(dic)
        table = self.tree
        items = table.get_children()
        [table.delete(item) for item in items]
        print("complete clean!")

        self.base_root = self.tree.insert("", "end", text='返回上一级', open=True, values=('返回上一级',),
                                          tags=('return',), image=self.return_img)
        # self.dir_root = self.tree.insert("", "end", text=self.getlastpath(dic['dirname'], ), open=True,
        #                                  values=(apath,),tags='ftp_dir', image=self.dir_img)
        # self.tree.tag_configure('ftp_dir', background=self.dir_color_bg, foreground=self.dir_color_fg)
        self.loadtree('', dic)



