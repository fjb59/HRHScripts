#!/usr/bin/python3
import argparse
#created by Frank Barton AKA effjerbee
#purpose: uploads and downloads your shows to internetarchive.org
#2025

import glob
from datetime import datetime
from time import strptime

from dateutil.utils import today
import os

# you need to create the credentials.py yourself. Check the  README
from my_credentials import keys



# internet archive.org library
from internetarchive import get_item, download, search_items, delete


#libraries for handling mp3 files and their metadata
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

def read_tags(filename):

    title = "NA"
    artist = ""
    albumArtist = ""
    composer = ""
    album = ""
    #read mp3 file and acquire metdata

    mp3file = MP3(filename, ID3=EasyID3)  # retag here

    if "Title" in mp3file:
        title = mp3file["Title"]

    if "Artist" in mp3file:
        artist =  mp3file["Artist"]

    if "AlbumArtist" in mp3file:
        albumArtist = mp3file["AlbumArtist"]

    if "composer" in mp3file:
        composer = mp3file["composer"]
    if  "Album" in mp3file:
        album = mp3file["Album"]
    return {"title":title,"artist":artist,"albumartist":albumArtist,'composer':composer,'album':album}

def calcdate(tagname):
    #remove tag (4 characters) leaving the date
    dateStr= tagname[4:12]
    return dateStr

def freindlydate(date, format="%d %B %Y"):
    # reformat date to a more human readabler version
    date_obj=""
    try:
        date_obj = datetime.strptime(date, "%d%m%Y")
        #date_obj = datetime.strptime(date, format)

    except:
        print ("date format is wrong")
        try:
            date_obj = datetime.strptime(date, "%Y%m%d")
        except:
            print("date format is still wrong")
            try:
                date_obj = datetime.strptime(date, "%Y%d%m")
            except:
                print("date format is very wrong")
                return None





    #readable_date = date_obj.strftime("%d %B %Y")
    readable_date = date_obj.strftime(format)

    return readable_date

def upload(tFilename,verbose=True):

    if os.path.exists(tFilename):
        #build archive metadata from mp3 metadata
        ddmm = today().strftime("%d%m")
        tags = read_tags(tFilename)
        showname = tags['title'][0]
        date = calcdate(tags['album'][0])
        broadcastdate = strptime(date, "%d%m%Y")
        ddmmyy=strptime(today().strftime("%d%m%Y"),"%d%m%Y")
        yymmdd =freindlydate(calcdate(tags['album'][0]), "%Y-%m-%d")

        if ddmmyy >=broadcastdate:

            identifier = tags['album'][0] + "_" + ddmm
            mediatype = 'audio'
            collection = 'opensource_audio'
            description = showname + " " +freindlydate(date)  # 25th march 2025
            md = {'collection': collection, 'title': description, 'mediatype': mediatype, 'date': yymmdd, 'subject':'Hard Rock Hell Radio','Creator':'Effjerbee', 'DJ':'Effjerbee'}
            #check if archive already exists, if not then upload
            myMedia = get_item(identifier)
            if not myMedia.exists:
                print (f"Uploading {tFilename} to Archive.org")
                r = myMedia.upload(files=tFilename, metadata=md, access_key=keys.access_key,
                                secret_key=keys.secret_key,verbose=verbose)

                print (r[0].status_code)
                return int(r[0].status_code)
            else:

                print(f"media :{myMedia.created} already exists")
        else :
            print ("too soon to upload this.")
            return -1









def upload_show(tag,candelete=False) :
    from my_credentials import paths

    #search folder for mp3 files beginning with '{mytag}' and upload them. i may build this into a function later
    for files in glob.glob(paths.searchpath + f'{tag}*.mp3'):
        r = upload(files)
        if r == 200:
            print("successful upload")
            if canDelete:
                os.remove(files)
                print (f"{files} deleted.")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="uploads to archive.org")
    parser.add_argument("--tag", type=str, default="0215",
                        help="Tag id.")
    parser.add_argument("--candelete", type=str, default="yes",
                        help="Tag id.")
    args = parser.parse_args()

tag=args.tag
canDelete =True
if args.candelete !="yes":
    canDelete =False

upload_show(tag,canDelete)
#listofitems = findByUploader()
#print("Done")
#fetch('021522042025_2404',"*.mp3")
