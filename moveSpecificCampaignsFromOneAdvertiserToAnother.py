import json
import time
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

# XPLOSION
old_advertiser_id = '106696'
new_advertiser_id = '160667'

# TEST
#old_advertiser_id = '58227'
#new_advertiser_id = '101854'


proxies = {
  "http": "http://proxy.t-online.net:3128",
  "https": "http://proxy.t-online.net:3128",
}

filename = "all_profiles.csv"

http = HttpHandler("http://api.appnexus.com", proxies)

a = Auth()

aquireAuthToken(a, http)

params = {'advertiser_id':old_advertiser_id}

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
    if 'TripleAds' in campaign['name']:
    #if 'Test' in campaign['name']:
    #if '6006' in campaign['name']:

        campaign_new = campaign

        #line = str(campaign['id']) + ';' + campaign['name'] + ';'
        params = {'id':str(campaign['profile_id'])}
        profile = http.getRequest("profile", params).json()['response']['profile']

        print('old profile: ' + str(profile['id']))

        #Clone Campaign Profile
        profile['advertiser_id'] = new_advertiser_id
        profile['id'] = ''
        profile['created_on'] = ''
        profile['last_modified'] = ''

        payload = {'profile':profile}
        params = {'advertiser_id':new_advertiser_id}
        campaign_profile_id = http.postRequest(payload, 'profile', params).json()['response']['id']

        print('new profile: ' + str(campaign_profile_id))


        # GET LINE-ITEM

        print('old line-item: ' + str(campaign['line_item_id']))

        params = {'id':str(campaign['line_item_id'])}
        line_item = http.getRequest('line-item', params).json()['response']['line-item']

        # CLONE PROFILE from LINEITEM

        params = {'id':str(line_item['profile_id'])}
        line_item_profile = http.getRequest('profile', params).json()['response']['profile']

        line_item_profile['advertiser_id'] = new_advertiser_id
        del line_item_profile['id']
        del line_item_profile['created_on']
        del line_item_profile['last_modified']

        payload = {'profile':line_item_profile}
        params = {'advertiser_id':new_advertiser_id}
        line_item_profile_id = http.postRequest(payload, 'profile', params).json()['response']['id']


        # CLONE LINE ITEM
        del line_item['id']
        line_item['advertiser_id'] = new_advertiser_id
        #line_item['campaigns'] =
        line_item['advertiser'] = {'id': str(new_advertiser_id)} #, 'name': ''}
        line_item['profile_id'] = line_item_profile_id

        payload = {'line-item':line_item}
        params = {'advertiser_id':new_advertiser_id}

        time.sleep(5)
        new_line_item = http.postRequest(payload, 'line-item', params).json()['response']

        print(new_line_item)
        lineitem_id = new_line_item['id']
        print('new line item: ' + str(lineitem_id))

        # CLONE CREATIVES & CREATIVE PROFILE

        new_creative_ids = list()
        for creative in campaign['creatives']:
            params = {'id':str(creative['id'])}
            creative_object = http.getRequest('creative', params).json()['response']['creative']

            # CLONE PROFILE from Creative

            params = {'id':str(creative_object['profile_id'])}
            creative_profile = http.getRequest('profile', params).json()['response']['profile']

            creative_profile['advertiser_id'] = new_advertiser_id
            del creative_profile['id']
            del creative_profile['created_on']
            del creative_profile['last_modified']

            payload = {'profile':creative_profile}
            params = {'advertiser_id':new_advertiser_id}
            creative_profile_id = http.postRequest(payload, 'profile', params).json()['response']['id']

            # CLONE CREATIVE

            creative_object['state'] = 'active'
            creative_object['advertiser_id'] = new_advertiser_id
            creative_object['profile_id'] = creative_profile_id

            del creative_object['folder']
            del creative_object['id']
            del creative_object['ssl_status']
            payload = {'creative':creative_object}
            params = {'advertiser_id':new_advertiser_id}

            #print(payload)
            time.sleep(5)
            response = http.postRequest(payload, 'creative', params).json()['response']
            print(response)
            creative_id = response['id']
            new_creative_ids.append({'id': int(creative_id)})


        # CLONE CAMPAIGN
        print('old campaign: ' + str(campaign['id']))

        del campaign_new['id']
        campaign_new['advertiser_id'] = new_advertiser_id
        campaign_new['line_item_id'] = str(lineitem_id)
        del campaign_new['creative_id']
        campaign_new['profile_id'] = str(campaign_profile_id)
        campaign_new['creatives'] = new_creative_ids
        #campaign_new['creatives'] = None

        payload = {'campaign':campaign}
        params = {'advertiser_id':new_advertiser_id}
        #print(payload)
        time.sleep(5)
        response_campaign = http.postRequest(payload, 'campaign', params).json()['response']

        print(response_campaign)
        campaign_id = response_campaign['id']
        print('new campaign ' + str(campaign_id))

    #line += str(profile) + ';'
    #line += '\n'

    #writer_content.append(line)


fw = FileWriter(filename, 'w')

for line in writer_content:
    print(line)
    print("---")
    fw.writeInNewFile(line)

fw.closeFile()
