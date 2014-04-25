import json
from lib.auth import Auth, AuthException
from lib.httpHandler import HttpHandler
from lib.fileWriter import FileWriter
from worker.deleteNeverRunCampaign.NeverRunCampaign import NeverRunCampaign

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

filename = "deleted_campaigns.csv"

http = HttpHandler(proxies, "http://api.appnexus.com")

a = Auth()

aquireAuthToken(a, http)

count = http.getRequestPage(0, "campaign").json()['response']['count']

params = {'stats':'true', 'interval':'lifetime'}
count = http.getRequestPage(0, 'campaign', params).json()['response']['count']

deletedCampaigns = list()

for start_element in range(0, count, 100):
	campaign = http.getRequestPage(start_element, "campaign", params).json()['response']['campaigns']
	deletedCampaigns.append(campaign)


neverRunCampaignWorker = NeverRunCampaign()

writer_content = list()
writer_content.append('Id;Name;Start;\n')


for validCampaign in neverRunCampaignWorker.check_if_opt_campaign_never_run(deletedCampaigns):
	params = {'id':str(validCampaign['id']), 'advertiser_id':str(validCampaign['advertiser_id'])}
	status = http.deleteRequest("campaign", params).json()['response']['status']
	if status == 'OK':
		writer_string = str(validCampaign['id']) + ';' + validCampaign['name'] + ';'
		if validCampaign['start_date'] is not None:
			writer_string += validCampaign['start_date'].split(" ")[0]
		writer_string += ';\n'

		writer_content.append(writer_string)
	
fw = FileWriter(filename, 'w')

for line in writer_content:
	print(line)
	print("---")
	fw.writeInNewFile(line)

fw.closeFile()
