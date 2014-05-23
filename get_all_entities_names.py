import json
import os
from lib.auth import Auth, AuthException
from lib.httpHandler import HttpHandler
from worker.generic.AbstractGenericWorker import AbstractGenericWorker

def main():

    http = HttpHandler("http://api.appnexus.com")
    a = Auth()
    a.aquireAuthToken(http)

    #entity_list = ('platform-member', 'advertiser', 'line-item', 'campaign', 'publisher', 'site', 'placement')
    entity_list = ('advertiser', 'publisher')

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
    
    with open(foldername + '/' + filename, 'w') as fw:    
        fw.write('id; name\n')

        for entity in entities:
            fw.write(str(entity['id']) + '; ' + entity['name'] + '\n')


if __name__ == "__main__":
    main()