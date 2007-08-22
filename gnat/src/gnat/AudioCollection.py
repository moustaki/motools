#!/usr/bin/python2.4
#
# Abstraction of an audio collection, living in a top-directory
#

import os
import os.path
import logging
import re
import mopy

from time import asctime
from MbzURIConverter import *
from MbzTrackLookup import *
from FPTrackLookup import FPTrackLookup
from RdfFile import RdfFile
from ExternalSources import *
from Id3Writer import *
from logging import log, error, warning, info, debug
from optparse import OptionParser
from urllib import quote as urlencode

from mopy.MusicInfo import MusicInfo, isBlind
from mopy.model import Stream, Track

exclPatterns = r".*(jpg|jpeg|txt|ini|db|DS\_Store|m3u|pls|xml|log|png|\.directory)$"
excludeRE = re.compile(exclPatterns, re.IGNORECASE)


class AudioCollection :

	def __init__(self) :
		self.rdf = RdfFile()
		self.processed = 0
		self.succeeded = 0
		
	def walk(self, commandName, filepath):
		if os.path.isdir(filepath):
			dcount=0; fcount=0
			for root,dirs,files in os.walk(filepath) :
				info("Considering "+root)
				dcount+=1
				if self.rdf.open(os.path.join(root,"info_"+commandName+".rdf")):
					for name in files :
						filename = os.path.join(root,name)
						if (re.match(excludeRE, name) == None):
							mi = getattr(self, commandName)(filename)
							self.rdf.addMusicInfo(mi)
							fcount+=1
					self.rdf.write()
					self.rdf.clear()
					
			info("Succeeded for %d/%d files across %d directories.", self.succeeded, fcount, dcount)
		else:
			error("Filepath given is not a directory ! "+filepath)

	def clean(self, filepath):
		if os.path.isdir(filepath):
			dcount=0; fcount=0
			for root,dirs,files in os.walk(filepath) :
				dcount+=1
				for f in files:
					if f.find("info_") != -1 and f.find(".rdf") != -1:
						os.remove(os.path.join(root,f))
						fcount+=1
			info("Removed %d files across %d directories.", fcount, dcount)
		elif os.path.exists(filepath) and filepath.find("info_") != -1 and filepath.find(".rdf") != -1:
			os.remove(filepath)
		else:
			error("Filepath given is not a directory or an rdf file ! "+filepath)		
	
	def metadata(self, filename) :
		debug("Considering "+filename)
		mi = MusicInfo()
		try :
			lookup = MbzTrackLookup(filename)
			mbzuri = lookup.getMbzTrackURI()
			mbzconvert = MbzURIConverter(mbzuri)
			sig = Stream(urlencode(os.path.basename(filename)))
			mbz = Track(mbzconvert.getURI())
			mbz.available_as = sig
			mi.add(sig); mi.add(mbz)
			self.succeeded+=1
		except MbzLookupException, e:
			error(" - " + e.message)
		except FileTypeException, e:
			error(" - " + e.message)
		return mi

	def fingerprint(self, filename) :
		lookup = FPTrackLookup()
		debug("Considering "+filename)
		mi = lookup.fpFile(filename)
		if hasattr(mi, "TrackIdx") and len(mi.TrackIdx) > 0:
			if not isBlind(mi.TrackIdx.values()[0]):
				self.succeeded+=1
		return mi


	# def crawl(self,path) :
	# 	 for itemURIstr in self.rdf.getItemURIs(contextName=None) :
	# 	 	filename = self.rdf.URItoFilename(itemURIstr)
	# 		debug("Considering "+filename)
	# 		manifURIs = self.rdf.availableAs(itemURIstr,contextName=None)
	# 		for manifURI in manifURIs :
	# 			#try :
	# 			debug("Loading "+manifURI)
	# 			self.rdf.load(manifURI) 
	# 			self.rdf.commit()
	# 			debug("Crawling from "+manifURI)
	# 			self.rdf.crawl(manifURI,path)
	# 			self.rdf.commit()
	# 			#except Exception, e:
	# 			#	error(" - " + str(e))
	# 
	# 
	# def addExternalInfo(self):
	# 	addIsophonicsTrackLinks(self.rdf)



if __name__ == '__main__':

	usage = "%prog [options] command filepath"
	parser = OptionParser(usage=usage)
	parser.add_option("-D", "--debug", action="store_true", dest="extradebug", default="false", \
						help="output extra debug messages")
	parser.add_option("-f", "--debug-file", action="store", type="string", dest="logfilename", \
						help="write messages to LOGFILE", metavar="LOGFILE", default="error.log")
	(opts,args) = parser.parse_args()

	commands = ["clean", "fingerprint", "metadata"]
	
	if len(args) == 0:
		parser.error("Must supply a command : \t"+"\n\t\t\t\t\t\t\t".join(commands))
	
	command = args[0]
	if (command not in commands):
		parser.error("Unknown command !")
	
	if len(args) != 2:
		parser.error("You must specify both a command and a filepath !")
	
	loggingConfig = {"format":'%(asctime)s %(levelname)-8s %(message)s',
	                     	  "datefmt":'%d.%m.%y %H:%M:%S',
					 	  "filename":opts.logfilename,
	                      	  "filemode":'a'}
	if opts.extradebug == True:
		loggingConfig["level"]=logging.DEBUG
	else:
		loggingConfig["level"]=logging.INFO
	
	logging.basicConfig(**loggingConfig)
	
	
	ac = AudioCollection()
	debug("--- Starting "+ asctime()  +" ---")
	if command == "clean":
		ac.clean(args[1])
	else:
		ac.walk(*args)	
	debug("--- Finished "+ asctime()  +" ---")
