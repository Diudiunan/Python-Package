import tkinter as tk
import Main

autowindow = tk.Tk()
autowindow.title("Auto PLoter")
autowindow.geometry('400x500')

#输入
e = tk.Entry(autowindow, show=None)
e.pack()

#显示
t = tk.Text(autowindow,height=2)
t.pack()

def OKPot():
    Val = e.get()
    t.delete("1.0", "end")
    NVA = Main.GETB(Val)
    t.insert("end", NVA)

def DOIT():
    VAL = t.get("1.0", "end")
    Main.GOMain(VAL)

#按钮
BShow = tk.Button(autowindow, text="确认", command=OKPot)
BShow.pack()

BShow = tk.Button(autowindow, text="确认生成", command=DOIT)
BShow.pack()

autowindow.mainloop()
