import json
from lib.auth import Auth, AuthException
from lib.httpHandler import HttpHandler
from lib.fileWriter import FileWriter
from worker.lowRunning.LowRunning import LowRunning

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

filename = "low_running_lineitems.csv"

http = HttpHandler(proxies, "http://api.appnexus.com")

a = Auth()

aquireAuthToken(a, http)

count = http.getRequestPage(0, "line-item").json()['response']['count']

allLineItems = list()

for start_element in range(0, count, 100):
	lineItemsNew = http.getRequestPage(start_element, "line-item").json()['response']['line-items']
	allLineItems.append(lineItemsNew)

params = {'never_run':'true'}
count = http.getRequestPage(0, 'line-item', params).json()['response']['count']

allNeverLineItems = list()

for start_element in range(0, count, 100):
	params = {'never_run':'true'}
	lineItemsNew = http.getRequestPage(start_element, "line-item", params).json()['response']['line-items']
	allNeverLineItems.append(lineItemsNew)


lowRunningWorker = LowRunning()

writer_content = list()
writer_content.append('Id;Name;Start;Ende;\n')

# Low running items
writer_content.append('\n')
writer_content.append('Low running Lineitems \n')
writer_content.append('\n')

for lineItem in lowRunningWorker.check_low_running_items(allLineItems):
	if lineItem['state'] != 'inactive':
		writer_content.append(str(lineItem['id']) + ';' + lineItem['name'] + ';' + lineItem['start_date'].split(" ")[0] + ';' + lineItem['end_date'].split(" ")[0] + ';\n')

# Never running items
writer_content.append('\n')
writer_content.append('Never run Lineitems \n')
writer_content.append('\n')

for lineItem in lowRunningWorker.check_never_running_items(allNeverLineItems):
	if lineItem['end_date'] is not None:
		writer_content.append(str(lineItem['id']) + ';' + lineItem['name'] + ';' + lineItem['start_date'].split(" ")[0] + ';' + lineItem['end_date'].split(" ")[0] + ';\n')
	else:
		writer_content.append(str(lineItem['id']) + ';' + lineItem['name'] + ';' + lineItem['start_date'].split(" ")[0] + ';' + 'Kein Enddatum;\n')

fw = FileWriter(filename, 'w')

for line in writer_content:
	print(line)
	print("---")
	fw.writeInNewFile(line)

fw.closeFile()
