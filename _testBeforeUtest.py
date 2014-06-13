import json
import time
import copy
from random import shuffle
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
    countAllValidEntities(http, 'placement', 'mobil')
    #testSearch(http, 'adidas')
    #testMinRunDate(http, '2014-05-01+00:00:00')
    #testSapNumber(http, 'adidas')
    #testGetProfile(http, 'adidas')
    #testGetSpecificRegioTarget(http, 3961329)

# not real tests, just preparation

def countAllValidEntities(http, entity, invalid_value):
    testClass = AbstractGenericWorker(http)
    allEntities = testClass.getAllEntitiesByRange(entity, 6000, 6199)
    #allEntities = testClass.getAllEntitiesByType(entity)
    
    count = 0
    all_placements = list()
    
    placements = list()
    for entity in allEntities:    
        if invalid_value not in entity['publisher_name']:
            placements.append({'id':entity['id']})
            count = count + 1
            if count == 100:
                all_placements.append(copy.deepcopy(placements))
                placements = list()
                count = 0
    
    shuffle(all_placements)
    
    count = 1
    for places in all_placements:
        construct_deal(http, places, count)
        count = count + 1
        print('######')

def construct_deal(http, placement_ids, number):
    
    print(placement_ids)
    params_profile = {'profile':{'placement_targets':placement_ids}}
    
    response = http.postRequest(params_profile, 'profile').json()['response']
    print(response)
    profile = response['profile']

    print(profile['id'])
    #params = {'deal':{'name':'PerformaceAdvertising - Transparency Deal '+str(number), 'active':'true', 'floor_price':'1.0', 'currency':'EUR', 'buyer':{'id':'1200'}, 'type':{'id':'1'}}}
    
    # xp td
    params = {'deal':{'name':'PerformanceAdvertising - Transparency Deal '+str(number), 'active':'true', 'start_date':'2014-06-13 00:00:00', 'floor_price':'1.0', 'use_deal_floor':'true', 'currency':'EUR', 'buyer':{'id':'2150'}, 'type':{'id':'1'}, 'profile_id':profile['id']}}
    print(params)
    response = http.postRequest(params, 'deal').json()['response']
    print(response)
    deal = response['deal']
    print(deal['id'])

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


def testGetSpecificRegioTarget(http, campaign_id):
    params = {'id':str(campaign_id)}
    campaign = http.getRequest('campaign', params).json()['response']['campaign']
        
    testClass = AbstractGenericWorker(http)
    profile = testClass.getProfileFromEntity(campaign)

    camp_profile = Profile(profile['id'], profile['country_targets'], profile['region_targets'], profile['city_targets'], profile['segment_group_targets'])
    for city in camp_profile.city_targets:
        print(city['name'])
    

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