import time
import datetime

class NeverRunCampaign:
	def __init__(self):
		pass

	def check_if_opt_campaign_never_run(self, allcampaigns):
		deletedCampaigns = list()
	
		for campaignArr in allcampaigns:
			for campaign in campaignArr:
				if campaign['name'].startswith('O_') and campaign['stats'] is None:
					if campaign['start_date'] is not None:
						date = campaign['start_date'].split(" ")[0].split("-")
						if int(date[0]) == 2012 or int(date[1]) < 9:
							deletedCampaigns.append(campaign)
		return deletedCampaigns
