import glob
from datetime import datetime
from datetime import date

from dateutil.utils import today

import credentials
import os

from internetarchive import get_item, upload
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

def read_tags(filename):

    title = "NA"
    artist = ""
    albumArtist = ""
    composer = ""
    album = ""

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
    dateStr= tagname[4:]
    return dateStr

def freindlydate(date):
    date_obj = datetime.strptime(date, "%d%m%Y")
    readable_date = date_obj.strftime("%d %B %Y")

    return readable_date

def upload(tFilename):
    if os.path.exists(tFilename):
        ddmm = today().strftime("%d%m")
        tags = read_tags(tFilename)
        date = calcdate(tags['album'][0])
        identifier = tags['album'][0] + "_" + ddmm
        mediatype = 'audio'
        collection = 'opensource_audio'
        description = 'A whole lotta rock. ' + freindlydate(date)  # 25th march 2025
        md = {'collection': collection, 'title': description, 'mediatype': mediatype}
        myMedia = get_item(identifier)
        if not myMedia.exists:
            print (f"Uploading {tFilename} to Archive.org")
            r = myMedia.upload(files=tFilename, metadata=md, access_key=credentials.access_key,
                            secret_key=credentials.secret_key)

            print (r[0].status_code)
        else:
            print(f"media :{myMedia.created} already exists")
def download(id,tFilename):
    # not tested yet
    myMedia = get_item(id)
    if myMedia.exists:
        r = myMedia.download(tFilename)


mytag="0215"
#item = get_item(mytag)
#for k,v in item.metadata.items():
#    print(print(k,":",v))
#tags = read_tags("/Users/frank/pCloud Drive/HRH/recordings/021501042025.mp3")
for files in glob.glob(credentials.searchpath + f'{mytag}*.mp3'):
    upload(files)
pass


