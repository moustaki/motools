from mutagen.id3 import ID3, UFID

class Id3Writer :
	
	def __init__(self,file) :
		self.id3 = ID3(file)
		
	def writeUri(self,uri) :
		self.id3.add(UFID(owner="http://zitgist.com/music/",data=uri))
		self.id3.save()
