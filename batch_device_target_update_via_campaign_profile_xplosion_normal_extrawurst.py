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

response = http.getRequest("campaign", params).json()['response']
#print(response)
count = response['count']
campaigns = list()

for start_element in range(100, count, 100):
    resp = http.getRequestPage(start_element, "campaign", params).json()['response']
    for campaign in resp['campaigns']:
        campaigns.append(campaign)


#print(campaigns['id'])

# Alternativ liste hardgecodet:
#campaigns = (7124618,7124628)

number = 1
for campaign in campaigns:
    print('Fortschritt: ' + str(number) + ' / ' + str(len(campaigns)))
    params = {'id':str(campaign['profile_id'])}
    #params = {'id':str(campaign)}

    pub_targets = http.getRequest("profile", params).json()['response']['profile']['publisher_targets']
    
    if pub_targets is not None:
        for pub in pub_targets:
            if str(pub['id']) == '145618':
                pub['action'] = 'exclude'
        pub_targets.append({"id":"145618", "action":"exclude"})
    else:
        pub_targets = [{"id":"145618", "action":"exclude"}]
    
    payload = {'profile':{'publisher_targets':pub_targets}}
    print(payload)

    resp = http.putRequest(payload, "profile", params).json()['response']
    print(resp)
	#print(resp['status'])


    number+=1

