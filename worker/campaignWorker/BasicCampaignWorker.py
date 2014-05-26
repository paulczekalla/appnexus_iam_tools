class BasicCampaignWorker:
	def __init__(self):
		print("All Entity Check instance created")

	# With SAP Positionnumber
	def extractFullSapNumber(self, campaign):
		campaign_name = campaign['name']
		
		# SAP Number should be last element, seperated by space
		sap_number = campaign_name.split(' ')[-1]

		return sap_number

	def splitSapNumber(self, sap_number):
		sap_number_splited = list(sap_number)
		return sap_number_splited

	# 'Real' SAP Number
	def extractCleanSapNumber(self, full_splited_sap_number):
		splited_sap_number = full_splited_sap_number[0:-3]
		return ''.join(splited_sap_number)

	# SAP Position Number - last three digits
	def extractSapPositionNumber(self, full_splited_sap_number):
		splited_sap_position_number = full_splited_sap_number[-3:len(full_splited_sap_number)]
		return ''.join(splited_sap_position_number)