import json
from lib.auth import Auth, AuthException
from lib.httpHandler import HttpHandler
from lib.fileWriter import FileWriter
from worker.allLineitemCheck.allLineitemsCheck import AllLineitemsCheck

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

filename = "all_campaign_date.csv"

http = HttpHandler(proxies, "http://api.appnexus.com")

a = Auth()

aquireAuthToken(a, http)

params = {'stats':'true', 'interval':'7day'}
count = http.getRequestPage(0, "campaign", params).json()['response']['count']

allLineItems = list()

for start_element in range(0, count, 100):
	resp = http.getRequestPage(start_element, "campaign", params).json()['response']
	if 'error_id' in resp:
		print(resp)
	else:
		allLineItems.append(resp['campaigns'])

allLineitems = AllLineitemsCheck()

writer_content = list()
writer_content.append('Id;Name;imps last 7 days;\n')

# Low running items
writer_content.append('\n')
writer_content.append('All Campaigns \n')
writer_content.append('\n')

for campaign in allLineitems.get_all_items(allLineItems):
	line = str(campaign['id']) + ';' + campaign['name'] + ';'
	if campaign['stats'] is not None:
		line += campaign['stats']['imps']
	line += '\n' 
	
	writer_content.append(line)

fw = FileWriter(filename, 'w')

for line in writer_content:
	print(line)
	print("---")
	fw.writeInNewFile(line)

fw.closeFile()
