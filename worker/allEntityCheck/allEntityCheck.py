import time
import datetime

class AllEntityCheck:
	def __init__(self):
		print("All Entity Check instance created")

	def get_all_items(self, allEntities):
		all_entities_as_list = list()
	
		for entitieList in allEntities:
			for entity in entitieList:
				all_entities_as_list.append(entity)

		return all_entities_as_list
