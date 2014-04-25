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
        print("Login mit Zugang {} nicht mÃ¶glich.".format(e.login))
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

# Alternativ liste hardgecodet:
ym_rules = (363924, 366025, 362260, 266772, 367450, 369238, 392665, 396096, 265558, 359200, 369239, 392487, 373059, 384973, 359201, 388815, 270614, 270318, 265745, 268332, 267277, 261059, 330593, 261057, 260949, 260948, 263478, 260947, 261060, 261061, 256153, 261112, 261116, 261118, 261119, 262211, 261121, 261127, 256227, 262210, 277816, 256235, 270345, 261408, 261412, 261413, 261416, 261417, 261419, 261420, 256244, 256246, 268983, 261481, 268722, 258045, 256317, 269266, 261120, 267282, 256200, 258044, 258042, 258043, 285744, 256400, 256413, 326472, 268982, 261273, 261480, 261424, 280296, 261324, 389105, 256534, 256477, 359259, 256461, 256376, 268720, 280295, 262208, 268331, 262209, 256337, 274737, 257985, 256548, 316432, 256474, 256372, 266424, 316405, 256440, 389826, 261346, 263477, 256520, 256472, 256325, 261197, 256288, 261406, 256298, 365945, 379507, 256371, 369827, 256457, 290503, 261427, 257584, 256345, 267173, 258954, 256327, 258863, 256366, 256355)

number = 1
for ym_rule_id in ym_rules:
    print('Fortschritt: ' + str(number) + ' / ' + str(len(ym_rules)))
    params = {'id':str(ym_rule_id)}
    ym_rule = http.getRequest('ym-floor', params).json()['response']['ym-floor']
    params = {'id':str(ym_rule['profile_id'])}
    #params = {'id':line_item}

    #resp_profile = http.getRequest("profile", params).json()['response']['profile']
    payload = {'profile':{"size_targets":[{"width":120,"height":600},{"width":160,"height":600},{"width":200,"height":600},{"width":300,"height":250},{"width":468,"height":60},{"width":728,"height":90}]}}

    resp = http.putRequest(payload, "profile", params).json()['response']
    print(resp['status'])
    number+=1

