#!/usr/bin/python2.4
#
# Abstraction of an audio collection, living in a top-directory
#

import os
import os.path
import logging
import re

from time import asctime
from MbzURIConverter import *
from MbzTrackLookup import *
from FPTrackLookup import FPTrackLookup
from RdfHub import *
from ExternalSources import *
from Id3Writer import *
from logging import log, error, warning, info, debug
from optparse import OptionParser

exclPatterns = r".*(jpg|jpeg|txt|ini|db|DS\_Store|m3u|pls|xml|log)$"
excludeRE = re.compile(exclPatterns, re.IGNORECASE)


class AudioCollection :

	def __init__(self,directory, extradebug=True, errorlog="error.log") :
		self.loggingConfig = {"format":'%(asctime)s %(levelname)-8s %(message)s',
	                     	  "datefmt":'%d.%m.%y %H:%M:%S',
						 	  "filename":errorlog,
	                      	  "filemode":'a'}
		if extradebug == True:
			self.loggingConfig["level"]=logging.DEBUG
		else:
			self.loggingConfig["level"]=logging.INFO
		
		logging.basicConfig(**self.loggingConfig)
		
		self.dir = directory
		self.walk = os.walk(directory)
		self.rdf = RdfHub()
		self.gnat_processed = 0
		self.gnat_succeeded = 0
		self.fp_processed = 0
		self.fp_succeeded = 0

	def batch_gnat(self) :
		self.rdf.setContext("batch gnat")
		self.rdf.dropAllLocks()
		for root,dirs,files in self.walk :
			for name in files :
				if (re.match(excludeRE, name) == None):
					self.gnat_processed = self.gnat_processed + 1

					filename = os.path.join(root,name)
					fileURIstr = 'file://'+filename
					debug("Considering "+filename)
					if self.rdf.haveMD_URI(filename) == False:
						if self.rdf.lock(fileURIstr) :
							try :
								lookup = MbzTrackLookup(filename)
								mbzuri = lookup.getMbzTrackURI()
								mbzconvert = MbzURIConverter(mbzuri)
								self.rdf.addAvailableAs(mbzconvert.getURI(),fileURIstr)
								self.gnat_succeeded = self.gnat_succeeded + 1
								self.rdf.commit()
							except MbzLookupException, e:
								error(" - " + e.message)
							except FileTypeException, e:
								error(" - " + e.message)
								self.gnat_processed = self.gnat_processed -1
							self.rdf.unlock(fileURIstr)
					else :
						debug("Found existing URI in store")
						self.gnat_succeeded = self.gnat_succeeded + 1

		info('Files processed : ' +str(self.gnat_processed))
		info('Successful identifications : '+str(self.gnat_succeeded))
		
	def batch_fp(self) :
		lookup = FPTrackLookup()
		self.rdf.setContext("batch fp")
		self.rdf.dropAllLocks()
		for root,dirs,files in self.walk :
			for name in files :
				if (re.match(excludeRE, name) == None):
					self.fp_processed += 1
					filename = os.path.join(root,name)
					debug("Considering "+filename)
					fileURIstr = "file://"+filename
					if self.rdf.have_URI(filename, "batch_fp") == False:
						if self.rdf.lock(fileURIstr) :
							results = lookup.fpFile(filename)
							if results.has_key("puids"):
								self.fp_succeeded += 1
								self.rdf.addItemType(fileURIstr)
								for puid in results["puids"]:
									self.rdf.addPUID(fileURIstr, puid)
							if results.has_key("title"):
								self.rdf.addTitleL(fileURIstr, results["title"])
							if results.has_key("artist"):
								self.rdf.addArtistL(fileURIstr, results["artist"])
							if results.has_key("year"):
								self.rdf.addYearL(fileURIstr, results["year"])
							if results.has_key("genres"):
								for genre in results["genres"]:
									self.rdf.addGenreL(fileURIstr, genre)
							
							self.rdf.commit()
							self.rdf.unlock(fileURIstr)
					else:
						debug("Found existing FP-derived URI.")
		info('Files processed : ' +str(self.fp_processed))
		info('Successful identifications : '+str(self.fp_succeeded))
		#print self.serialize("xml")

	def addExternalInfo(self):
		addIsophonicsTrackLinks(self.rdf)

	def serialize(self,type) :
		return self.rdf.getSerializedGraph(type)



if __name__ == '__main__':
	usage = "%prog [options] command musicpath"
	parser = OptionParser(usage=usage)
	parser.add_option("-D", "--debug", action="store_true", dest="extradebug", default="false", \
						help="output extra debug messages")
	parser.add_option("-f", "--debug-file", action="store", type="string", dest="logfilename", \
						help="write messages to LOGFILE", metavar="LOGFILE", default="error.log")	
	parser.add_option("-w", "--write-file", action="store", type="string", dest="dumpfilename", \
						help="write the resulting triplestore to DUMP", metavar="DUMP")
	parser.add_option("--write-format", action="store", type="string", dest="dumpformat", \
						help="use FORMAT format for the output file (default : 'xml')", metavar="FORMAT", default="xml")
	(opts,args) = parser.parse_args()
	
	if not ( (len(args) == 2) \
		   | ((len(args) in [0,2]) & (opts.dumpfilename <> None)) \
		   ):
		parser.error("Incorrect number of arguments given !")
	
	if (len(args)==2):
		if (args[0] not in ["batch_gnat", "batch_fp", "addExternalInfo"]):
			parser.error("Unknown command !")
	
		(command, musicpath) = args
	
		ac = AudioCollection(musicpath, opts.extradebug, opts.logfilename)
		debug("--- Starting "+ asctime()  +" ---")
		getattr(ac, command)()
		ac.rdf.commit()
	else:
		# We're just doing a data dump
		ac = AudioCollection(".")
		debug("--- Starting data dump "+ asctime()  +" ---")
	
	if opts.dumpfilename <> None:
		debug("Dumping data to file...")
		out = open(opts.dumpfilename,'w')
		out.write(ac.serialize(opts.dumpformat))
		out.close()

	debug("--- Finished "+ asctime()  +" ---")
