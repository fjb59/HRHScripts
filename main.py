import parsexml
import tkinter as tk
from tkinter import filedialog as fd


def callback1():
    name = fd.askopenfilename()
    print(name)
    parsexml.ParseXML(name, includeTrackTitle=True)


def callback2():
    name = fd.askdirectory()
    print(name)


if __name__ == '__main__':
    errmsg = 'Error!'

    tk.Button(text='import playlist to clipboard',
              command=callback1).pack(fill=tk.X)
    tk.Button(text='Tag Mp3 files',
              command=callback2).pack(fill=tk.X)
    tk.mainloop()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
