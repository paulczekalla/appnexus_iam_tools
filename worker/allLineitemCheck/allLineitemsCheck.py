import time
import datetime

class AllLineitemsCheck:
	def __init__(self):
		pass

	def get_all_items(self, allLineItems):
		allLowLineItems = list()
	
		for lineItemArr in allLineItems:
			for lineItem in lineItemArr:
				allLowLineItems.append(lineItem)

		return allLowLineItems
