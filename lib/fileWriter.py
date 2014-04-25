import os
from datetime import datetime, date, time

class FileWriter:
	def __init__(self, filename, fileRights):
		self.baseFilename = filename
		self.fileRights = fileRights
		self.fileInstance = self.generateFileInstanceWithNewFile()
	
	def generateFileInstanceWithNewFile(self):
		filename = self.generateFilename()
		return open(filename, self.fileRights)

	def generateFilename(self):
		time_now = datetime.now()
		ts_date = str(time_now.year) + str(time_now.month) + str(time_now.day)
		ts_time = str(time_now.hour) + str(time_now.minute) + str(time_now.second)
		return self.baseFilename.split('.')[0] + '_' + ts_date + '_' + ts_time + '.' + self.baseFilename.split('.')[1]
	
	def writeInNewFile(self, fileContent):
		for line in fileContent:
			try:
				self.fileInstance.write(line)
			except:
				print("Error occured while writing into file")
				self.closeFile()
		
	def closeFile(self):
		self.fileInstance.close()
