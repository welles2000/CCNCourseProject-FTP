import os
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

class WinTree:

    def __init__(self, path, win_path, tree, win_menu, win_dir_entry):
        self.path = path
        self.win_path = win_path
        self.tree = tree
        self.win_menu = win_menu
        self.win_dir_entry = win_dir_entry

        self.dir_color_bg = "white"
        self.dir_color_fg = "black"
        self.dir_img = tk.PhotoImage(file="../resources/dir_pic4.png")
        self.return_img = tk.PhotoImage(file="../resources/return_pic.png")
        self.file_img = tk.PhotoImage(file="../resources/file_pic.png")


        # # 滚动条
        # sy = tk.Scrollbar(self.left_frame)
        # sy.pack(side=tk.RIGHT, fill=tk.Y)
        # sy.config(command=self.tree.yview)
        # self.tree.config(yscrollcommand=sy.set)

        # 绑定事件
        self.tree.bind("<<TreeviewSelect>>", self.func)
        self.tree.bind("<Double-Button-1>", self.double_click_func)
        self.tree.bind('<Button-3>',  self.popout)
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.ev = tk.Variable()
        print(self.ev)







    def popout(self, event):
        # 先判断选的这个是文件or文件夹
        self.v = event.widget.selection()
        print(self.v)
        txt = self.tree.item(self.v[0], 'tags')
        print(txt)
        self.win_menu.post(event.x_root, event.y_root)
        if txt == ('dir',):
            pass

    def double_click_func(self, event):
        self.sel = event.widget.selection()  # 'I001'、'I002'
        for sv in self.sel:
            apath = self.tree.item(sv)["values"][0].replace('/', '\\')
            print(apath)
        if self.sel:
            txt = self.tree.item(self.sel[0], 'tags')
            print(self.sel, '  ', txt)
            if txt == ('dir',):
                table = self.tree
                items = table.get_children()
                [table.delete(item) for item in items]
                print("complete clean!")
                self.base_root = self.tree.insert("", "end", text='返回上一级', open=True, values=('返回上一级',), tags=('return',), image=self.return_img)
                if os.path.isdir(apath):
                    os.environ['WIN_CURRENT_PATH'] = apath
                    # self.dir_root = self.tree.insert("", "end", text=self.getlastpath(apath, ), open=True, values=(apath,), tags='dir', image=self.dir_img)
                    # self.tree.tag_configure('dir', background=self.dir_color_bg, foreground=self.dir_color_fg)
                self.loadtree('', apath)
                self.win_dir_entry.delete(0, 'end')
                self.win_dir_entry.insert(0, apath)
            elif txt == ('file', ):
                try:
                    print("打开文件")
                    os.startfile(apath)
                except:
                    showinfo("错误提示", "未选择路径！")



    def show_wenjian(self):
        self.base_root = self.tree.insert("", "end", text='返回上一级', open=True, values=('返回上一级',), tags=('return',), image=self.return_img)
        if os.path.isdir(self.path):
            # self.root = self.tree.insert("", "end", text=self.getlastpath(self.path, ), open=True, values=(self.path,), tags='dir', image=self.dir_img)
            # self.tree.tag_configure('dir', background=self.dir_color_bg, foreground=self.dir_color_fg)
            os.environ['WIN_CURRENT_PATH'] = self.path
        self.loadtree('', self.path)
        # print(self.root)

    def func(self, event):
        # widget触发事件的构建
        self.v = event.widget.selection()
        print(self.v)

        txt = self.tree.item(self.v[0], 'tags')
        # print(txt)
        if txt == ('return',):
            current_dir_path = os.environ['WIN_CURRENT_PATH']
            lastpath = self.getlastpath(current_dir_path)
            formalpath = current_dir_path.replace(lastpath, "")
            formalpath = formalpath[:-1]
            print("返回上级目录")
            print(formalpath)
            self.win_dir_entry.delete(0, 'end')
            self.win_dir_entry.insert(0, formalpath)
            # self.win_path.clear()
            # self.win_path.append(formalpath)

            table = self.tree
            items = table.get_children()
            [table.delete(item) for item in items]
            print("complete clean!")
            self.base_root = self.tree.insert("", "end", text='返回上一级', open=True, values=('返回上一级',), tags=('return',), image=self.return_img)
            if os.path.isdir(formalpath):
                # self.dir_root = self.tree.insert("", "end", text=self.getlastpath(formalpath, ), open=True, values=(formalpath,), tags='dir', image=self.dir_img)
                # self.tree.tag_configure('dir', background=self.dir_color_bg, foreground=self.dir_color_fg)
                os.environ['WIN_CURRENT_PATH'] = formalpath
            self.loadtree('', formalpath)

        else:
            if txt == ('dir', ):
                os.environ['WIN_CHOOSE_FILE_TYPE'] = 'dir'
            else:
                os.environ['WIN_CHOOSE_FILE_TYPE'] = 'file'
            for sv in self.v:
                # file = self.tree.item(sv)["text"].replace('/', '\\')
                # self.ev.set(file)
                print(sv)
                apath = self.tree.item(sv)["values"][0].replace('/', '\\')
                os.environ['WIN_CHOOSE_FILE'] = apath
                # self.win_path.clear()
                # self.win_path.append(apath)
                # print(self.win_path)
                print(apath)  # 点击树中项目后获得的字符串


    def loadtree(self, parent, parentPath):
        os.environ['WIN_CURRENT_PATH'] = parentPath
        for FileName in os.listdir(parentPath):
            absPath = os.path.join(parentPath, FileName)
            if ("$" in absPath) == False:
                if os.path.isdir(absPath):
                    # 插入树枝
                    treey = self.tree.insert(parent, "end", text=self.getlastpath(absPath), values=(absPath, ), tags='dir', image=self.dir_img)
                    self.tree.tag_configure('windir', background=self.dir_color_bg, foreground=self.dir_color_fg)
                else:
                    treey = self.tree.insert(parent, "end", text=self.getlastpath(absPath), values=(absPath, ), tags='file', image=self.file_img)


                # # 判断是否是目录，是的话，递归调用
                # if os.path.isdir(absPath):
                #     self.tree.tag_configure(absPath, background='yellow')
                #     self.loadtree(treey, absPath)
                #     self.tree.item(treey)["tags"] = "dir"

    def getlastpath(self, path):
        pathList = os.path.split(path) # 把path分解了，取最后一级别目录
        return pathList[-1]


