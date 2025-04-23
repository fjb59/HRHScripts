import xml.etree.ElementTree as ET
from os.path import exists
#from tkinter.filedialog import askopenfilename


import pyperclip as cb


def ParseXML(tcFileName, **parms):
    if "includeTrackTitle" in parms:
        if parms['includeTrackTitle']==False:
            includeTrackTitle = False
        else:
             includeTrackTitle = True
    if exists(tcFileName):
        handle = open(tcFileName,"r")
        tree = ET.parse(tcFileName)
        root = tree.getroot()
        tracklist = []
        track = ["artist", ""] #artist, title

        for element in root:
            for subelement in element:
                if subelement.tag=='{http://xspf.org/ns/0/}track':
                    for grandchild in subelement:
                        if( "title" in grandchild.tag):
                            track[1]= grandchild.text
                        if ("creator" in grandchild.tag):
                            track[0]=  grandchild.text



                        if ("extension" in grandchild.tag):
                            try:
                                ext = list(grandchild)
                            except AttributeError:
                                pass

                            else:
                                for extension in ext: #should be setteings
                                    for settings in extension:
                                        for setting in settings:
                                            if "entryType" in setting.tag:
                                                if setting.text in ['0','1','2']:
                                                    if includeTrackTitle:
                                                        tracklist.append(f"{track[0]}, {track[1]}")
                                                    else:
                                                        tracklist.append(f"{track[0]}")
                                                    track[0] = ""
                       # track.clear()
        buf=""
        for tracks in tracklist:
            buf=buf+tracks+"\n"
            print (f"{tracks}\n")
        cb.copy(buf)


        handle.close()
    else:
        print (tcFileName+" does not exist")
if __name__ == '__main__':

    name ="/Users/frank/Documents/021530012024.pfp"
        #askopenfilename()
    print(name)
    ParseXML(name, includeTrackTitle=True)