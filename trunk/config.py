import os, logging
from xml.etree import ElementTree
from os import path

class AlbumFilesConfig:
	def __init__(self, fileFullPath="", fileName="AlbumFiles.xml"):
		self._homeDir = os.environ["USERPROFILE"]
		self._fileInHomeDir = path.join(self._homeDir, fileName)
		
		foundFileName = self._findConfigFile(fileFullPath, fileName)
		if foundFileName == "":
			self._createConfigFile()
			foundFileName = self._fileInHomeDir
		
		self._parseConfigFile(foundFileName)
		
	def _findConfigFile(self, fileFullPath, fileName):
		if fileFullPath == "":
			if path.exists(fileName):
				logging.info("Using config file %s from current directory" % fileName)
				return fileName
			
			if path.exists(self._fileInHomeDir):
				logging.info("Using config file %s from %s" % (fileName, self._homeDir))
				return self._fileInHomeDir
			
			logging.debug("No config file with name %s was found in current directory or in %s" % (fileName,self._homeDir))
			return ""
		else:
			if path.splitext(fileFullPath)[1] != ".xml":
				raise Exception, "Must be an xml file"
			
			logging.info("Using config file %s" % fileFullPath)
			return fileFullPath
	
	# Assumes filename is a valid xml file name
	def _parseConfigFile(self, filename):			
		tree = ElementTree.parse(filename)
		node = tree.find("DefaultTargetPath/Path")
		self.defaultTargetPath = node.attrib["value"]
		
		nodes = tree.findall("SearchPaths/Path")
		self.searchPaths = [node.attrib["value"] for node in nodes]
	
	def _createConfigFile(self):
		logging.info("Creating config file in %s", self._homeDir)
		defaultFile = """<?xml version="1.0"?>
<AlbumFiles>
	<DefaultTargetPath>
		<Path value=\"D:/albums\" />
	</DefaultTargetPath>
	<SearchPaths>
		<Path value=\"D:/albums\" />
	</SearchPaths>
</AlbumFiles>
"""
		f = open(self._fileInHomeDir, 'w')
		f.write(defaultFile)
	
if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG,
		format='%(asctime)s %(levelname)s %(message)s')
	
	config = AlbumFilesConfig()
	print config.defaultTargetPath, config.searchPaths

	#tree.findall("SearchPaths/Path")
	#childrens = root.getchildren()
	#for child in childrens: print child