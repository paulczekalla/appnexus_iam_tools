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

os_exclude = [
  {"id":1, "action":"exclude"},
  {"id":2, "action":"exclude"},
  {"id":6, "action":"exclude"},
  {"id":7, "action":"exclude"},
  {"id":8, "action":"exclude"}
]

device_exclude = [
  {"id":301, "action":"exclude"},
  {"id":302, "action":"exclude"},
  {"id":303, "action":"exclude"},
  {"id":304, "action":"exclude"}
]


http = HttpHandler(proxies, "http://api.appnexus.com")

a = Auth()

aquireAuthToken(a, http)

campaigns = (2507286,2563197,2507293,2507295,2654152,2654212,2531893,2558858,2561660,2652080,2658719,2531894,2559005,2531897,2559028,2531898,2546276,2652152,2652194,2658721,2558450,2561318,2559327,2596785,2623720,2652085,2658720,2596816,2596847,2596700,2652153,2652195,2658722,2596761,2596883,2597262,2558856,2561659,2559003,2559027,2546270,2558448,2559265,2559325,2563213,2563214,2563215,2563216,2623905)

filename = "log_updated_campaigns.csv"

writer_content = list()
writer_content.append('Id;Name;Status;os Targets; Old Targets; dev target; old targets\n')

for campaign_id in campaigns:
	params = {'id':str(campaign_id)}
	campaign = http.getRequest("campaign", params).json()['response']['campaign']
	params = {'id':str(campaign['profile_id'])}
	profile = http.getRequest("profile", params).json()['response']['profile']
	
	profile_exclude = list(os_exclude)
	old_targets = ""
	if profile['operating_system_family_targets'] is not None:
		for target in profile['operating_system_family_targets']:
			profile_exclude.append(target)
			old_targets += str(target) + ' '
	
	profile_device_exclude = list(device_exclude)
	old_dev_targets = ""
	if profile['device_model_targets'] is not None:
		for target in profile['device_model_targets']:
			profile_device_exclude.append(target)
			old_dev_targets += str(target) + ' '
			
	print(profile_device_exclude)
	
	payload = {"profile":{"operating_system_family_targets":profile_exclude, "device_model_targets":profile_device_exclude}}
	publisher_targets = payload
	status = http.putRequest(payload, "profile", params).json()['response']['status']
	writer_string = str(campaign_id) + '; ' + campaign['name'] + '; ' + status + ';' + str(profile_exclude) + '; ' + old_targets + ';' + str(profile_device_exclude) + ';' + old_dev_targets + '\n'
	writer_content.append(writer_string)

fw = FileWriter(filename, 'w')

for line in writer_content:
	fw.writeInNewFile(line)

fw.closeFile()
