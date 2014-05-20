import json
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

filename = "all_lineitem.csv"

http = HttpHandler(proxies, "http://api.appnexus.com")

a = Auth(http)

aquireAuthToken(a, http)

with open('qisma_creative_import.csv', 'r') as f:
    for line in f:
        splited_line = line.split(';')
        pub_name = splited_line[0]
        pub_id = splited_line[1]
        code = splited_line[2]
        v_size = splited_line[3]
        h_size = splited_line[4]
