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
        self.label01 = Label(self, text="用户名")
        self.label01.pack()

        # StringVar变量绑定到指定组件，双向关联
        v1 = StringVar() # StringVar   DoubleVar   IntVar   BooleanVar
        self.entry01 = Entry(self, textvariable=v1)
        self.entry01.pack()
        v1.set("admin")

        # 创建密码框
        self.label02 = Label(self, text="密码")
        self.label02.pack()

        # StringVar变量绑定到指定组件，双向关联
        v2 = StringVar()  # StringVar   DoubleVar   IntVar   BooleanVar
        self.entry02 = Entry(self, textvariable=v2, show="*")
        self.entry02.pack()


        self.btn01 = Button(self, text="登录", command=self.login)
        self.btn01.pack()

        # 创建一个退出按钮
        self.btnQuit = Button(self, text="退出", command=self.master.destroy)
        self.btnQuit.pack()

    def login(self):
        username = self.entry01.get()
        pwd = self.entry02.get()
        print("用户名："+username)
        print("密码："+pwd)

        if username == "lhy" and pwd == "whl":
            messagebox.showinfo("登录界面", "您已登录，欢迎")
        else:
            messagebox.showinfo("登录界面", "密码错误")






if __name__ == '__main__':
    root = Tk()
    root.geometry("1280x720+200+300")
    root.title("")
    app = Application(master=root)
    root.mainloop()
