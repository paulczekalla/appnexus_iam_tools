﻿import json
import copy
import time
from lib.auth import Auth, AuthException
from lib.httpHandler import HttpHandler
from lib.fileWriter2 import FileWriter

def aquireAuthToken(authObj, http):
    token = ""
    try:
        token = authObj.readResponse(authObj.authorizationRequest(http))
        global token2
        token2 = token
    except AuthException as e:
        print("Login mit Zugang {} nicht moeglich.".format(e.login))
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

print(token2)
payload = {"report":{"report_type":"network_analytics","columns":["day", "hour", "buyer_member_id", "advertiser_id", "publisher_id", "placement_id", "line_item_id", "campaign_id", "campaign_priority", "size", "brand_id", "bid_type", "revenue_type", "deal_id", "imps", "imps_blank", "imps_kept", "imps_resold", "imp_type", "clicks", "revenue"], "publisher_id":"145560", "start_date":"2014-03-30 23:00:00","end_date": "2014-03-31 23:59:59","format":"csv", "emails":["p.czekalla@interactivemedia.net"], "timezone":"Europe/Berlin"}}
# Request Report
status = http.postRequest(payload, "report").json()['response']

# Pruefen, ob keien Fehlern aufgetreten sind
if 'error' in status:
    print(status)
    print("Something went wrong.")
else:
    print(status['report_id'])
reportID = status['report_id']
params = {'id':reportID}

# Warten bis Report erstellt wurde
print("Waiting for generating report by appnexus")
time.sleep(20)


# Abfragen der Download-URL
downloadURL = http.getRequest("report", params).json()['response']
readydownload = downloadURL['execution_status']
report_download_done = False

if 'error' in downloadURL:
    print(downloadURL)
    print("Something went wrong.")
else:
	while not(report_download_done):
		if readydownload == "pending":
			print("Noch nicht fertig. Neuer Versuch erfolgt in Kürze.")
			time.sleep(5)
			downloadURL = http.getRequest("report", params).json()['response']
			readydownload = downloadURL['execution_status']
		else:
			print(readydownload)
			filedownload = downloadURL['report']['url']
			print(filedownload)
			downloadedReport = http.getRequest(filedownload)
			fileWriter = FileWriter("new_report.csv", "w")
			fileWriter.writeReportInNewFile(downloadedReport.content)
			report_download_done = True




