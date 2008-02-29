import sys
import os
import logging
from CreateMusicDirectories import *

#		
# Cosole application functions:
#
		
def getClipboardText(): 
	import win32clipboard as w 
	import win32con
	w.OpenClipboard() 
	d=w.GetClipboardData(win32con.CF_TEXT) 
	w.CloseClipboard() 
	return d 
		
def main(dir = ""):
	logging.basicConfig(level=logging.DEBUG,
		format='%(asctime)s %(levelname)s %(message)s')
		#filename=path.join('/myapp.log'),
		#filemode='w')

	if dir == "" :
		dir = raw_input("Enter directory, or Hit <Enter> to read from clipboard > ")
		if dir == "" :
			dir = getClipboardText()
			
	logging.info("Using directory [%s]" % dir)
	
	try:
		moveToSubdirsFromDir(dir)
		os.system("pause")
	except MusicDirectoriesError, message:
		exceptionPrint("Cannot create subdirs: " + str(message))
	except id3reader.Id3Error, message:
		exceptionPrint("id3reader error: " + str(message))
	except Exception, message:
		exceptionPrint("General error: " + str(message))
	
if __name__ == "__main__":
	if len(sys.argv) > 1:
		dirPath = " ".join(sys.argv[1:])
		main(dirPath)
	else:
		main()