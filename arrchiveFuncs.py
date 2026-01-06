import os

from internetarchive import search_items,get_item,upload,download

from toarchiveorg import update_tag


def findByUploader( author=""):
    listofthings = search_items(f'uploader:({author})').iter_as_items()
    return listofthings
    # if len(listofthings) > 0:
    #     for item in listofthings:
    #
    #         if 'date' in item.metadata:
    #             continue
    #         else:
    #             datestr = freindlydate(calcdate(item.metadata["identifier"]), "%Y-%m-%d")
    #             if datestr is None:
    #                 print(f"skipping {item.metadata['identifier']}")
    #             else:
    #                 update_tag(item.metadata["identifier"], "date", datestr)
    #                 # datename = "A Whole Lotta Rock - "+ datestr
    #                 # update_tag(item.metadata["identifier"],"creator","Effjerbee")
    #                 # erase_tag(item.metadata["identifier"],"Subject")
    #                 print("Identifier :" + item.metadata["identifier"] + " Updated")
    # else:
    #     print("nothing found")
def findByQuery(query):
    return search_items(query).iter_as_items()


def fetch(identifier,pattern = "*",verbose=True):
    #fetch archive files based on pattern, leave empty for all files in archive
    myMedia = get_item(identifier)
    if myMedia.exists:
        #downloado only if we don't aleady have it
        download(identifier,glob_pattern=pattern,checksum_archive=True,verbose=verbose)
        print (f"Downloaded to {os.getcwd()}")

def erase_tag(identifier,tagid,access,secret):
    item = get_item(identifier)
    item.modify_metadata({tagid: 'REMOVE_TAG'}, access_key=access, secret_key=secret)

def update_tag(identifier,tagid,value,access,secret):
    item = get_item(identifier)
    item.modify_metadata({tagid: value}, access_key=access, secret_key=secret)


def add_file(tIdentifier, tFilename, verbose=True, access="", key=""):
    if os.path.exists(tFilename):



            identifier = tIdentifier

            # check if archive already exists, if so then upload
            myMedia = get_item(identifier)
            if  myMedia.exists:
                print(f"appending  {tFilename} to {identifier}")
                r = myMedia.upload(files=tFilename, access_key=access,
                                   secret_key=key, verbose=verbose)

                print(r[0].status_code)
                return int(r[0].status_code)

    else:
        print (f"file:{tFilename} does not exist")



