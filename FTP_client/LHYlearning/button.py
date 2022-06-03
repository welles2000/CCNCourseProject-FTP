# 经典面向对象的GUI写法

from tkinter import *
from tkinter import messagebox


class Application(Frame):
    """一个经典的GUI程序"""
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createWidget()

    def createWidget(self):
        """创建组件"""
        self.btn01 = Button(self,text="登录",
                            width=6, height=3, anchor=NE, command=self.login) # 要传master，即放在哪
        self.btn01.pack()

        global photo
        photo = PhotoImage(file="../../resources/SHU2.gif")

        self.btn02 = Button(self,image=photo,command=self.login)
        self.btn02.pack()
        self.btn02.config(state="disabled")

        # 创建一个退出按钮
        self.btnQuit = Button(self, text="退出", command=self.master.destroy)
        self.btnQuit.pack()
    def login(self):
        messagebox.showinfo("登录","您已经登录")


if __name__ == '__main__':
    root = Tk()
    root.geometry("1280x720+200+300")
    root.title("")
    app = Application(master=root)
    root.mainloop()
