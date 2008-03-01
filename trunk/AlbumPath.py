import sys
import os, glob, shutil
import logging
import easygui
import path	# has path.path

import config

DEFAULT_ALBUMS_DIR=r"D:\albums"

class AlbumInfo:
	def __init__(self, artist, album, year, genre):
		self.artist = artist
		self.album = album
		self.year = year
		self.genre = genre

def default_chooseBaseTargetDirectory(albumDirectory, albumInfo, config, initialDir):
	return albumDirectory

def graphical_chooseBaseTargetDirectory(albumDirectory, albumInfo, config, initialDir):
	message = "Where do you want to move the album %s by %s?" % (albumInfo.album, albumInfo.artist)
	title = "Choose base target directory"
	return easygui.diropenbox(msg=message, title=message, argInitialDir=initialDir)

class AlbumFilesHandler:
	def __init__(self, albumDirectory, albumInfo, 
			chooseBaseTargetDirectory = default_chooseBaseTargetDirectory):
		self.albumDirectory = albumDirectory
		self.albumInfo = albumInfo
		self.chooseBaseTargetDirectory = chooseBaseTargetDirectory
		
		self.config = config.AlbumFilesConfig()

	def moveFiles(self):
		targetDir = self._searchTargetDir()
		if targetDir:
			initialDir = targetDir
		else:
			initialDir = self.config.defaultTargetPath

		targetDir = self.chooseBaseTargetDirectory(self.albumDirectory, self.albumInfo, self.config, initialDir)
		if targetDir == None or targetDir == "":
			logging.info("No target directory selected, not moving anything")
			return

		targetPath = path.path(targetDir)
		targetPath = targetPath.splitpath()[0]
		
		createdDir = self._createMusicSubdirs(targetPath, self.albumInfo)
		self._moveAllFilesToDir(self.albumDirectory, createdDir)
		return createdDir

	def _createMusicSubdirs(self, baseDir, albumInfo):
		""" Creates directory [./artist/year - album] """
		
		artistDir = os.path.join(baseDir, albumInfo.artist)
		
		# Files will be in directory [artist/year - album]
		filesDir = os.path.join(artistDir, "%s - %s" % (albumInfo.year, albumInfo.album))
		
		logging.info("Creating directories")
		self._createDirIfNotExist(artistDir)
		self._createDirIfNotExist(filesDir)
		
		return filesDir

	def _createDirIfNotExist(self, dirpath):
		""" Create a directory if it doesn't exist """
		if not os.path.isdir(dirpath):
			logging.info("Creating directory: [%s]" % dirpath)
			os.mkdir(dirpath)
		else:
			logging.info("Directory already exists: [%s]" % dirpath)	

	def _moveAllFilesToDir(self, fromDir, targetDir):
		"""Moves all files from fromDir to targetDir."""
		
		oldDir = os.path.realpath(os.curdir)
		os.chdir(fromDir)
		
		logging.info("Moving all files from [%s] to [%s]" % (fromDir, targetDir))
		allInDir = glob.glob("*")
		filesToMove = [file for file in allInDir if not os.path.isdir(file)]
		for file in filesToMove:
			logging.info("Moving [%s]" % file)
			shutil.move(file, targetDir)	
			
		os.chdir(oldDir)

	def _searchTargetDir(self):
		searchPaths = self.config.searchPaths
		
		# Search genre/artist directory
		for searchPathName in self.config.searchPaths:
			searchPath = path.path(searchPathName)
			genrePath = self._findDirInDir(searchPath, self.albumInfo.genre)
			if genrePath:
				artistPath = self._findDirInDir(genrePath, self.albumInfo.artist)
				if artistPath:
					logging.debug("Found artist directory in %s" % artistPath)
					return artistPath
					
		# Search artist directory
		for searchPathName in self.config.searchPaths:
			searchPath = path.path(searchPathName)
			for dir in searchPath.dirs():
				artistPath = self._findDirInDir(dir, self.albumInfo.artist)
				if artistPath:
					logging.debug("Found artist directory in %s" % artistPath)
					return artistPath
					
		return None
		
	def _findDirInDir(self, basePath, dirNameToFind):
		toFind = dirNameToFind.lower()
		
		# Sometimes it is under our nose
		if basePath.splitpath()[1].lower() == toFind:
			return basePath

		dirs = [dir for dir in basePath.dirs() if toFind==dir.splitpath()[1].lower()]
		if len(dirs) >0:
			return dirs[0]
		return None
#
# Tester
#
if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG,
		format='%(asctime)s %(levelname)s %(message)s')
	
	albumInfo = AlbumInfo("John Coltrane", "Ballads", "1962")
	albumPathHandler = AlbumFilesHandler(r"D:\software\wscite175\AAA", albumInfo)
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