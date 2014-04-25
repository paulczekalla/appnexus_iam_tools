import json
from lib.auth import Auth
from lib.httpHandler import HttpHandler

http = HttpHandler()
a = Auth()

token = a.readResponse(a.authorizationRequest(http))
http.setToken(token)

count = http.getRequestPage(0, "line-item").json()['response']['count']

allAineItems = list()

for start_element in range(4300, count, 100):
	lineItemsNew = http.getRequestPage(start_element, "line-item").json()['response']['line-items']
	allAineItems.append(lineItemsNew)

allLowLineItems = list()
	
for lineItemArr in allAineItems:
	for lineItem in lineItemArr:
		if lineItem['lifetime_budget'] is not None and lineItem['all_stats'] is not None:
			if float(lineItem['lifetime_budget']) > float(lineItem['all_stats']['lifetime']['revenue'])*2.0:
				if '7day' in lineItem['all_stats'] and int(lineItem['all_stats']['7day']['imps']) < 7000:
					allLowLineItems.append(lineItem)
				elif 'yesterday' in lineItem['all_stats'] and int(lineItem['all_stats']['yesterday']['imps']) < 1000:
					allLowLineItems.append(lineItem)


for lineItem in allLowLineItems:
	print(lineItem['name'] + '(' + str(lineItem['id']) + ')')
			