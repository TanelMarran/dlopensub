import xmlrpc.client
import base64
import gzip
import struct
import os
import tkinter as tk
from tkinter import filedialog

def hashFile(name): ##source: http://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes?fbclid=IwAR3e4Qsusy0--Jkd8jnMsvYk_wFtAcsItec-Vyf4QXxFiLWoFcNmGpfOpzs#Python
    try:

        longlongformat = 'q'  # long long
        bytesize = struct.calcsize(longlongformat)

        f = open(name, "rb")

        filesize = os.path.getsize(name)
        hash = filesize

        if filesize < 65536 * 2:
            return "SizeError"

        for x in range(int(65536/bytesize)):
            buffer = f.read(bytesize)
            (l_value,)= struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number


        f.seek(max(0,filesize-65536),0)
        for x in range(int(65536/bytesize)):
            buffer = f.read(bytesize)
            (l_value,)= struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF

        f.close()
        returnedhash =  "%016x" % hash
        return returnedhash

    except(IOError):
        return "IOError"

def muuda():
    global fileDir
    fileDir = filedialog.askopenfilename()
    global label
    label.config(text=fileDir)

def tõmba():
    #Otsi filmi faili järgi ning salvesta selle info
    mhash = hashFile(fileDir)
    info = server.SearchSubtitles(token, [{"sublanguageid":"eng", "moviehash": mhash}])
    #Faili nime saame kätte
    subDir = fileDir
    subDir = subDir.split("/")
    subName = subDir[-1]
    while subName[-1] != ".":
        subName = subName.replace(subName[-1], "")
    del subDir[-1]
    subDir = "/".join(subDir)
    subDir = os.path.join(subDir, subName+"srt")


    #Kui infot leidus, võta otsingust esimene leid ning tõmba subtiitrid
    global label2

    if info["data"] != []:
        fail = server.DownloadSubtitles(token,[info["data"][0]["IDSubtitleFile"]])
        fail = fail["data"][0]["data"]
        fail = base64.b64decode(fail)
        fail = gzip.decompress(fail)
        with open(subDir, "wb") as fp:
            fp.write(fail)
        label2.config(text="Subtiitrid tõmmatud!")
    else:
        label2.config(text="Subtiitreid ei leitud.")

#Ühenda serveriga
server = xmlrpc.client.ServerProxy("http://api.opensubtitles.org/xml-rpc")

#Salvesta acess token
useragent = "utopensub"
log = server.LogIn("","","en",useragent)
token = log["token"]

#tkinter file dialog
root = tk.Tk()
root.title("Subtiitrid tõmmatud OpenSubtitles'iga")
fileDir = ""
label = tk.Label(root,text=fileDir)
button = tk.Button(root,text="Ava",command=muuda)
button2 = tk.Button(root,text="Tõmba subtiitrid",command=tõmba)
label2 = tk.Label(root,text="")
label.pack()
button.pack()
button2.pack()
label2.pack()
root.mainloop()


