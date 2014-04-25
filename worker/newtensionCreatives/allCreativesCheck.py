class AllCreativesCheck:
	def __init__(self):
		pass

	def get_all_items(self, allCreatives):
		allItems = list()
	
		for itemArr in allCreatives:
			for creative in itemArr:
				allItems.append(creative)

		return allItems
