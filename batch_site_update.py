import json
import csv
from lib.auth import Auth, AuthException
from lib.httpHandler import HttpHandler
from lib.fileWriter import FileWriter

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

filename = "new_site_types.csv"

http = HttpHandler(proxies, "http://api.appnexus.com")

a = Auth()

aquireAuthToken(a, http)

writer_content = list()
writer_content.append('publisher_id;site;supply type\n')

with open('placement_app_mobile.csv') as f:
	f_csv = csv.reader(f)
	for row in f_csv:
		params = {'publisher_id':str(row[0])}
		sites = http.getRequest("site", params).json()['response']['sites']
		for site in sites:
			params = {'id':str(site['id'])}
			payload = {"site":{"supply_type":row[1]}}
			status = http.putRequest(payload, "site", params).json()['response']['status']
			writer_string = str(row[0]) + '; ' + site['name'] + ';' + row[1] + '\n'
			writer_content.append(writer_string)

fw = FileWriter(filename, 'w')

for line in writer_content:
	fw.writeInNewFile(line)

fw.closeFile()