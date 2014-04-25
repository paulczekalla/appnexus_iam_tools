import json
import time
from lib.auth import Auth, AuthException
from lib.httpHandler import HttpHandler
from lib.fileWriter import FileWriter
from worker.generic.AbstractGenericWorker import AbstractGenericWorker
from worker.placements.PlacementCategoriesChecker import PlacementCategoriesChecker
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

DEFAULT_RESULT_FOLDER = 'results'
filename = "all_site_ALL_categories.csv"

http = HttpHandler("http://api.appnexus.com")

a = Auth()

aquireAuthToken(a, http)

worker = AbstractGenericWorker(http)
sites = worker.getAllEntitiesByType('site')
#sites = worker.getAllEntitiesByRange('site', 0, 100)

writer_content = list()

count = len(sites)
i = 1

all_categories = set()
all_placement = list()

defect_sites = list()
defect_placement = list()


placement_cat_checker = PlacementCategoriesChecker()

for site in sites:
    print(str(i) + ' / ' + str(count))

    print('Working on site:' + site['name'])

    site_categories = list()
    
    if site['content_categories'] is not None:
        for category in site['content_categories']:
            site_categories.append(category['name'])
            all_categories.add(category['name'])
            
    else:
        print("No Custom Categories")        
   
    if site['placements'] is not None:
        for placement_site in site['placements']:
            placement_full = getPlacement(placement_site['id'])
            
            if placement_full is not None:
                all_placement.append(placement_cat_checker.read_in_categories(placement_full, site_categories, all_categories))
            else:
                # trying to throttle
                time.sleep(30)
                
                # if same thing happens again, than we have to look deeper
                placement_full = getPlacement(placement_site['id'])
                if placement_full is not None:
                    all_placement.append(placement_cat_checker.read_in_categories(placement_full, site_categories, all_categories))
                else:
                    defect_placement.append(placement_site['id'])
    else:
        defect_sites.append(site['name'])
    
    i+=1

writer_string = 'placement_id; placement_name; placement_code; publisher_name; site_name; default_referrer_url; ' 
for cat in all_categories:
    writer_string += cat + '; ' 

writer_string += '\n'
writer_content.append(writer_string)

for placement in all_placement:
    writer_string = str(placement.id) + '; ' + placement.name + '; '
    if placement.code is not None:
        writer_string += str(placement.code)
    writer_string += '; ' + placement.publisher_name + '; ' + placement.site_name + '; '
    
    if placement.default_referrer_url is not None:
        writer_string += placement.default_referrer_url
    
    writer_string += '; '
    
    for cat in all_categories:
        if cat in placement.custom_categories:
            writer_string += 'JA ;'
        else:
            writer_string += 'NEIN ;'
    writer_string += '\n'
    writer_content.append(writer_string)



fw = FileWriter(filename, 'w', DEFAULT_RESULT_FOLDER)

for line in writer_content:
    fw.writeInNewFile(line)

fw.closeFile()

print('Defect Sites: ')
print(defect_sites)

print('Defect Placements: ')
print(defect_placement)