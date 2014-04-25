import json
from lib.auth import Auth,AuthException
from lib.fileWriter import FileWriter
from lib.httpHandler import HttpHandler
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

worker = AbstractGenericWorker(http)

placements = worker.getAllEntitiesByType('placement')

writer_content = list()
writer_content.append('Placement_id;Placement_Name;Code;Default Ref Url;Site_id;Site_Name;Publisher_Name\n')

for place in placements:
	hex_id = str(hex(place['site_id'])).split("0x")[1]
	url = "interactivemedia-" + str(hex_id) + ".net"
	code = "-----"
	if place['code'] is not None:
		code = place['code']
	writer_content.append(str(place['id']) + ';' + place['name'] + ';' + code + ';' + url + ';' + str(place['site_id']) + ';' + place['site_name'] + ';' + place['publisher_name'] + '\n')

fw = FileWriter('Default_Ref_Url.csv', 'w')

for line in writer_content:
	fw.writeInNewFile(line)

fw.closeFile()
	

#payload = {"placement":{"default_referrer_url":None}}
#payload = {"placement":{"default_referrer_url":"interactivemedia-42313.net"}}

#params = {'id':placements[3]['id']}
#reqRet = http.putRequest(payload, 'placement', params)
#print(reqRet.json()['response']['status'])
