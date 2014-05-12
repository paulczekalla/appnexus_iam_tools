import json
import time
from lib.auth import Auth, AuthException
from lib.httpHandler import HttpHandler
from lib.fileWriter2 import FileWriter

proxies = {
  "http": "http://proxy.t-online.net:3128",
  "https": "http://proxy.t-online.net:3128",
}


http = HttpHandler("http://api.appnexus.com")
a = Auth()
a.aquireAuthToken(http)

start_value = "2014-04-28 00:00:00"
end_value = "2014-04-29 00:00:00"


# Auswahl des Report-Types sowie der Dimensionen und Metriken

# Bulk Feed
report_columns = ["day", "seller_member_id", "advertiser_id","line_item_id","campaign_id", "creative_id", "size", "publisher_id", "site_id", "placement_id", "bid_type", "pub_rule_id", "revenue_type", "payment_type", "imps", "clicks", "post_click_convs", "post_view_convs", "total_convs", "profit", "revenue", "media_cost", "total_network_rpm", "ppm"]
report_type_paramter = "network_analytics_feed"

# Analytics Report
#report_columns = ["day", "seller_member_id", "seller_member_name", "advertiser_id", "advertiser_id", "line_item_id", "line_item_name","campaign_id", "campaign_name", "brand_id", "brand_name", "geo_country_name", "size", "bid_type", "publisher_id", "site_id", "placement_id", "bid_type", "pub_rule_id", "revenue_type", "payment_type", "imps", "clicks", "ctr", "post_click_convs", "post_view_convs", "total_convs", "revenue", "cost", "profit", "total_network_rpm", "cpm", "rpm", "ppm"]
#report_type_paramter = "network_analytics"


payload = {"report":{"report_type":report_type_paramter,"columns":report_columns, "start_date":start_value,"end_date": end_value,"format":"excel","timezone":"Europe/Berlin", "escape_fields":"true", "reporting_decimal_type":"periode"}}


# Request Report
status = http.postRequest(payload, "report").json()['response']

# Pruefen, ob kein Fehlern aufgetreten sind
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

