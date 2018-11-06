import xmlrpc.client
import base64
import gzip

server = xmlrpc.client.ServerProxy("http://api.opensubtitles.org/xml-rpc")

useragent = "utopensub"
log = server.LogIn("","","en",useragent)
token = log["token"]

nimi = input("Sisestage filmi nimi: ")
info = server.SearchSubtitles(token, [{"sublanguageid":"eng", "query":nimi}])

if info["data"] != []:
    #for i,j in info["data"][0].items():
    #    print(str(i)+": "+str(j))
    fail = server.DownloadSubtitles(token,[info["data"][0]["IDSubtitleFile"]])
    fail = fail["data"][0]["data"]
    fail = base64.b64decode(fail)
    #print(fail)
    fail = gzip.decompress(fail)
    print(type(fail))
    print(fail)
    with open("sub.srt", 'wb') as f:
        f.write(fail)