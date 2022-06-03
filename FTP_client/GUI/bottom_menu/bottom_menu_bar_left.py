import tkinter as tk
import os
from tkinter.messagebox import showinfo
from FTP_client.GUI.Tree.win_tree import WinTree
from FTP_client.GUI.Tree.ftp_tree import FtpTree

class BottomMenuBarleft:

    def __init__(self, bommot_frame_left, menubar):
        self.bommot_frame_left = bommot_frame_left
        self.menubar = menubar

    # 创建本地目录
    def win_chuangjian_mulu(self, win_path, xuanzhe_win_path, tree):
        def win_mulu_button():

            def mulu_but(): # 这个放在前面是因为后面有函数要调用它，放后面要报错
                try:
                    mulu_name = str(mulu_entry.get())
                    os.mkdir(win_path[0] + "\\" + mulu_name)

                    table = tree
                    items = table.get_children()
                    [table.delete(item) for item in items]

                    wintree = WinTree(win_path[0], win_path, tree)
                    wintree.show_wenjian()

                except:
                    showinfo("错误提示", "未选择路径或文件名重复")
                finally:
                    cj_mulu_win.destroy()

            print(win_path)
            if win_path:  #先判断有没有预先点选择本地目录，否则不知道在哪创建
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




        win_mulu_but = tk.Button(self.bommot_frame_left, text="创建目录", font=("宋体", 13), command=win_mulu_button, relief="flat")
        win_mulu_but.place(x=10, y=2)

    # 创建本地文件
    def win_chuangjian_wenjian(self, win_path, xuanzhe_win_path, tree):
        def win_wenjian_button():
            def wenjian_but():
                try:
                    wenjian_name = str(wenjian_entry.get())
                    f = open(win_path[0] + "\\" + wenjian_name, "w")
                    f.close()
                    # 刷新树
                    table = tree
                    items = table.get_children()
                    [table.delete(item) for item in items]

                    wintree = WinTree(win_path[0], win_path, tree)
                    wintree.show_wenjian()

                    # cj_wenjian_win.destroy()
                except:
                    showinfo("错误提示", "未选择路径！")
                finally:
                    cj_wenjian_win.destroy()
            if win_path:  # 先判断有没有预先点选择本地目录，否则不知道在哪创建
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

        win_wenjian_but = tk.Button(self.bommot_frame_left, text="创建文件", font=("宋体", 13), command=win_wenjian_button, relief="flat")
        win_wenjian_but.place(x=10, y=35)

    # 删除目录
    def win_delete_mulu(self, win_path, xuanzhe_win_path, tree):
        def win_mulu_delete_button():
            try:
                path = win_path[0] # 点击选择本地文件夹后选择的文件夹
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
                table = tree
                items = table.get_children()
                [table.delete(item) for item in items]

                wintree = WinTree(win_path[0], win_path, tree)
                wintree.show_wenjian()
            except:
                showinfo("错误提示", "未选择路径！")

        win_delete_mu_but = tk.Button(self.bommot_frame_left, text="删除", font=("宋体", 13), command=win_mulu_delete_button, relief="flat")
        win_delete_mu_but.place(x=115, y=2)

    # 打开文件
    def open_wenjian(self, win_path):
        def win_open_wenjian_button():
            try:
                os.startfile(rf"{win_path[0]}")
            except:
                showinfo("错误提示", "未选择路径！")

        win_open_wenjian_but = tk.Button(self.bommot_frame_left, text="打开文件", font=("宋体", 13),
                                         command=win_open_wenjian_button, relief="flat")
        win_open_wenjian_but.place(x=110, y=35)

    def gexian(self):
        tk.Label(self.bommot_frame_left, text="w|\ni|\nn|", font=("宋体", 13)).place(x=335, y=1)

    # 上传文件
    # def shangchaung(self, ftp_path, ftp_list, win_path, bommot_frame_center, tree_ftp):
    #     def shangchaung_button():
    #         try:
    #             print(ftp_list[0].pwd().encode('iso-8859-1').decode('GB18030'), '-----===------..>>>', win_path[0])
    #             print(ftp_list[0],
    #                   ftp_list[0].pwd().encode('iso-8859-1').decode('GB18030') + "/" + win_path[0].split("\\")[-1],
    #                   win_path[0], "----------==============-----------------==========")
    #             ftp_object = ftp_list[0]
    #             local_path = win_path[0]
    #             target_path = ftp_path[0]
    #             ftp_object.put(('put', local_path, target_path))
    #
    #
    #
    #             # 更新进度条函数
    #             def change_schedule(now_schedule, all_schedule):
    #                 canvas.coords(fill_rec, (5, 5, 6 + (now_schedule / all_schedule) * 100, 25))
    #                 bommot_frame_center.update()
    #                 x.set(str(round(now_schedule / all_schedule * 100, 2)) + '%')
    #                 if round(now_schedule / all_schedule * 100, 2) == 100.00:
    #                     x.set("完==成==了")
    #
    #             canvas = tk.Canvas(bommot_frame_center, width=110, height=30, bg="white")
    #             canvas.place(x=150, y=25)
    #             x = tk.StringVar()
    #             # 进度条以及完成程度
    #             out_rec = canvas.create_rectangle(5, 5, 105, 25, outline="blue", width=1)
    #             fill_rec = canvas.create_rectangle(5, 5, 5, 25, outline="", width=0, fill="blue")
    #
    #             tk.Label(bommot_frame_center, textvariable=x, font=("宋体", 13)).place(x=280, y=30)
    #
    #             for i in range(100):
    #                 change_schedule(i, 99)
    #
    #             if str(ftp_list[0].pwd().encode('iso-8859-1').decode('GB18030')) != "/":
    #                 table = tree_ftp
    #                 items = table.get_children()
    #                 [table.delete(item) for item in items]
    #                 ftptree = FtpTree(ftp_path, ftp_list, tree_ftp)
    #                 ftptree.xianshi(ftp_list[0].pwd().encode('iso-8859-1').decode('GB18030'))
    #             else:
    #                 table = tree_ftp
    #                 items = table.get_children()
    #                 [table.delete(item) for item in items]
    #                 ftptree = FtpTree(ftp_path, ftp_list, tree_ftp)
    #                 ftptree.xianshi("/")
    #         except Exception as e:
    #             if '451' in e:
    #                 if str(ftp_list[0].pwd().encode('iso-8859-1').decode('GB18030')) != "/":
    #                     table = tree_ftp
    #                     items = table.get_children()
    #                     [table.delete(item) for item in items]
    #                     ftptree = FtpTree(ftp_path, ftp_list, tree_ftp)
    #                     ftptree.xianshi(ftp_list[0].pwd().encode('iso-8859-1').decode('GB18030'))
    #                 else:
    #                     table = tree_ftp
    #                     items = table.get_children()
    #                     [table.delete(item) for item in items]
    #                     ftptree = FtpTree(ftp_path, ftp_list, tree_ftp)
    #                     ftptree.xianshi("/")
    #             else:
    #                 print(e)
    #                 showinfo("错误提示", f"本地路径或服务器连接异常!")
    #
    #     shangchaung_but = tk.Button(self.bommot_frame_left, text="上传文件", font=("宋体", 13),
    #                                 command=shangchaung_button, relief="flat")
    #     shangchaung_but.place(x=220, y=2)

