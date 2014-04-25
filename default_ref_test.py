import json
import requests
from lib.auth import Auth,AuthException
from lib.fileWriter import FileWriter 
from lib.httpHandler import HttpHandler
from worker.generic.AbstractGenericWorker import AbstractGenericWorker

def aquireAuthToken(authObj, http):
	token = ''
	try:
		token = authObj.readResponse(authObj.authorizationRequest(http))
	except AuthException as e:
		print('Login mit Zugang {} nicht möglich.'.format(e.login))
		print('Zugangsdaten erneut eingeben: ')
		login = input('Login: ')
		password = input('Passwort: ')
		aquireAuthToken(Auth(login, password), http)
	else:
		print(token)
		http.setToken(token)

http = HttpHandler()

a = Auth()
aquireAuthToken(a, http)

worker = AbstractGenericWorker(http, "http://api.appnexus.com")

placements = worker.getAllEntitiesByRange('placement', 500, 550)

print(len(placements))

'''
for place in placements:
	hex_id = str(hex(place['site_id'])).split("0x")[1]
	url = "interactivemedia-" + str(hex_id) + ".net"
	code = "-----"
	if place['code'] is not None:
		code = place['code']
	writer_content.append(str(place['id']) + ';' + place['name'] + ';' + code + ';' + url + ';' + str(place['site_id']) + ';' + place['site_name'] + ';' + place['publisher_name'] + '\n')

'''