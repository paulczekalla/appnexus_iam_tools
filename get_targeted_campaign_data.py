import json
import time
import os
from lib.auth import Auth, AuthException
from lib.httpHandler import HttpHandler
from lib.fileWriter2 import FileWriter
from entity.profile import Profile
from worker.generic.AbstractGenericWorker import AbstractGenericWorker
from worker.campaignWorker.BasicCampaignWorker import BasicCampaignWorker

def main():


    FILENAME = "active_campaign_targetings.csv"
    DEFAULT_RESULT_FOLDER = 'results'
    writer_content = list()  

    http = HttpHandler("http://api.appnexus.com")
    a = Auth()
    a.aquireAuthToken(http)
    abstractWorker = AbstractGenericWorker(http)
    basicCapaignWorker = BasicCampaignWorker()

    
    valid_campaigns = getValidCampaigns(http, '2014-05-25+00:00:00')
    #params = {'advertiser_id':str(131480)}
    #params = {'search':'adidas'}
    #valid_campaigns = abstractWorker.getAllEntitiesFiltered('campaign', params)


    line = 'id; name; SAP Number; SAP Position; country; region; city; contextual; soz_dem\n'

    for campaign in valid_campaigns:
        profile = getProfile(http, campaign)

        line += str(campaign['id']) + '; ' + campaign['name'] + '; '

        sap_number = basicCapaignWorker.extractFullSapNumber(campaign)
        line += str(basicCapaignWorker.extractCleanSapNumber(basicCapaignWorker.splitSapNumber(sap_number))) + '; '
        line += str(basicCapaignWorker.extractSapPositionNumber(basicCapaignWorker.splitSapNumber(sap_number))) + '; '

        if profile.country_targets is not None:
            for country in profile.country_targets:
                line += country['name'] + ' '
        line += '; '


        if profile.region_targets is not None:
            for region_targets in profile.region_targets:
                line += region_targets['name'] + ' '
        line += '; '


        if profile.city_targets is not None:
            for city_targets in profile.city_targets:
                line += city_targets['name'] + ' '
        line += '; '


        all_segments = list()
        
        if profile.segment_group_targets is not None:
            for segment_groups in profile.segment_group_targets:
                for segments in segment_groups['segments']:
                    all_segments.append(segments)

        for segment in all_segments:
            if ('Grapeshot' in segment['name']) or ('proximic' in segment['name']):
                line += segment['name'] + ' '
        line += '; '

        for segment in all_segments:
            if 'AS_' in segment['name']:
                line += segment['name'] + ' '

        line += '\n'

    writeIntoFile(line, DEFAULT_RESULT_FOLDER, FILENAME)



def writeIntoFile(lines, DEFAULT_RESULT_FOLDER, FILENAME):
    if not os.path.exists(DEFAULT_RESULT_FOLDER):
        os.mkdir(DEFAULT_RESULT_FOLDER)
    
    with open(DEFAULT_RESULT_FOLDER + '/' + FILENAME, 'w') as fw:    
        fw.write(lines)



def getValidCampaigns(http, date):
    abstractWorker = AbstractGenericWorker(http)
    return abstractWorker.getAllEntitiesRunOnOrAfterADate('campaign', date)


def getProfile(http, campaign):
    abstractWorker = AbstractGenericWorker(http)
    profile = abstractWorker.getProfileFromEntity(campaign)
    return Profile(profile['id'], profile['country_targets'], profile['region_targets'], profile['city_targets'], profile['segment_group_targets'])
    

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