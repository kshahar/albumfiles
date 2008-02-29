from distutils.core import setup
import py2exe

#setup(console=['AlbumPathFromFile.py'])
#setup(console=['AlbumPathFromDirectory.py'])
setup(
	console = [
		{ 
			"script" : "AlbumPathMp3tag.py",
			"icon_resources": [(0, "small.ico")]
		}
	]
)