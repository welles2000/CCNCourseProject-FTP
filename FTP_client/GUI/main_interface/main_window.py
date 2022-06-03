import tkinter as tk
from tkinter import ttk
from FTP_client.GUI.top_menu.top_menu_bar import TopMenuBar
from FTP_client.GUI.Tree.win_tree import WinTree
from FTP_client.GUI.Tree.ftp_tree import FtpTree
from FTP_client.GUI.bottom_menu.bottom_menu_bar_left import BottomMenuBarleft
import os

win = tk.Tk()
win.title("FTP客户端")
win.geometry("800x600+120+60")
win.resizable(0, 0)
win.tk.call("source","../../sun-valley.tcl")
win.tk.call("set_theme","light")
menubar = tk.Menu(win)
win['menu'] = menubar

win_menu = tk.Menu(win, tearoff=0)
ftp_menu = tk.Menu(win, tearoff=0)


xuanzhe_win_path = [] # 点击选择本地文件夹后的路径

win_path = [] # 点击树后，被点击条目的路径
ftp_path = []
win_search_name = []
win_search_path = []
ftp_search_path = []
ftp_list = []
ftp_tree_list = []
win_xuanze_tree = []
win_search_tree = []
path = "初始化占位"

left_frame = tk.Frame(win, width="350", height="600")
left_frame.place(x=20, y=90)
tree = ttk.Treeview(left_frame, show="tree", height=25)
tree.column("#0", width=350)


def resize(ev=None):
    '''改变label字体大小'''
    # label.config(font='Helvetica -%d bold' % scale.get())
    pass




# tree.column("shijian", width=80)
st = ttk.Style()
st.configure("Treeview", font=("宋体", 13))
# def treeviewClick(event):
#     v = event.widget.selection()
#     for sv in v:
#         apath = tree.item(sv)["values"][0].replace('/', '\\')
#         print(apath)  # 点击树中项目后获得的字符串
#         win_path[0] = apath
# tree.bind('<ButtonRelease-1>', treeviewClick)

top_frame = tk.Frame(win, width="800", height="90")
top_frame.place(x=0, y=5)

label_s = tk.Label(top_frame,text = "速度限制(%):")

label_s.place(x=170,y=20)

scale = tk.Scale(top_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=resize)
scale.set(100)  # 设置初始值
scale.place(x=250,y=0)

# 创建进度条
progressbarOne = ttk.Progressbar(top_frame)
progressbarOne.place(relx=0.05, width=740, height=30, rely=0.75)
progressbarOne['maximum'] = 1
# 进度值初始值
progressbarOne['value'] = 0
# top_frame.update()

win_dir_label = tk.Label(top_frame, text=">", font=("宋体", 15))
win_dir_label.place(x=20, y=50)
win_dir_entry = tk.Entry(top_frame, font=("宋体", 15), width=33)
win_dir_entry.place(x=40, y=50)

ftp_dir_label = tk.Label(top_frame, text=">", font=("宋体", 15))
ftp_dir_label.place(x=385, y=47.5)
ftp_dir_entry = tk.Entry(top_frame, font=("宋体", 15), width=36)
ftp_dir_entry.place(x=405, y=47.5)

win_xuanze_tree.clear()
win_xuanze_tree.append(tree)
wintree = WinTree(path, win_path, tree, win_menu, win_dir_entry) # 看似卵用没有，实则用处是先显示一个空树

right_frame = tk.Frame(win, width="350", height="720")
right_frame.place(x=380, y=90)

tree_ftp = ttk.Treeview(right_frame, show="tree", height=25)
tree_ftp.column("#0", width=350)
# tree_ftp.column("shijian", width=80)
# tree_ftp.column("wenjiantype", width=60)

ftp_tree_list.append(tree_ftp)
st = ttk.Style()
st.configure("Treeview", font=("宋体", 13))
ftptree = FtpTree(ftp_path, tree_ftp, None, ftp_menu, ftp_dir_entry)

# 下边栏的左半部分
# bommot_frame_left = tk.Frame(win, width="350", height="60")
# bommot_frame_left.place(x=0, y=635)
storage_lab = tk.Label(win, text="磁盘所用空间", font=("宋体", 13))
storage_lab.place(x=380, y=570)  #800x720





top_menu = TopMenuBar(top_frame, path, win, win_search_path, ftp_list, xuanzhe_win_path, menubar, win_menu, ftp_menu, tree, ftptree, win_dir_entry, ftp_dir_entry, progressbarOne, storage_lab,scale)
top_menu.logo()

top_menu.name_ip("", "")
top_menu.login_in(ftp_path, ftp_list, ftp_tree_list)
top_menu.register()
top_menu.dir_entry()
top_menu.local_mulu(win_path, tree)

# 下边栏的左半部分。暂时不需要了
# bommot_frame_left = tk.Frame(win, width="350", height="60")
# bommot_frame_left.place(x=0, y=635)

# bommot_menu_left = BottomMenuBarleft(bommot_frame_left, menubar)
# bommot_menu_left.win_chuangjian_mulu(win_path, xuanzhe_win_path, tree)
# bommot_menu_left.win_chuangjian_wenjian(win_path, xuanzhe_win_path, tree)
# bommot_menu_left.win_delete_mulu(win_path, xuanzhe_win_path, tree)
# bommot_menu_left.open_wenjian(win_path)
# bommot_menu_left.gexian()



# def test_current_dir():
#     tk.messagebox.showinfo("测试", os.environ['WIN_CURRENT_PATH'])
#
# test_current_dir_but = tk.Button(top_frame, text="test current dir", command=test_current_dir)
# test_current_dir_but.pack()
#
# def test_current_path():
#     tk.messagebox.showinfo("测试", os.environ['WIN_CHOOSE_FILE'])
#
# test_current_path_but = tk.Button(top_frame, text="test choose file", command=test_current_path)
# test_current_path_but.pack()
#
# def test_file_type():
#     tk.messagebox.showinfo("测试", os.environ['WIN_CHOOSE_FILE_TYPE'])
#
# test_file_type_but = tk.Button(top_frame, text="test choose file type", command=test_file_type)
# test_file_type_but.pack()

tk.mainloop()
