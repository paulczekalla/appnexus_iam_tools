import os
from datetime import datetime, date, time

class FileWriter:
    def __init__(self, filename, fileRights, default_folder = None):
        self._baseFilename = filename
        self._fileRights = fileRights
        self._default_folder = default_folder
        self._fileInstance = self.generatefileInstanceWithNewFile()
    
    def generatefileInstanceWithNewFile(self):
        filename = self.generateFilename()
        if self._default_folder is not None:
            return open(self._default_folder + '/' + filename, self._fileRights)
        else:
            return open(filename, self._fileRights)

    def generateFilename(self):
        time_now = datetime.now()
        ts_date = str(time_now.year) + str(time_now.month) + str(time_now.day)
        ts_time = str(time_now.hour) + str(time_now.minute) + str(time_now.second)
        return self._baseFilename.split('.')[0] + '_' + ts_date + '_' + ts_time + '.' + self._baseFilename.split('.')[1]
    
    def writeInNewFile(self, fileContent):
        for line in fileContent:
            try:
                self._fileInstance.write(line)
            except:
                print("Error occured while writing into file")
                self.closeFile()
        
    def closeFile(self):
        self._fileInstance.close()
