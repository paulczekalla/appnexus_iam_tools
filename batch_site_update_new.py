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
        print("Login mit Zugang {} nicht mÃ¶glich.".format(e.login))
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

response = http.getRequest("site").json()['response']
#print(response)
count = response['count']
sites = list()

for start_element in range(0, count, 100):
    resp = http.getRequestPage(start_element, "site").json()['response']
    for site in resp['sites']:
        sites.append(site)


number = 1
for site in sites:
    print('Fortschritt: ' + str(number) + ' / ' + str(len(sites)))
    params = {'id':str(site['id'])}
    payload = {'site':{"intended_audience":"general", "audited":"true"}}

    resp = http.putRequest(payload, "site", params).json()['response']
    print(resp['status'])
    number+=1

