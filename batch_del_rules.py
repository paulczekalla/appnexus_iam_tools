import json
import copy
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

http = HttpHandler(proxies, "http://api.appnexus.com")

a = Auth()

aquireAuthToken(a, http)

rules = (124438,127020)

number = 1
for rule_id in rules:
    print('Fortschritt: ' + str(number) + ' / ' + str(len(rules)))
    params = {'id':str(rule_id)}
    
    resp = http.deleteRequest("ym-floor", params).json()['response']
    print(resp['status'])
    number+=1


