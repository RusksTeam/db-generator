from dbreguesthandler import DBRequestHandler
from dbserver import DBServer
import time
import configparser
import json
import drybreadfactory

Config = configparser.ConfigParser();
Config.read("config/server.ini")
HOST_NAME = Config.get('HTTPConfig', 'HOST_NAME')
PORT_NUMBER = Config.getint('HTTPConfig', 'PORT_NUMBER')


dry_bread = drybreadfactory.get_dry_bread()

#Generating json for DB response8
response = {}
response["question"] = dry_bread[0]
response["answer"] = dry_bread[1]
response_string = json.dumps(response, ensure_ascii=False, indent=4)

httpd = DBServer((HOST_NAME, PORT_NUMBER), DBRequestHandler)
httpd.set_dry_bread(response_string, mime="application/json")
#httpd.set_dry_bread('<html><head><meta content="text/html;charset=utf-8" http-equiv="Content-Type"><meta content="utf-8" http-equiv="encoding"></head><body><h1>Po co kotu telefon?</h1><h1>Żeby MIAU</h1></body></html>', mime="text/html")


print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))
