import json
from lib.auth import Auth, AuthException
from lib.httpHandler import HttpHandler
from lib.fileWriter import FileWriter
from worker.allEntityCheck.allEntityCheck import AllEntityCheck

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

filename = "all_rule_check.csv"

http = HttpHandler(proxies, "http://api.appnexus.com")

a = Auth()

aquireAuthToken(a, http)

count = http.getRequestPage(0, "ym-floor").json()['response']['count']

allRules = list()

for start_element in range(0, count, 100):
    resp = http.getRequestPage(start_element, "ym-floor").json()['response']
    if 'error_id' in resp:
        print(resp)
    else:
        allRules.append(resp['ym-floors'])

allEntityCheckInstance = AllEntityCheck()

writer_content = list()
writer_content.append('Id;Name;Prio;Hard Floor\n')

# Low running items
writer_content.append('\n')
writer_content.append('All Rules \n')
writer_content.append('\n')

for rule in allEntityCheckInstance.get_all_items(allRules):
    if rule['members'] is None and rule['brands'] is None and rule['categories'] is None:
        line = str(rule['id']) + ';' + rule['name'] + ';' + str(rule['priority']) + ';' + str(rule['hard_floor']) + '\n' 
        writer_content.append(line)

fw = FileWriter(filename, 'w')

for line in writer_content:
    print(line)
    print("---")
    fw.writeInNewFile(line)

fw.closeFile()
