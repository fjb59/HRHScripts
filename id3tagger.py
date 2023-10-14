from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import glob
#import tkinter as tk
from tkinter import  *
from tkinter import filedialog as fd
from os.path import exists
import threading
my_tag = '0215'
show_title = "A Whole Lotta Rock"
show_artist = "Hard Rock Hell Radio"
album_artist = "effjerbee aka FJB"
composer = album_artist
track = 0
disk_number = 0


def callback():
    #name = fd.askopenfilename()
    name = fd.askdirectory()
    if len(name) > 2:
         if exists(name):
            Tagger(name)


def Tagger_Thread(filename):
    print (f" The file is {filename}")
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


def Tagger(tPath):


    print (tPath)
    if exists(tPath):
        segs_path=tPath
    else:

        segs_path = "P:\\HRH\\20230530_1500"
    tags = [{'artist':f'{show_artist}'}, {'title':f"{show_title} "}]



    filez = glob.glob(f"{segs_path}\\{my_tag}*.mp3") # get array of filename with mp3 extension
    # print the first element of filez:
    for thisfile in filez:

        # print (thisfile)
        this_file_list = thisfile.split("\\") # seperate filename from path
        last_chunk=len(this_file_list)-1
        if this_file_list[last_chunk].count(" pt") > 0: # if it ends ' pt' then part number  in the filemame then ok to carry on or raise an error

            threading.Thread(target=Tagger_Thread, args=(thisfile,)).start()
            # print (f"tagging {thisfile}")
            # song = this_file_list[last_chunk].split('.')[0]  # remove file extension
            # file_section = song.split(' pt')[0] #seperate filename and part number
            # track = song.split(' pt')[1] #seperate filename and part number
            # disk_number=track
            # mp3file = MP3(thisfile, ID3=EasyID3) #retag here
            # mp3file["encodedby"] = 'id3tagger'
            # mp3file["Title"] = show_title
            # mp3file["Artist"] = show_artist
            # mp3file["AlbumArtist"] = album_artist
            # mp3file["composer"] = composer
            # mp3file["Album"] = f"{file_section} pt{track}"
            # mp3file["Tracknumber"] = track
            # mp3file["Discnumber"] = disk_number
            #
            # mp3file.save() #save changes. don't forget this line.



        else:
            print(f"{thisfile} has no part number.")

if __name__ == '__main__':
    errmsg = 'Error!'

    window = Tk()
    window.title("id3 tagger")
    window.geometry('320x200')
    lbl = Label(window,text='Select a folder containing relevent mp3s')
    lbl.grid(column=0,row=0)

    btn=Button(window,text='Tag Mp3 files', command=callback)
    btn.grid(column=0,row=2)
    #tk.Button(text='Tag Mp3 files',command=callback).pack(fill=tk.X)
    window.mainloop()
