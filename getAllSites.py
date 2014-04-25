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

filename = "all_site_categories.csv"

worker = AbstractGenericWorker(http)
sites = worker.getAllEntitiesByType('site')


writer_content = list()
writer_content.append('Id;Name; Publisher; Audited; Category\n')

count = len(sites)
i = 1

for site in sites:
    print(str(i) + ' / ' + str(count))

    print('Working on site:' + site['name'])
    current_site = str(site['id']) + '; ' + site['name'] + '; '+ site['publisher_name'] + '; '+ str(site['audited']) + '; '

    if site['content_categories'] is not None:
        for category in site['content_categories']:
            writer_string = current_site + category['name'] + '\n '
            writer_content.append(writer_string)
    else:
        print("No Custom Categories")
        writer_string = current_site + '\n'
        writer_content.append(writer_string)
        
    i+=1

fw = FileWriter(filename, 'w')

for line in writer_content:
    fw.writeInNewFile(line)

fw.closeFile()
