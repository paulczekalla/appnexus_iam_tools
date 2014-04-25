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

filename = "all_profiles.csv"

http = HttpHandler(proxies, "http://api.appnexus.com")

a = Auth()

aquireAuthToken(a, http)

params = {'advertiser_id':'106696'}

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
writer_content.append('Id;Name;Profile;\n')

# Low running items
writer_content.append('\n')
writer_content.append('All Profiles \n')
writer_content.append('\n')

for campaign in allCampaigns:
    line = str(campaign['id']) + ';' + campaign['name'] + ';'
    params = {'id':str(campaign['profile_id'])}
    profile = http.getRequest("profile", params).json()['response']['profile']
    ''' TO DO Profile
    profile['advertiser_id'] = ''
    profile['id'] = ''
    profile['created_on'] = ''
    profile['last_modified'] = ''

    # POST PROFILE
    get ID
    '''

    ''' TO DO Lineitem
    params = {'id':str(campaign['line_item_id'])}
    line-item = http.getRequest("line-item", params).json()['response']['line-item']
    line-item['id'] =
    line-item['name'] =
    line-item['advertiser_id'] =
    line-item['start_date'] =
    line-item['campaigns'] =
    line-item['last_modified'] =
    line-item['advertiser'] = {'id': '', 'name': ''}
    line-item['profile_id'] =

    # POST LINE-ITEM
    get ID
    '''

    '''
    campaign_new = campaign
    campaign_new['id'] =
    campaign_new['advertiser_id'] =
    campaign_new['line_item_id'] =
    campaign_new['creative_id'] =
    campaign_new['profile_id'] =
    campaign_new['creatives'] = {}

    '''

    line += str(profile) + ';'
    line += '\n'

    writer_content.append(line)

fw = FileWriter(filename, 'w')

for line in writer_content:
    print(line)
    print("---")
    fw.writeInNewFile(line)

fw.closeFile()
