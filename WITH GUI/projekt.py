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
    global entry
    entry.delete(0,"end")
    entry.insert(0,filedialog.askopenfilename())
    if entry.get() != "":
        uuri()
    #global fileDir
    #fileDir = filedialog.askopenfilename()
    #global label
    #label.config(text=fileDir)

def tõmba():
    #Otsi filmi faili järgi ning salvesta selle info
    mhash = hashFile(entry.get())
    info = server.SearchSubtitles(token, [{"sublanguageid":"eng", "moviehash": mhash}])
    #Faili nime saame kätte
    subDir = entry.get()
    subDir = subDir.split("/")
    subName = subDir[-1]
    while subName[-1] != ".":
        subName = subName.replace(subName[-1], "")
    del subDir[-1]
    subDir = "/".join(subDir)
    subDir = os.path.join(subDir, subName+"srt")


    #Kui infot leidus, võta otsingust esimene leid ning tõmba subtiitrid
    global label2
    global listbox

    if listbox.curselection() != tuple():
        secindex = listbox.curselection()[0]
        print(secindex)
        fail = server.DownloadSubtitles(token,[info["data"][secindex]["IDSubtitleFile"]])
        fail = fail["data"][0]["data"]
        fail = base64.b64decode(fail)
        fail = gzip.decompress(fail)
        with open(subDir, "wb") as fp:
            fp.write(fail)
        label2.config(text="Subtiitrid tõmmatud!")
        label2.place(relx=0.4-0.01, rely=0.53+0.2, anchor = tk.CENTER)
    """if info["data"] != []:
        fail = server.DownloadSubtitles(token,[info["data"][0]["IDSubtitleFile"]])
        fail = fail["data"][0]["data"]
        fail = base64.b64decode(fail)
        fail = gzip.decompress(fail)
        with open(subDir, "wb") as fp:
            fp.write(fail)
        label2.config(text="Subtiitrid tõmmatud!")
        label2.place(relx = 0.5, rely = 0.65, anchor = tk.CENTER)
    else:
        label2.config(text="Subtiitreid ei leitud.")
        label2.place(relx = 0.5, rely = 0.65, anchor = tk.CENTER)"""

def uuri():
    #Otsi filmi faili järgi ning salvesta selle info
    mhash = hashFile(entry.get())
    info = server.SearchSubtitles(token, [{"sublanguageid":"eng", "moviehash": mhash}])
    #Faili nime saame kätte
    subDir = entry.get()
    subDir = subDir.split("/")
    subName = subDir[-1]
    while subName[-1] != ".":
        subName = subName.replace(subName[-1], "")
    del subDir[-1]
    subDir = "/".join(subDir)
    subDir = os.path.join(subDir, subName+"srt")


    #Kui infot leidus, võta otsingust esimene leid ning tõmba subtiitrid
    global listbox

    if info["data"] != []:
        listbox.delete(0,"end")
        for i in info["data"]:
            listbox.insert("end", i["SubFileName"])



#Ühenda serveriga
server = xmlrpc.client.ServerProxy("http://api.opensubtitles.org/xml-rpc")

#Salvesta acess token
useragent = "utopensub"
log = server.LogIn("","","en",useragent)
token = log["token"]

#tkinter file dialog
root = tk.Tk()
root.resizable(False, False)
root.geometry("600x400")
root.configure(background = "white")
root.title("Subtiitrid tõmmatud OpenSubtitles'iga")
fileDir = ""
entry = tk.Entry(root,width=60)
#label = tk.Label(root,text=fileDir, background = "white")
button = tk.Button(root,text="Ava",command=muuda, height = 3, width = 30)
button2 = tk.Button(root,text="Tõmba subtiitrid",command=tõmba, height = 3, width = 30)
label2 = tk.Label(root,text="", background = "white")
listbox = tk.Listbox(root)
entry.pack()
#label.pack()
button.pack()
button2.pack()
label2.pack()
entry.place(relx = 0.5, rely = 0.23, anchor = tk.CENTER)
button.place(relx = 0.4-0.01, rely = 0.53-0.09, anchor = tk.CENTER)
button2.place(relx=0.4-0.01, rely=0.53+0.09, anchor=tk.CENTER)
listbox.place(relx=0.7-0.01, rely=0.53, anchor=tk.CENTER)
#label.place(relx = 0.5, rely = 0.25, anchor = tk.CENTER)
root.mainloop()


