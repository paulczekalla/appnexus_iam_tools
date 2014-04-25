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

filename = "all_ym_floors.csv"

http = HttpHandler(proxies, "http://api.appnexus.com")

a = Auth()

aquireAuthToken(a, http)

count = http.getRequest("ym-floor").json()['response']['count']

allYmFloors = list()

for start_element in range(0, count, 100):
    resp = http.getRequestPage(start_element, "ym-floor").json()['response']
    if 'error_id' in resp:
        print(resp)
    else:
        for floor in resp['ym-floors']:
            allYmFloors.append(floor)

writer_content = list()
writer_content.append('Id;Name;last modified; hard_floor; soft_floor; prio; ym_profile_id; profile id;\n')


for ym_floor in allYmFloors:
    line = str(ym_floor['id']) + ';' + ym_floor['name'] + ';' + ym_floor['last_modified'] + ';'
    if ym_floor['hard_floor'] is not None: 
        line += str(ym_floor['hard_floor']) + ';' 
    else:
        line += ';'
    
    if ym_floor['soft_floor'] is not None: 
        line += str(ym_floor['soft_floor']) + ';' 
    else:
        line += ';'
     
    line += str(ym_floor['priority']) + ';'     
    
    if ym_floor['ym_profile_id'] is not None: 
        line += str(ym_floor['ym_profile_id']) + ';' 
    else:
        line += ';'
        
    if ym_floor['profile_id'] is not None: 
        line += str(ym_floor['profile_id']) + ';' 
    else:
        line += ';'

    if ym_floor['brands'] is not None:
        for brand in ym_floor['brands']:
            line += brand['name'] + ' __ '
    line += ';'
            
    if ym_floor['members'] is not None:
        for member in ym_floor['members']:
            line += member['name'] + ' __ '
    line += ';'
            
    if ym_floor['categories'] is not None:
        for category in ym_floor['categories']:
            line += category['name'] + ' __ '

    line += '\n'

    writer_content.append(line)

fw = FileWriter(filename, 'w')

for line in writer_content:
    print(line)
    print("---")
    fw.writeInNewFile(line)

fw.closeFile()
