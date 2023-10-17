import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("Id3 Tagger config")
        #setting window size
        width=600
        height=300
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_890=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_890["font"] = ft
        GLabel_890["fg"] = "#333333"
        GLabel_890["justify"] = "left"
        GLabel_890["text"] = "Tag"
        GLabel_890.place(x=190,y=70,width=70,height=25)

        GLineEdit_322=tk.Entry(root)
        GLineEdit_322["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_322["font"] = ft
        GLineEdit_322["fg"] = "#333333"
        GLineEdit_322["justify"] = "right"
        GLineEdit_322["text"] = "Entry"
        GLineEdit_322.place(x=310,y=70,width=70,height=25)

        GLabel_129=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_129["font"] = ft
        GLabel_129["fg"] = "#333333"
        GLabel_129["justify"] = "left"
        GLabel_129["text"] = "Show Title"
        GLabel_129.place(x=210,y=110,width=70,height=25)

        GLineEdit_554=tk.Entry(root)
        GLineEdit_554["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_554["font"] = ft
        GLineEdit_554["fg"] = "#333333"
        GLineEdit_554["justify"] = "right"
        GLineEdit_554["text"] = "Entry"
        GLineEdit_554.place(x=310,y=110,width=75,height=30)

        GLabel_834=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_834["font"] = ft
        GLabel_834["fg"] = "#333333"
        GLabel_834["justify"] = "left"
        GLabel_834["text"] = "Show Artist"
        GLabel_834.place(x=210,y=140,width=70,height=25)

        GLabel_561=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_561["font"] = ft
        GLabel_561["fg"] = "#333333"
        GLabel_561["justify"] = "left"
        GLabel_561["text"] = "Album Artist"
        GLabel_561.place(x=210,y=170,width=70,height=25)

        GLineEdit_722=tk.Entry(root)
        GLineEdit_722["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_722["font"] = ft
        GLineEdit_722["fg"] = "#333333"
        GLineEdit_722["justify"] = "right"
        GLineEdit_722["text"] = "Entry"
        GLineEdit_722.place(x=310,y=140,width=70,height=25)

        GLineEdit_73=tk.Entry(root)
        GLineEdit_73["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_73["font"] = ft
        GLineEdit_73["fg"] = "#333333"
        GLineEdit_73["justify"] = "right"
        GLineEdit_73["text"] = "Entry"
        GLineEdit_73.place(x=310,y=170,width=70,height=25)

        GButton_290=tk.Button(root)
        GButton_290["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        GButton_290["font"] = ft
        GButton_290["fg"] = "#000000"
        GButton_290["justify"] = "center"
        GButton_290["text"] = "Save"
        GButton_290.place(x=210,y=220,width=70,height=25)
        GButton_290["command"] = self.GButton_290_command

    def GButton_290_command(self):
        print("command")

# if __name__ == "__main__":
#     # root = tk.Tk()
#     # app = App(root)
#     # root.mainloop()
