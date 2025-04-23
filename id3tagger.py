import io
import os
import tkinter.messagebox

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import glob
from tkinter import Tk,Label,Button,Menu
from tkinter import filedialog as fd
from os.path import exists
import tags
import threading
import defaults
my_tag = ''
show_title = ""
show_artist = ""
album_artist = ""
composer = album_artist
track = 0
disk_number = 0
myDocuments = 5


def callback():

    name = fd.askdirectory()
    if len(name) > 2:
        if exists(name):
            tagger(name)


def saveme():
    print("he's been taken up")


def tagger_thread(filename):
    print(f" The file is {filename}")
    print(f"tagging {filename}")
    this_file_list = filename.split("\\")  # seperate filename from path
    last_chunk = len(this_file_list) - 1
    song = this_file_list[last_chunk].split('.')[0]  # remove file extension
    file_section = song.split(' pt')[0]  # seperate filename and part number
    track = song.split(' pt')[1]  # seperate filename and part number
    disk_number = track
    mp3file = MP3(filename, ID3=EasyID3)  # retag here
    mp3file["encodedby"] = 'id3tagger'
    mp3file["Title"] = show_title
    mp3file["Artist"] = show_artist
    mp3file["AlbumArtist"] = album_artist
    mp3file["composer"] = composer
    mp3file["Album"] = f"{file_section} pt{track}"
    mp3file["Tracknumber"] = track
    mp3file["Discnumber"] = disk_number

    mp3file.save()  # save changes. don't forget this line.


def wipe_config():
    if exists(defaults.confPath):
        l_title="Are you sure?"
        response = tkinter.messagebox.askyesno(title=l_title,message="Are you sure you want to erase the tag data?")
        if response:
            os.remove(defaults.confPath)
            window.quit()


def tagger(tPath):

    if exists(tPath):
        segs_path = tPath
    else:

        segs_path = "P:\\HRH\\20230530_1500"
    # tags = [{'artist':f'{show_artist}'}, {'title':f"{show_title} "}]

    filez = glob.glob(f"{segs_path}\\{my_tag}*.mp3")  # get array of filename with mp3 extension
    # print the first element of filez:
    for thisfile in filez:

        # print (thisfile)
        this_file_list = thisfile.split("\\")  # seperate filename from path
        last_chunk = len(this_file_list)-1
        if this_file_list[last_chunk].count(" pt") > 0:
            # if it ends ' pt' then part number  in the filemame then ok to carry on or raise an error

            threading.Thread(target=tagger_thread, args=(thisfile,)).start()
        else:
            print(f"{thisfile} has no part number.")


if __name__ == '__main__':
    errmsg = 'Error!'

    window = Tk()
    window.minsize(width=320,height=200)
    window.geometry('320x200')

    # myDocs=userpaths.get_my_documents()
    lbl = Label(window, text='Select a folder containing relevent mp3s')

    if exists(defaults.confPath):
        confHandle = io.open(defaults.confPath, mode="r")
        line = confHandle.readline().rstrip()

        window.title("id3 tagger")
        menuBar = Menu(window)
        window.config(menu=menuBar)

        fileMenu = Menu(menuBar)
        fileMenu.add_command(label="Wipe tag config", command=wipe_config)
        appMenu = Menu(menuBar)
        appMenu.add_command(label="Exit", foreground="#cc0000", command=window.destroy)

        menuBar.add_cascade(label="File", menu=fileMenu)
        menuBar.add_cascade(label='App', menu=appMenu)

        if line == defaults.taggerName:
            my_tag = confHandle.readline().rstrip()
            show_title = confHandle.readline().rstrip()
            show_artist = confHandle.readline().rstrip()
            album_artist = confHandle.readline().rstrip()
            composer = album_artist
            confHandle.close()

            lbl = Label(window, text='Select a folder containing relevent mp3s')
            btn = Button(window, text='Tag Mp3 files', command=callback)
            btn.grid(column=0, row=2)
            lbl.grid(column=0, row=0)
        else:
            confHandle.close()

    else:
        window.title("id3 tagger options")
        app = tags.App(window)

    window.mainloop()
