import json
import time
from lib.auth import Auth, AuthException
from lib.httpHandler import HttpHandler
from lib.fileWriter2 import FileWriter
from entity.profile import Profile
from worker.generic.AbstractGenericWorker import AbstractGenericWorker
from worker.campaignWorker.BasicCampaignWorker import BasicCampaignWorker

def main():

    http = HttpHandler("http://api.appnexus.com")
    a = Auth()
    a.aquireAuthToken(http)

    #testSearch(http, 'adidas')
    #testMinRunDate(http, '2014-05-01+00:00:00')
    #testSapNumber(http, 'adidas')
    testGetProfile(http, 'adidas')

# not real tests, just preparation
def testSearch(http, searchterm):
    testClass = AbstractGenericWorker(http)
    print('Campaigns fetched: ' + str(len(testClass.getAllEntitiesBySearchTerm('campaign', searchterm))))


def testMinRunDate(http, date):
    testClass = AbstractGenericWorker(http)
    print('Campaigns fetched: ' + str(len(testClass.getAllEntitiesRunOnOrAfterADate('campaign', date))))


def testGetProfile(http, searchterm):
    testClass = AbstractGenericWorker(http)
    campaigns = testClass.getAllEntitiesBySearchTerm('campaign', searchterm)

    profiles = list()
    for campaign in campaigns:
        profile = testClass.getProfileFromEntity(campaign)

        profiles.append(Profile(profile['id'], profile['country_targets'], profile['region_targets'], profile['city_targets'], profile['segment_group_targets']))

    for profile in profiles:
        print(profile.profile_id)
        print(profile.country_targets)


def testSapNumber(http, searchterm):
    basicCapaignWorker = BasicCampaignWorker()
    testClass = AbstractGenericWorker(http)
    
    campaigns = testClass.getAllEntitiesBySearchTerm('campaign', searchterm)
    
    for campaign in campaigns:
        sap_number = basicCapaignWorker.extractFullSapNumber(campaign)
        print('Full SAP Number: ' + str(sap_number))
        print('Real SAP Number: ' + str(basicCapaignWorker.extractCleanSapNumber(basicCapaignWorker.splitSapNumber(sap_number))))
        print('SAP Position Number: ' + str(basicCapaignWorker.extractSapPositionNumber(basicCapaignWorker.splitSapNumber(sap_number))))

if __name__ == "__main__":
    main()