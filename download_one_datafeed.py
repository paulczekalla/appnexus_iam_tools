import json
import time
from lib.auth import Auth,AuthException

from lib.httpHandler import HttpHandler
from worker.siphon.feedGenerator import FeedGenerator
from worker.siphon.SiphonDownloader import SiphonDownloader

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

downloader = SiphonDownloader("temp", http)

params = {"siphon_name":"bid_landscape_feed","hour":"2014_04_07_09", "timestamp":"20140407104511", "split_part":"0"}

downloader.download_file(params)
