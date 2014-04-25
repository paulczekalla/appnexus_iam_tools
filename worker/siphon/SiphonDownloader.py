import os
import time

class SiphonDownloader:
	
	def __init__(self, path, http):
		self._path = path
		self._http = http
		self._service = "siphon-download"


	def download_file(self, params):
		feed_data_file = self._http.getRequest(self._service, params)
		if self.check_file_downloadable(feed_data_file.headers):
			self.save_file_to_folder(feed_data_file)
		else:
			print("Trying again in 15 seconds")
			time.sleep(15)
			self.download_file(params)

	def check_file_downloadable(self, header):
		if "content-disposition" not in header:
			print("File not ready yet.")
			return False
		
		return True

	def generate_filename(self, header):
		# Header is a dict with a content-disposition, where the filename sits.. 
		filename_value = header["content-disposition"]
		
		# filename=read_filename
		return filename_value.split("=")[1]
		

	def save_file_to_folder(self, feed_data_file):
		if not os.path.exists(self._path):
			os.mkdir(self._path)

		new_file = open(self._path + "/" + self.generate_filename(feed_data_file.headers), "wb").write(feed_data_file.content)
		# file close