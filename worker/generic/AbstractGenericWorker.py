class AbstractGenericWorker:
	def __init__(self, http):
		self.http = http

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

	def getAllEntitiesByRange(self, type, start_element, stop_element):
		firstReturn = self.http.getRequestPage(start_element, type).json()['response']
		count = firstReturn['count']

		allEntities = list()
		# very ugly hack with the add of the letter s
		# for later versions maybe a dict with every plural version
		allEntities.extend(firstReturn[type+'s'])
		
		if count > 100:
			for cur_start_element in range(start_element+100, stop_element, 100):
				# again this plural s implementation 
				allEntities.extend(self.http.getRequestPage(cur_start_element, type).json()['response'][type+'s'])
		
		return allEntities

	def getAllEntitiesBySearchTerm(self, type, searchterm):
		pass