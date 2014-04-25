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

response = http.getRequest("placement").json()['response']
#print(response)
count = response['count']
placements = list()

for start_element in range(4900, count, 100):
    resp = http.getRequestPage(start_element, "placement").json()['response']
    for placement in resp['placements']:
        placements.append(placement)


number = 1
for placement in placements:
    print('Fortschritt: ' + str(number) + ' / ' + str(len(placements)))
    params = {'id':str(placement['id'])}
    payload = {'placement':{"intended_audience":"general", "audited":"true", "audit_level":"placement"}}

    resp = http.putRequest(payload, "placement", params).json()['response']
    print(resp)
    number+=1

