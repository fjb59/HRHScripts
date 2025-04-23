import io

from PyQt5 import QtCore
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QDialog, QLabel

#import tkinter as tk
#import tkinter.font as tkFont
import defaults

class App(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        if not self.objectName():
            self.setObjectName(u"Dialog")
        self.resize(600, 300)
        if parent != None:
            self.setParent(parent)
        #setting title
        self.title("Id3 Tagger config")
        #setting window size
        width=600
        height=300
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)

        self.lblTag=QLabel(self,"Tag")
        self.lblTag.setGeometry(QRect(190,70,70,25))

        tag_var = tk.StringVar()
        edtTag=tk.Entry(root,textvariable=tag_var)
        edtTag["borderwidth"] = "1px"
        edtTag["fg"] = "#003300"
        edtTag["justify"] = "right"
        edtTag.place(x=310,y=70,width=70,height=25)

        lbST=tk.Label(root)
        lbST["justify"] = "left"
        lbST["text"] = "Show Title"
        lbST.place(x=210,y=110,width=70,height=25)

        stVar = tk.StringVar()
        edtST=tk.Entry(root, textvariable=stVar)
        edtST["borderwidth"] = "1px"
        edtST["justify"] = "right"
        edtST["fg"] = "#003300"
        edtST.place(x=310,y=110,width=75,height=30)

        lblSA=tk.Label(root)
        lblSA["justify"] = "left"
        lblSA["text"] = "Show Artist"
        lblSA.place(x=210,y=140,width=70,height=25)

        saVar=tk.StringVar()
        edtSA=tk.Entry(root, textvariable=saVar)
        edtSA["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        edtSA["font"] = ft
        edtSA["fg"] = "#003300"
        edtSA["justify"] = "right"
        edtSA.place(x=310,y=140,width=70,height=25)

        lblAA=tk.Label(root)
        lblAA["justify"] = "left"
        lblAA["text"] = "Album Artist"
        lblAA.place(x=210,y=170,width=70,height=25)

        aaVar=tk.StringVar()
        edtAA=tk.Entry(root, textvariable=aaVar)
        edtAA["borderwidth"] = "1px"
        edtAA["fg"] = "#003300"
        edtAA["justify"] = "right"
        edtAA.place(x=310,y=170,width=70,height=25)

        btnSave=tk.Button(root)
        btnSave["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        btnSave["font"] = ft
        btnSave["fg"] = "#00dd00"
        btnSave["justify"] = "center"
        btnSave["text"] = "Save"
        btnSave.place(x=210,y=220,width=70,height=25)
        btnSave["command"] = lambda: self.btnSave_command(root,tag_var.get(),stVar.get(),saVar.get(),aaVar.get())

    def btnSave_command(self,tWindow,tag,st,sa,aa):
        print(f"command {tag}:{st}:{sa}:{aa}")
        with  io.open(defaults.confPath,mode="w") as handle:
            print(defaults.taggerName,file=handle)
            print(tag,file=handle)
            print(st,file=handle)
            print(sa,file=handle)
            print(aa,file=handle)
            handle.close()
            tWindow.quit()



# if __name__ == "__main__":
#     # root = tk.Tk()
#     # app = App(root)
#     # root.mainloop()
