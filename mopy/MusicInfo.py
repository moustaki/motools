"""
MusicInfo.py

Holds a collection of Music Ontology objects

Created by Chris Sutton on 2007-08-13.
Copyright (c) 2007 Chris Sutton. All rights reserved.
"""

import model

class MusicInfoException(Exception):
	def __init__(self, message) :
		self.message = message
	def __str__(self) :
		return self.message

class MusicInfo(object):
	def __init__(self, objects, namespaceBindings = model.namespaceBindings):
		self.MainIdx = {}
		for obj in objects:
			self.__addObject(obj)
		self.namespaceBindings = namespaceBindings

	def __addObject(self, obj, URI=None):
		if URI == None:
			if hasattr(obj, "URI") == False:
				raise MusicInfoException("Tried to add object "+str(obj)+" with no URI !")
			else:
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