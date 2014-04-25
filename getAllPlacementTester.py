import json
import copy
import time
from lib.auth import Auth, AuthException
from lib.httpHandler import HttpHandler
from lib.fileWriter import FileWriter
from worker.generic.AbstractGenericWorker import AbstractGenericWorker
from entity.placement import Placement

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



def getPlacement(placement_id):    
    params = {'id':str(placement_id)}
    response_placement = http.getRequest('placement', params).json()['response']
    if 'placement' in response_placement:
        return response_placement['placement']
    else:
        return None


proxies = {
  "http": "http://proxy.t-online.net:3128",
  "https": "http://proxy.t-online.net:3128",
}

http = HttpHandler("http://api.appnexus.com")

a = Auth()

aquireAuthToken(a, http)

filename = "all_site_ALL_categories.csv"

worker = AbstractGenericWorker(http)
#sites = worker.getAllEntitiesByType('site')
sites = worker.getAllEntitiesByRange('site', 900, 1200)

print(len(sites))

for site in sites:
    print(site['name'])