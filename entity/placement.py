class Placement:
    def __init__(self, id, name, code, publisher_name, site_name, default_referrer_url, custom_categories):
        self.id = id
        self.name = name
        self.code = code
        self.publisher_name = publisher_name
        self.site_name = site_name
        self.default_referrer_url = default_referrer_url
        self.custom_categories = custom_categories

    def getAllEntitiesByType(self, type):
        firstReturn = self.http.getRequestPage(0, type).json()['response']
        count = firstReturn['count']

        allEntities = list()
        # very ugly hack with the add of the letter s
        # for later versions maybe a dict with every plural version
        allEntities.extend(firstReturn[type+'s'])
        
        print('Getting all ' + str(count) + ' items\n')
        if count > 100:
            for start_element in range(100, count, 100):
                # again this plural s implementation 
                allEntities.extend(self.http.getRequestPage(start_element, type).json()['response'][type+'s'])
        
        return allEntities