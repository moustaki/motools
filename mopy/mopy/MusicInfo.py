"""
MusicInfo.py

Holds a collection of Music Ontology objects

Created by Chris Sutton on 2007-08-13.
Copyright (c) 2007 Chris Sutton. All rights reserved.
"""

from logging import log, error, warning, info, debug
from mopy import model
import random

class MusicInfoException(Exception):
	def __init__(self, message) :
		self.message = message
	def __str__(self) :
		return self.message

class MusicInfo(object):
	def __init__(self, objects=None, namespaceBindings = model.namespaceBindings):
		if objects==None:
			objects = []
		self.MainIdx = {}
		for obj in objects:
			self.add(obj)
		self.namespaceBindings = namespaceBindings

	def add(self, obj, URI=None):
		if URI == None:
			# See if we have an existing blind node object :
			if hasattr(obj, "URI") == False or obj.URI == None or isBlind(obj):
				#raise MusicInfoException("Tried to add object "+str(obj)+" with no URI !")
				info("Tried to add object "+str(obj).replace("\n","|")+" with no URI or blind URI !")
				if self.findExistingBlindObj(obj) == None:
					if not isBlind(obj):
						info(" Assigning a blind URI.")
						obj.URI = getBlindURI()
				else:
					info("Already know this blind obj.")
					return
					
			URI = obj.URI

		if not self.haveURI(URI):
			# Add object :
			self.MainIdx[URI] = obj
			if not hasattr(obj, "shortname"):
				raise MusicInfoException("No shortname property for object " + str(obj) + ", did it come from the MO model ?")
			if not hasattr(self, obj.shortname+"Idx"):
				setattr(self, obj.shortname+"Idx", {})
			getattr(self, obj.shortname+"Idx")[URI] = obj
		else:
			raise MusicInfoException("Tried to add two objects for the same URI ! "+str(URI))
			# TODO : Actually handle this, merging with existing objects & interlinking as appropriate
	
	def haveURI(self, uri):
		return self.MainIdx.has_key(uri)
		
	def findExistingBlindObj(self, o):
		if not hasattr(o, "shortname"):
			raise MusicInfoException("No shortname property for object " + str(o) + ", did it come from the MO model ?")
		if not hasattr(self, o.shortname+"Idx"):
			return None
			
		idx = getattr(self, o.shortname+"Idx")
		for obj in idx.values():
			if obj.URI.startswith("blind:"):
				# test properties
				match = True
				try:
					for propName in obj._props.keys():
						if obj._props[propName] != o._props[propName]:
							#print("Disregarding "+str(obj).replace("\n","|")+" due to property "+propName+" differing.\n")
							match = False
				except:
					match = False
					
				if match == True:
					print("Found object "+str(obj)+" to match "+str(o)+"\n")
					return obj
					
		return None
		
def isBlind(obj):
	return hasattr(obj,"URI") and obj.URI != None and obj.URI.startswith("blind:")

def getBlindURI(s=None):
	if s==None:
		s=str(hex(random.getrandbits(64))[2:-1])
	return "blind:"+s