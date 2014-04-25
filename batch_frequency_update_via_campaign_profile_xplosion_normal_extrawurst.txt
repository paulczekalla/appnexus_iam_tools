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
params = {'advertiser_id':'106696'}
# Noch nicht für alle Entitäten automatisiert durchführbar. Läuft per Hand das 100 inkrement
# Seite 2 (ab Lineitem 100)

count = http.getRequest("line-item", params).json()['response']['count']

lineitems = list()

for start_element in range(0, count, 100):
    resp = http.getRequestPage(start_element, "line-item", params).json()['response']
    for line_item in resp['line-items']:
        lineitems.append(line_item)


#print(lineitems['id'])

# Alternativ liste hardgecodet:
#lineitems = (8284000,8284292)

number = 1
for line_item in lineitems:
    print('Fortschritt: ' + str(number) + ' / ' + str(len(lineitems)))
    if 'TripleAds' in line_item['name']:
        params = {'id':line_item['profile_id']}
        #params = {'id':line_item}

        #resp_profile = http.getRequest("profile", params).json()['response']['profile']
        payload = {'profile':{'max_day_imps':'40'}}

        resp = http.putRequest(payload, "profile", params).json()['response']
        print(resp['status'])
    else:
        print('Keine TrippleAds Lineitem')
        print(line_item['name'])

    number+=1

