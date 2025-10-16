#!/usr/bin/python3

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

def update_tag(identifier,tagid,value):
    item = get_item(identifier)
    item.modify_metadata({tagid: value}, access_key=keys.access_key, secret_key=keys.secret_key)

def erase_tag(identifier,tagid):
    item = get_item(identifier)
    item.modify_metadata({tagid: 'REMOVE_TAG'}, access_key=keys.access_key, secret_key=keys.secret_key)



def fetch(identifier,pattern = "*",verbose=True):
    #fetch archive files based on pattern, leave empty for all files in archive
    myMedia = get_item(identifier)
    if myMedia.exists:
        #downloado only if we don't aleady have it
        download(identifier,glob_pattern=pattern,checksum_archive=True,verbose=verbose)
        print (f"Downloaded to {os.getcwd()}")
def findByQuery(query):
    return search_items(query)
    pass
def findByUploader(tag='', author=""):
    listofthings=findByQuery('uploader:(g7wap@live.co.uk)').iter_as_items()
    if len(listofthings)>0:
        for item in listofthings:

    
          if 'date' in item.metadata:
              continue
          else:
            datestr = freindlydate(calcdate(item.metadata["identifier"]), "%Y-%m-%d")
            if datestr is None:
                    print (f"skipping {item.metadata["identifier"]}")
            else:
                    update_tag(item.metadata["identifier"], "date", datestr)
                #datename = "A Whole Lotta Rock - "+ datestr
                #update_tag(item.metadata["identifier"],"creator","Effjerbee")
                #erase_tag(item.metadata["identifier"],"Subject")
                    print ("Identifier :"+item.metadata["identifier"]+ " Updated")
    else:
        print("nothing found")



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

tag="0215"
canDelete =True

upload_show(tag,canDelete)
#listofitems = findByUploader()
#print("Done")
#fetch('021522042025_2404',"*.mp3")
