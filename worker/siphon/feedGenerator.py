import json

class FeedGenerator:

	def __init__(self, http = None, feedTypes = ("standard_feed", "bid_landscape_feed","segment_feed", "custom_data_feed")):
		self.http = http
		self.service = 'siphon'
		self.feedTypes = feedTypes
		self.ready_for_download = ("new", "pending", "in_progress", "completed")

	def getFeeds(self):
		allDataFeeds = self.http.getRequest(self.service).json()['response']['siphons']

		return allDataFeeds

	def getFeedTypes(self):
		return self.feedTypes

	def generateLocationRequests(self, datafeeds):
		siphon_downloadlinks = list()
		for feed in datafeeds:
			for split_part in feed["splits"]:
				if feed["name"] in self.getFeedTypes():
					params = {"siphon_name":feed["name"],"hour":feed["hour"], "timestamp":feed["timestamp"], "split_part":split_part["part"]}
					if split_part["status"] in self.ready_for_download:
						siphon_downloadlinks.append(params)
					#download_link = self.http.getRequest("siphon-download", params)
					#print(download_link.headers)

		return siphon_downloadlinks
