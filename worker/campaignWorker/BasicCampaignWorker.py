class BasicCampaignWorker:
	def __init__(self):
		print("All Entity Check instance created")

	def extractSapNumber(self, campaign):
		campaign_name = campaign['name']
		
		# SAP Number should be last element, seperated by space
		sap_number = campaign_name.split(' ')[-1]

		return sap_number
