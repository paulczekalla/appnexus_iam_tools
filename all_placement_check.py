import json
from lib.auth import Auth, AuthException
from lib.httpHandler import HttpHandler
from lib.fileWriter import FileWriter
from worker.allEntityCheck.allEntityCheck import AllEntityCheck

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

filename = "all_placement_date.csv"

http = HttpHandler(proxies, "http://api.appnexus.com")

a = Auth()

aquireAuthToken(a, http)

count = http.getRequestPage(0, "placement").json()['response']['count']

allPlacements = list()

for start_element in range(0, count, 100):
	resp = http.getRequestPage(start_element, "placement").json()['response']
	if 'error_id' in resp:
		print(resp)
	else:
		allPlacements.append(resp['placements'])

allPlacementListHandler = AllEntityCheck()

writer_content = list()
writer_content.append('Id;Name;Site Name; Is Resizeable\n')

for placement in allPlacementListHandler.get_all_items(allPlacements):
	line = str(placement['id']) + ';' + placement['name'] + ';'  + placement['site_name'] + ';'  + str(placement['is_resizable']) + '\n' 
	writer_content.append(line)

fw = FileWriter(filename, 'w')

for line in writer_content:
	print(line)
	print("---")
	fw.writeInNewFile(line)

fw.closeFile()
