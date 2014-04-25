import json
import copy
from lib.auth import Auth, AuthException
from lib.httpHandler import HttpHandler
from lib.fileWriter import FileWriter
from worker.generic.AbstractGenericWorker import AbstractGenericWorker

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

http = HttpHandler(proxies, "http://api.appnexus.com")

a = Auth()

aquireAuthToken(a, http)

filename = "global_klicker_opt_campaigns.csv"

worker = AbstractGenericWorker(http)
campaigns = worker.getAllEntitiesByType('campaign')

writer_content = list()
writer_content.append('Id;Name\n')

count = len(campaigns)
i = 1

for campaign in campaigns:
	print(str(i) + ' / ' + str(count))
	params = {'id':str(campaign['profile_id'])}
	resp = http.getRequest("profile", params).json()['response']
	if 'profile' in resp:
		profile = resp['profile']
		if profile['segment_group_targets'] is not None:
			for segment_group_target in profile['segment_group_targets']:
				for segment in segment_group_target['segments']:
					if segment['action'] == 'include' and segment['id'] == 467564:
						writer_string = str(campaign['id']) + '; ' + campaign['name'] + '\n'
						writer_content.append(writer_string)
		else:
			print("No Segment Targets for this profile")
	else:
		print("No profile avaiable for campaign: " + str(campaign['id']))
	i+=1

fw = FileWriter(filename, 'w')

for line in writer_content:
	fw.writeInNewFile(line)

fw.closeFile()
