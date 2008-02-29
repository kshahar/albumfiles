import sys
import os, glob, shutil
from os import path
import logging
import easygui

DEFAULT_ALBUMS_DIR=r"D:\albums"

class AlbumInfo:
	def __init__(self, artist, album, year):
		self.artist = artist
		self.album = album
		self.year = year

def default_chooseBaseTargetDirectory(albumDirectory, albumInfo):
	return albumDirectory

def graphical_chooseBaseTargetDirectory(albumDirectory, albumInfo):
	message = "Where do you want to move the album %s by %s?" % (albumInfo.album, albumInfo.artist)
	title = "Choose base target directory"
	return easygui.diropenbox(msg=message, title=message, argInitialDir=DEFAULT_ALBUMS_DIR)

class AlbumPathHandler:
	def __init__(self, albumDirectory, albumInfo, 
			chooseBaseTargetDirectory = default_chooseBaseTargetDirectory):
		self.albumDirectory = albumDirectory
		self.albumInfo = albumInfo
		self.chooseBaseTargetDirectory = chooseBaseTargetDirectory

	def moveFiles(self):
		targetDir = self.chooseBaseTargetDirectory(self.albumDirectory, self.albumInfo)
		if targetDir == "":
			logging.info("No target directory selected, not moving anything")
			return
			
		createdDir = self._createMusicSubdirs(targetDir, self.albumInfo)
		self._moveAllFilesToDir(self.albumDirectory, createdDir)
		return createdDir

	def _createMusicSubdirs(self, baseDir, albumInfo):
		""" Creates directory [./artist/year - album] """
		
		artistDir = path.join(baseDir, albumInfo.artist)
		
		# Files will be in directory [artist/year - album]
		filesDir = path.join(artistDir, "%s - %s" % (albumInfo.year, albumInfo.album))
		
		logging.info("Creating directories")
		self._createDirIfNotExist(artistDir)
		self._createDirIfNotExist(filesDir)
		
		return filesDir

	def _createDirIfNotExist(self, dirpath):
		""" Create a directory if it doesn't exist """
		if not path.isdir(dirpath):
			logging.info("Creating directory: [%s]" % dirpath)
			os.mkdir(dirpath)
		else:
			logging.info("Directory already exists: [%s]" % dirpath)	

	def _moveAllFilesToDir(self, fromDir, targetDir):
		"""Moves all files from fromDir to targetDir."""
		
		oldDir = path.realpath(os.curdir)
		os.chdir(fromDir)
		
		logging.info("Moving all files from [%s] to [%s]" % (fromDir, targetDir))
		allInDir = glob.glob("*")
		filesToMove = [file for file in allInDir if not path.isdir(file)]
		for file in filesToMove:
			logging.info("Moving [%s]" % file)
			shutil.move(file, targetDir)	
			
		os.chdir(oldDir)

#
# Tester
#
if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG,
		format='%(asctime)s %(levelname)s %(message)s')
	
	albumInfo = AlbumInfo("John Coltrane", "Ballads", "1962")
	albumPathHandler = AlbumPathHandler(r"D:\software\wscite175\AAA", albumInfo)
	albumPathHandler.moveFiles()

#
# Algorithm
#
""" 
 - Get album directory (AD)
 - Get album info (artist, album, year)
 - Create target directory (TD)
 - Move all files from AD to TD
"""