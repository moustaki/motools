import os

import mopy
from mopy.RDFInterface import exportRDFFile
from mopy.MusicInfo import MusicInfo
import logging
from logging import log, error, warning, info, debug


class RdfFile(object):
	
	def __init__(self):
		self.mi=None
		self.f=None
	
	def open(self, filename):
		if not os.path.exists(filename):
			try:
				self.f = open(filename,"w")
				self.filename = filename
				self.mi = MusicInfo()
				return True
			except Exception, e:
				error("Couldn't open file for writing : "+filename+"\nException info : "+str(e))
		return False
	
	def addMusicInfo(self, mi):
		for o in mi.MainIdx.values():
			if o != None:
				self.mi.add(o)
	
	def write(self):
		self.f.close()
		self.f = open(self.filename, 'r')
		fileEmpty = len(self.f.readlines()) == 0
		self.f.close()
		if fileEmpty and len(self.mi.MainIdx) == 0:
			# Don't leave empty files around :
			os.remove(self.filename)
		else:
			exportRDFFile(self.mi, self.filename, format="xml")
				
	def clear(self):
		self.mi = None
		if self.f != None:
			self.f.close()
		self.filename = None
		
		
