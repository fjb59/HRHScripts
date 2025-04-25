#created by Frank Barton AKA effjerbee
#purpose: uploads and downloads your shows to internetarchive.org
#2025

import glob
from datetime import datetime
from dateutil.utils import today
import os

# you need to create the credentials.py yourself. Check the  README
import credentials


# internet archive.org library
from internetarchive import get_item, download

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
    dateStr= tagname[4:]
    return dateStr

def freindlydate(date):
    # reformat date to a more human readabler version
    date_obj = datetime.strptime(date, "%d%m%Y")
    readable_date = date_obj.strftime("%d %B %Y")

    return readable_date

def upload(tFilename,verbose=True):
    showname = 'A whole lotta rock'
    if os.path.exists(tFilename):
        #build archive metadata from mp3 metadata
        ddmm = today().strftime("%d%m")
        tags = read_tags(tFilename)
        date = calcdate(tags['album'][0])
        identifier = tags['album'][0] + "_" + ddmm
        mediatype = 'audio'
        collection = 'opensource_audio'
        description = showname + freindlydate(date)  # 25th march 2025
        md = {'collection': collection, 'title': description, 'mediatype': mediatype}
        #check if archive already exists, if not then upload
        myMedia = get_item(identifier)
        if not myMedia.exists:
            print (f"Uploading {tFilename} to Archive.org")
            r = myMedia.upload(files=tFilename, metadata=md, access_key=credentials.access_key,
                            secret_key=credentials.secret_key,verbose=verbose)

            print (r[0].status_code)
        else:
            print(f"media :{myMedia.created} already exists")

def fetch(identifier,pattern = "*",verbose=True):
    #fetch archive files based on pattern, leave empty for all files in archive
    myMedia = get_item(identifier)
    if myMedia.exists:
        #downloado only if we don't aleady have it
        download(identifier,glob_pattern=pattern,checksum_archive=True,verbose=verbose)
        print (f"Downloaded to {os.getcwd()}")


mytag="0215"

#search folder for mp3 files beginning with '{mytag}' and upload them. i may build this into a function later
for files in glob.glob(credentials.searchpath + f'{mytag}*.mp3'):
    upload(files)


#fetch('021522042025_2404',"*.mp3")
