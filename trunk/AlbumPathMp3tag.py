import sys
import os
import logging
import AlbumPath

def main(detailsStr):
	details = detailsStr.split("#")
	albumPath = details[0]
	artist = details[1]
	album = details[2]
	year = details[3]
	
	albumInfo = AlbumPath.AlbumInfo(artist, album, year)
	handler = AlbumPath.AlbumPathHandler(albumPath, albumInfo,
		AlbumPath.graphical_chooseBaseTargetDirectory)
	createdDir = handler.moveFiles()
	
	normpath = os.path.normpath(createdDir)
	os.system("explorer " + normpath)

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG,
		format='%(asctime)s %(levelname)s %(message)s')	
	
	if len(sys.argv) > 1:
		detailsStr = " ".join(sys.argv[1:])
		main(detailsStr)
	else:
		print "Usage: AlbumPathMp3tag AlbumPath#Artist#Album#Year"
		print "Example: AlbumPathMp3tag D:\\Album Downloaded\\From Internet#John Coltrane#Ballads#1962"
	#else:
	#	detailsStr = "D:\\software\\wscite175\\AAA#John Coltrane#Ballads#1962"
	#	main(detailsStr)
		
	os.system("pause")