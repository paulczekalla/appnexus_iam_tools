import json
import re
from lib.auth import Auth, AuthException
from lib.httpHandler import HttpHandler
from lib.fileWriter import FileWriter
from worker.newtensionCreatives.allCreativesCheck import AllCreativesCheck

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

filename = "newtension_creatives.csv"

http = HttpHandler(proxies, "http://api.appnexus.com")

a = Auth()

aquireAuthToken(a, http)

count = http.getRequestPage(0, "creative").json()['response']['count']

allCreatives = list()

print('**************************************\n')
print('Starte Suchlauf über ' + str(count) + ' Creatives\n')
print('**************************************\n')
for start_element in range(0, count, 100):
	resp = http.getRequestPage(start_element, "creative").json()['response']
	if 'error_id' in resp:
		print(resp)
	else:
		allCreatives.append(resp['creatives'])

allCreativesInst = AllCreativesCheck()

writer_content = list()
writer_content.append('Id;name;brand_id\n')

# Low running items
writer_content.append('\n')
writer_content.append('\n')

for item in allCreativesInst.get_all_items(allCreatives):
	if item['content'] is not None and item['state'] == 'active':
		if 'newtention' in item['content']:
			line = str(item['id']) + ';' + item['name'] + ';' + str(item['brand_id']) + ';' + '\n'
			print(item['name'])
			writer_content.append(line)

fw = FileWriter(filename, 'w')

for line in writer_content:
	fw.writeInNewFile(line)

fw.closeFile()
