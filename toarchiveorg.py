from datetime import datetime

from internetarchive import get_item
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

def read_tags(filename):
    print(f" The file is {filename}")


    mp3file = MP3(filename, ID3=EasyID3)  # retag here
    endodedby = mp3file["encodedby"]
    title = mp3file["Title"]
    artist =  mp3file["Artist"]
    albumArtist = mp3file["AlbumArtist"]
    composer = mp3file["composer"]
    album = mp3file["Album"]
    return {"title":title,"artist":artist,"albumartist":albumArtist,'composer':composer,'album':album}

def calcdate(tagname):
    dateStr= tagname[4:]
    return dateStr

def freindlydate(date):
    date_obj = datetime.strptime(date, "%d%m%Y")
    readable_date = date_obj.strftime("%d %B %Y")

    return readable_date

mytag='021525032025'

#item = get_item(mytag)
#for k,v in item.metadata.items():
#    print(print(k,":",v))
tags = read_tags("/Users/frank/pCloud Drive/HRH/recordings/021501042025.mp3")
pass
date = calcdate(tags['album'][0])
# identifier : 021525032025
mediatype = 'audio'
collection = 'opensource_audio'
creator =tags['composer']




description = 'A whole lotta rock. ' + freindlydate(date) #25th march 2025
subject = ['rock', 'effjerbee', 'effjerby', 'hrhRadio']
title = tags['album']

