import xmlrpc.client
import base64
import gzip
import os
import codecs
server = xmlrpc.client.ServerProxy("http://api.opensubtitles.org/xml-rpc")

useragent = "utopensub"
log = server.LogIn("","","en",useragent)
token = log["token"]

nimi = "westworld"#input("Sisestage filmi nimi: ")
info = server.SearchSubtitles(token, [{"sublanguageid":"eng", "query":nimi}])

if info["data"] != []:
    
    fail = server.DownloadSubtitles(token,[info["data"][0]["IDSubtitleFile"]])
    fail = fail["data"][0]["data"]
    fail = base64.b64decode(fail)
    print(fail)
    fail = gzip.decompress(fail)
    with open("sub.txt", "wb") as fp:
        fp.write(fail)

    #os.rename("sub.txt", "sub.srt")

