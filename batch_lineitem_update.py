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

# Advertiser Xplosion 2
params = {'advertiser_id':'160667'}
# Seite 2 (ab Lineitem 100)
resp = http.getRequestPage(100, "line-item", params).json()['response']

lineitems = list()
for line_item in resp['line-items']:
    lineitems.append(line_item['id'])

print(lineitems)

# Alternativ liste hardgecodet:
#lineitems = (942799,942841,942847)

number = 1
for line_item_id in lineitems:
    print('Fortschritt: ' + str(number) + ' / ' + str(len(lineitems)))
    params = {'id':str(line_item_id), 'advertiser_id':160667}
    payload = {'line-item':{'revenue_value':'0.3'}}

    resp = http.putRequest(payload, "line-item", params).json()['response']
    print(resp['status'])
    number+=1

