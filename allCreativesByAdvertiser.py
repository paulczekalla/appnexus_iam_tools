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

filename = "all_creatives.csv"

http = HttpHandler(proxies, "http://api.appnexus.com")

a = Auth()

aquireAuthToken(a, http)

params = {'advertiser_id':'58227'}

count = http.getRequest("campaign", params).json()['response']['count']

allCampaigns = list()

for start_element in range(0, count, 100):
    resp = http.getRequestPage(start_element, "campaign", params).json()['response']
    if 'error_id' in resp:
        print(resp)
    else:
        for campaign in resp['campaigns']:
            allCampaigns.append(campaign)

writer_content = list()
writer_content.append('Id;Name;creatives;\n')

# Low running items
writer_content.append('\n')
writer_content.append('All Creatives \n')
writer_content.append('\n')

for campaign in allCampaigns:
    line = str(campaign['id']) + ';' + campaign['name'] + ';'
    if campaign['creatives'] is not None:
        for creative in campaign['creatives']:
            line += str(creative['id']) + ';'
    line += '\n'

    writer_content.append(line)

fw = FileWriter(filename, 'w')

for line in writer_content:
    print(line)
    print("---")
    fw.writeInNewFile(line)

fw.closeFile()
