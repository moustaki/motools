"""
PropertySet.py

Created by Chris Sutton on 2007-08-11.
Copyright (c) 2007 Chris Sutton. All rights reserved.
"""

class PropertySet(set):

	def __init__(self, propertyURI, validTypes, allowLits):
#		self.s = set()
		set.__init__(self)
		self.propertyURI = propertyURI
		self.validTypes = validTypes
		self.allowLits = allowLits
		self.Lits = (str, int, list, float) # Any more ?
	#
	# Set functions :
	#	
	def add(self, o):
		# type check :
		print "type checking against : "+str(self.validTypes)
		if self.allowLits:
			print "(lits allowed)"
		if not ((self.allowLits and isinstance(o, self.Lits))\
				or isinstance(o, self.validTypes)\
				):
			raise TypeError("Invalid type ! Expected one of : "+str(self.validTypes))
		set.add(self,o)
	
	def get(self):
		print "in custom get()"
		return self

	def set(self, v):
		self.clear()
		self.add(v)

def protector(self, item, value):
	if (not self.__dict__.has_key("_initialised"))\
		   or self._initialised == False \
	       or hasattr(self,item):
		object.__setattr__(self,item,value)
	else:
		raise AttributeError("Not allowed add new attributes to classes ! Typo ?")
