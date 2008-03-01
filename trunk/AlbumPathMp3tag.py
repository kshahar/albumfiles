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
	genre = details[4]
	
	albumInfo = AlbumPath.AlbumInfo(artist, album, year, genre)
	handler = AlbumPath.AlbumFilesHandler(albumPath, albumInfo,
		AlbumPath.graphical_chooseBaseTargetDirectory)
	createdDir = handler.moveFiles()
	
	if not createdDir:
		return	
	normpath = os.path.normpath(createdDir)
	os.system("explorer " + normpath)

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG,
		format='%(asctime)s %(levelname)s %(message)s')	
	
	# For testing
	#sys.argv = ["a", r"D:\albums\ZZZ  2005 - My Rocky Mountain" + "#Shpongle#Balldas#1962#Funk"]
	
	if len(sys.argv) > 1:
		detailsStr = " ".join(sys.argv[1:])
		main(detailsStr)
	else:
		print "Usage: AlbumPathMp3tag AlbumPath#Artist#Album#Year#Genre"
		print "Example: AlbumPathMp3tag D:\\Album Downloaded\\From Internet#John Coltrane#Ballads#1962#Jazz"
	#else:
	#	detailsStr = "D:\\software\\wscite175\\AAA#John Coltrane#Ballads#1962"
	#	main(detailsStr)
		
	os.system("pause")