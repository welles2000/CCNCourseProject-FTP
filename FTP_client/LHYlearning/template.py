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
        # 创建一个退出按钮
        self.btnQuit = Button(self, text="退出", command=self.master.destroy)
        self.btnQuit.pack()


if __name__ == '__main__':
    root = Tk()
    root.geometry("1280x720+200+300")
    root.title("")
    app = Application(master=root)
    root.mainloop()
