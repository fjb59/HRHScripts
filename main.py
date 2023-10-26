import os
import tkinter.messagebox as messagebox
from os.path import exists



import parsexml
import tkinter as tk
from tkinter import filedialog as fd
import id3tag_dialog
import defaults


def wipe_config():
    if exists(defaults.confPath):
        l_title = "Are you sure?"
        response = messagebox.askyesno("Are you sure?","Are you sure you want to erase the tag data?")
        if response:
            os.remove(defaults.confPath)
def callback1():
    name = fd.askopenfilename()
    print(name)
    parsexml.ParseXML(name, includeTrackTitle=True)


def callback2():
    id3tag_dialog.main()

def callback3():
    wipe_config()


if __name__ == '__main__':
    errmsg = 'Error!'

    tk.Button(text='import playlist to clipboard',
              command=callback1).pack(fill=tk.X)
    tk.Button(text='Tag Mp3 files',
              command=callback2).pack(fill=tk.X)
    tk.Button(text='Erase tag config',
              command=callback3).pack(fill=tk.X)
    tk.mainloop()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
