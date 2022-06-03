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
        self.label01 = Label(self, text="百战程序员", width=10, height=2,
                             bg="black", fg="white")
        self.label01.pack()

        self.label02 = Label(self, text="林浩宇", width=10, height=2,
                             bg="blue", fg="white", font=("微软雅黑", 30))
        self.label02.pack()

        # 显示图像
        global photo   # 一定得这样，不然这图片调用完这个方法就被销毁了
        photo = PhotoImage(file="../../resources/SHU1.gif")
        self.label03 = Label(self, image=photo)
        self.label03.pack()

        self.label04 = Label(self, text="lhylhylhylhy\nyjxyjxyjxyjx\nlhylhylhylhy", borderwidth=5, relief="groove", justify="right")
        self.label04.pack()




if __name__ == '__main__':
    root = Tk()
    root.geometry("1280x720+200+300")
    root.title("Label测试")
    app = Application(master=root)
    root.mainloop()
