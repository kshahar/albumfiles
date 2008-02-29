import sys
import os
import logging
from CreateMusicDirectories import *

def main(filePath):
	logging.basicConfig(level=logging.DEBUG,
		format='%(asctime)s %(levelname)s %(message)s')
		#filename=path.join('/myapp.log'),
		#filemode='w')

	logging.info("Using File [%s]" % filePath)
	
	try:
		moveToSubdirsFromFile(filePath)
		os.system("pause")
	except MusicDirectoriesError, message:
		exceptionPrint("Cannot create subdirs: " + str(message))
	except id3reader.Id3Error, message:
		exceptionPrint("id3reader error: " + str(message))
	except Exception, message:
		exceptionPrint("General error: " + str(message))
	
if __name__ == "__main__":
	if len(sys.argv) > 1:
		filePath = " ".join(sys.argv[1:])
		main(filePath)