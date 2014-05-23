class AbstractGenericWorker:
	def __init__(self, http):
		self._http = http


	# very ugly hack with the add of the letter s
	# for later versions maybe a dict with every plural version	
	def getEntityPlural(self, type):
		return type+'s'


	def getAllEntitiesByType(self, type):
		firstReturn = self._http.getRequestPage(0, type).json()['response']
		count = firstReturn['count']

		allEntities = list()
		
		type_plural = self.getEntityPlural(type)
		allEntities.extend(firstReturn[type_plural])
		
		print('Getting all ' + str(count) + ' items\n')
		if count > 100:
			for start_element in range(100, count, 100):
				allEntities.extend(self._http.getRequestPage(start_element, type).json()['response'][type_plural])
		
		return allEntities


	# filtering over parameters
	def getAllEntitiesFiltered(self, type, params):
		firstReturn = self._http.getRequest(type, params).json()['response']
		count = firstReturn['count']
		
		allEntities = list()
		
		type_plural = self.getEntityPlural(type)
		allEntities.extend(firstReturn[type_plural])
		
		print('Getting ' + str(count) + ' items\n')
		if count > 100:
			for cur_start_element in range(100, count, 100):
				allEntities.extend(self._http.getRequestPage(cur_start_element, type, params).json()['response'][type_plural])
		
		return allEntities


	def getAllEntitiesByRange(self, type, start_element, stop_element):
		firstReturn = self._http.getRequestPage(start_element, type).json()['response']
		count = firstReturn['count']

		allEntities = list()
		
		type_plural = self.getEntityPlural(type)
		allEntities.extend(firstReturn[type_plural])
		
		print('Getting ' + str(count) + ' items\n')
		if count > 100:
			for cur_start_element in range(start_element+100, stop_element, 100):
				allEntities.extend(self._http.getRequestPage(cur_start_element, type).json()['response'][type_plural])
		
		return allEntities


	def getAllEntitiesBySearchTerm(self, type, searchterm):
		params = {'search':searchterm}
		self.getAllEntitiesFiltered(type, params)


	def getAllEntitiesRunOnOrAfterADate(self, type, first_run_date):
		params = {'min_first_run':first_run_date, 'flight_info':'true'}
		self.getAllEntitiesFiltered(type, params)