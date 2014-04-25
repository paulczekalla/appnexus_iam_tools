import time
import datetime

class LowRunning:
	def __init__(self):
		pass

	def check_low_running_items(self, allLineItems):
		allLowLineItems = list()
	
		for lineItemArr in allLineItems:
			for lineItem in lineItemArr:
				if lineItem['lifetime_budget'] is not None and lineItem['all_stats'] is not None:
					if float(lineItem['lifetime_budget']) > float(lineItem['all_stats']['lifetime']['revenue'])*2.0:
						if '7day' in lineItem['all_stats'] and int(lineItem['all_stats']['7day']['imps']) < 7000:
							allLowLineItems.append(lineItem)
						elif 'yesterday' in lineItem['all_stats'] and int(lineItem['all_stats']['yesterday']['imps']) < 1000:
							allLowLineItems.append(lineItem)

		return allLowLineItems

	def check_never_running_items(self, allLineItems):
		date_now = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d').split('-')

		current_year = int(date_now[0])
		current_month = int(date_now[1])

		if current_month in range(2,12):
			last_month = current_month - 1
			next_month = current_month + 1
		elif current_month == 1:
			last_month = 12
			next_month = 2
		elif current_month == 12:
			last_month = 11
			next_month = 1

		allNeverRunLineItems = list()

		for lineItemArr in allLineItems:
			for lineItem in lineItemArr:
				start_year = int(lineItem['start_date'].split(" ")[0].split("-")[0])
				start_date_month = int(lineItem['start_date'].split(" ")[0].split("-")[1])
				if lineItem['end_date'] is not None:
					end_date_month = int(lineItem['end_date'].split(" ")[0].split("-")[1])
				else:
					end_date_month = last_month + 1
				
				if lineItem['state'] != 'inactive' and (start_year == current_year or start_year == current_year-1) and (start_date_month <= current_month or start_date_month <= last_month) and (end_date_month >= current_month or end_date_month >= next_month):
					allNeverRunLineItems.append(lineItem)
						
				else:
					#print("not valid")
					pass

		return allNeverRunLineItems
