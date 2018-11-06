from xmlrpc.client import *
import base64
import gzip

server = ServerProxy("http://api.opensubtitles.org/xml-rpc")
##for method in server.system.listMethods():
##    print(method)
##    print(server.system.methodHelp(method))
    
useragent = "utopensub"
log = server.LogIn("", "", "en", useragent))

DownloadSubtitles("utopensub"())