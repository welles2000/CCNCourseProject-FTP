from tkinter import *
from tkinter import messagebox
root = Tk()

root.title("我的第一个GUI")
root.geometry("500x300+100+200") # 宽x高 距左边多少像素 距上面多少像素

btn01 = Button(root)
btn01["text"] = "点我就送花"

btn01.pack()

def songhua(e): # e为事件对象
    messagebox.showinfo("Message","啦啦啦啦啦")  # 窗口标题  窗口内容
    print("lalalalala")

btn01.bind("<Button-1>",songhua)  # 鼠标左键  绑定函数

root.mainloop()  # 进入事件循环
