import argparse
import glob
import io
import os
import threading
from os.path import exists


from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import sys
# defaults
import defaults
import tags

#

track = 0
disk_number = 0
myDocuments = 5


class id3tagger():
    my_tag = tags.my_tag
    show_title = tags.show_title
    show_artist = tags.show_artist
    album_artist = tags.album_artist
    album = tags.album
    composer = tags.composer
    dj = tags.dj
    default_path = ""






    # retranslateUi



    def read_config(self):

        confHandle = io.open(defaults.confPath, mode="r")
        line = confHandle.readline().rstrip()

        if line == defaults.taggerName:
            self.my_tag = confHandle.readline().rstrip()
            self.show_title = confHandle.readline().rstrip()
            self.show_artist = confHandle.readline().rstrip()
            self.album_artist = confHandle.readline().rstrip()
            self.composer = self.album_artist
            confHandle.close()

        else:
            confHandle.close()



    def tagger_thread(self, filename):

        this_file_list = filename.split("\\")  # seperate filename from path
        last_chunk = len(this_file_list) - 1
        song = this_file_list[last_chunk].split('.')[0]  # remove file extension
        file_section = song.split(' pt')[0]  # seperate filename and part number
        track = 1
        disk_number = track
        mp3file = MP3(filename, ID3=EasyID3)  # retag here
        mp3file["encodedby"] = 'id3tagger'
        mp3file["Title"] = self.show_title
        mp3file["Artist"] = self.show_artist
        mp3file["AlbumArtist"] = self.album_artist
        mp3file["composer"] = self.composer
        mp3file["comment"] = "tagged by id3tagger.py"

        mp3file["Album"] = song.split('/')[-1]
      #  mp3file["DJ"] = self.dj
      #  mp3file["Tracknumber"] = 1
      #  mp3file["Discnumber"] = 1

        mp3file.save()  # save changes. don't forget this line.

    def tagger(self, tPath):

        if exists(tPath):
            segs_path = tPath
        else:

            segs_path = "P:\\HRH\\20230530_1500"
        # tags = [{'artist':f'{show_artist}'}, {'title':f"{show_title} "}]

        filez = glob.glob(f"{segs_path}/{self.my_tag}*.mp3")  # get array of filename with mp3 extension
        # print the first element of filez:
        self.model.clear()
        for thisfile in filez:

            # print (thisfile)
            this_file_list = thisfile.split("/")  # seperate filename from path
            last_chunk = len(this_file_list) - 1

            print (thisfile)
            threading.Thread(target=self.tagger_thread, args=(thisfile,)).start()

    def __init__(self,parent=None):
        super().__init__()




def main(tpath = ""):
    tagger = id3tagger()

    tagger.tagger(tpath)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Breaks mp3 file into chunks")
    parser.add_argument("--path", type=str, default="",
                        help="Path of files to tag .")
    args = parser.parse_args()
    path = args.path
    if args.path == "":
        path = os.path.curdir()


    main(path)
