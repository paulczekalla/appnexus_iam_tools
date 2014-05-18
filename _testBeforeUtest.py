import json
import time
from lib.auth import Auth, AuthException
from lib.httpHandler import HttpHandler
from lib.fileWriter2 import FileWriter
from worker.generic.AbstractGenericWorker import AbstractGenericWorker
from worker.campaignWorker.BasicCampaignWorker import BasicCampaignWorker

def main():

    http = HttpHandler("http://api.appnexus.com")
    a = Auth()
    a.aquireAuthToken(http)

    testSearch(http, 'adidas')
    testMinRunDate(http, '2014-05-01+00:00:00')
    testSapNumber(http, 'adidas')

# not real tests, just preparation
def testSearch(http, searchterm):
    testClass = AbstractGenericWorker(http)
    print(len(testClass.getAllEntitiesBySearchTerm('campaign', searchterm)))

def testMinRunDate(http, date):
    testClass = AbstractGenericWorker(http)
    print(len(testClass.getAllEntitiesRunOnOrAfterADate('campaign', date)))

def testSapNumber(http, searchterm):
    basicCapaignWorker = BasicCampaignWorker()

    testClass = AbstractGenericWorker(http)
    campaigns = testClass.getAllEntitiesBySearchTerm('campaign', searchterm)
    
    for campaign in campaigns:
        print (basicCapaignWorker.extractSapNumber(campaign))

if __name__ == "__main__":
    main()