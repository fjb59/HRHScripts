tested on python 3.11.


run id3tagger to tag mp3 files. 
on first go it will bring up a dialog to put in your informarion
confirm changes then close dialog. then run id3tagger again. 
it will then bring ip a folders directory, from where you select the directory containing your mp3 files you want to tag
they must be in the format  tagname ptX.mp3 where tag is your id tax and X is the part number.  "31259 pt1.mp3" for example
mp3 fiels not in this format will be ignored.

# HRHScripts
changed ui to qt

The toarchaveorg.py will need you to create your own credentials.py file which contains information in the flowing format.

access_key = "your access key"
secret_key="your secret key"
searchpath = r"path to folder containing files you wish to upload"