"""
  Converts a Musicbrainz URI into a dereferencable Zitgist URI

  Yves Raimond, C4DM, Queen Mary, University of London
  yves.raimond@elec.qmul.ac.uk
"""

class MbzURIConverter:
	def __init__(self,mbzuri,zitgisturi='http://dbtune.org/musicbrainz/resource/'):
		self.mbzuri = mbzuri
		self.zitgisturi = zitgisturi
		self.parse()

	def parse(self):
		for i in range(len(self.mbzuri) - 1,0,-1) :
			if self.mbzuri[i] == '/' : 
				self.id = self.mbzuri[i+1:]
				rest = self.mbzuri[:i]
				break
		for j in range(i - 1,0,-1) : 
			if self.mbzuri[j] == '/' :
				self.type = rest[j + 1:]
				break

	def getId(self):
		return self.id
	
	def getType(self):
		return self.type

	def getURI(self):
		return self.zitgisturi + self.type + '/' + self.id
