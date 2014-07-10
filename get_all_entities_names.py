import json
import os
import sys
from lib.auth import Auth, AuthException
from lib.httpHandler import HttpHandler
from worker.generic.AbstractGenericWorker import AbstractGenericWorker

def main():

    http = HttpHandler("http://api.appnexus.com")
    a = Auth()
    a.aquireAuthToken(http)

    #entity_list = ('platform-member', 'advertiser', 'line-item', 'campaign', 'publisher', 'site', 'placement')
    entity_list = ('creative', 'category')

    for entity in entity_list: 
        getEntities(http, entity)


def getEntities(http, entity_type):
    genericWorker = AbstractGenericWorker(http)
    entities = genericWorker.getAllEntitiesByType(entity_type)
    writeIntoFile(entities, entity_type)


def writeIntoFile(entities, entity_type):
    foldername = 'id_mapping'
    filename = 'mapping_' + entity_type + '.csv'
    
    if not os.path.exists(foldername):
        os.mkdir(foldername)
    
    with open(foldername + '/' + filename, 'w', encoding='utf-8') as fw:    
        fw.write('id; name\n')

        for entity in entities:
            id = str(entity['id'])
            name = entity['name']
            fw.write(id + '; ' + name + '\n')


if __name__ == "__main__":
    main()