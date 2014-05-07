import os
from datetime import datetime, date, time

class FileWriter:
    def __init__(self, filename, fileRights, folder="new_files_folder"):
        self.baseFilename = filename
        self.fileRights = fileRights
        self._path = folder
        self.fileInstance = self.generateFileInstanceWithNewFile()

    def generateFileInstanceWithNewFile(self):
        filename = self.generateFilename()
        if not os.path.exists(self._path):
            os.mkdir(self._path)
        return open(self._path + '/' + filename, self.fileRights, newline='\n')

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
                exit()

    def writeReportInNewFile(self, fileContent):
        # Preparation
        print("Transforming file")
        fileContent = fileContent.decode('utf-8')

        try:
            self.fileInstance.write(fileContent)
        except:
            print("Error occured while writing into file")
            self.closeFile()
            exit()

    def closeFile(self):
        print("Closing file")
        self.fileInstance.close()
