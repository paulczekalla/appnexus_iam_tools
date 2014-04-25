import json
import copy
from lib.auth import Auth, AuthException
from lib.httpHandler import HttpHandler
from lib.fileWriter import FileWriter
from worker.generic.AbstractGenericWorker import AbstractGenericWorker

def aquireAuthToken(authObj, http):
    token = ""
    try:
        token = authObj.readResponse(authObj.authorizationRequest(http))
    except AuthException as e:
        print("Login mit Zugang {} nicht möglich.".format(e.login))
        print("Zugangsdaten erneut eingeben: ")
        login = input("Login: ")
        password = input("Passwort: ")
        aquireAuthToken(Auth(login, password), http)
    else:
        http.setToken(token)

proxies = {
  "http": "http://proxy.t-online.net:3128",
  "https": "http://proxy.t-online.net:3128",
}

http = HttpHandler(proxies, "http://api.appnexus.com")

a = Auth()

aquireAuthToken(a, http)

filename = "all_placement_urls.csv"

worker = AbstractGenericWorker(http)
placements = worker.getAllEntitiesByType('placement')

writer_content = list()
writer_content.append('Id;Name; Publisher; Site; URL\n')

count = len(placements)
i = 1

for placement in placements:
    print(str(i) + ' / ' + str(count))

    print('Working on placement:' + placement['name'])
    writer_string = str(placement['id']) + '; ' + placement['name'] + '; '+ placement['publisher_name'] + '; '+ placement['site_name'] + ';'
    if placement['default_referrer_url'] is not None:
            writer_string += placement['default_referrer_url'] + '; '

    writer_string +=  '\n'
    writer_content.append(writer_string)
    i+=1

fw = FileWriter(filename, 'w')

for line in writer_content:
    fw.writeInNewFile(line)

fw.closeFile()
