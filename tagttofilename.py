import argparse
import glob
import io
import os
import threading
from os.path import exists


from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
#

track = 0
disk_number = 0
myDocuments = 5





def tagger_thread(filename):
    ext = filename.split('.')[-1]
    folder=os.path.dirname(filename)
    mp3file = MP3(filename, ID3=EasyID3)  # retag here
    title = mp3file["Title"][0]

    filen=os.path.splitext(title)[0]
    newfilename =f"{folder}/{filen}.{ext}"
    if not os.path.exists(newfilename):
        print (f"{filename} -> {newfilename}")
        try:
            os.rename(filename,newfilename)
        except FileNotFoundError:
            print(f'The file "{filename}" does not exist.')
        except FileExistsError:
            print(f'The file "{newfilename}" already exists, and it will be overwritten.')

        except PermissionError:
            print(f'Permission denied when trying to rename the file.')

    else :
        print(f"error: {newfilename} exists")
        pass


def main(tPath=os.getcwd()):

    filez = glob.glob(f"{tPath}/*.mp3")  # get array of filename with mp3 extension
    # print the first element of filez:
    for thisfile in filez:



        threading.Thread(target=tagger_thread, args=(thisfile,)).start()





if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Breaks mp3 file into chunks")
    parser.add_argument("path", type=str,
                        help="Path of files to rename.")
    args = parser.parse_args()

    main(args.path)
