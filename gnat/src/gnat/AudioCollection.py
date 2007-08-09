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
from PUIDTrackLookup import *
from RdfHub import *
from ExternalSources import *
from Id3Writer import *
from logging import log, error, warning, info, debug
from optparse import OptionParser

exclPatterns = r".*(jpg|jpeg|txt|ini|db|DS\_Store|m3u|pls|xml|log|png|\.directory)$"
excludeRE = re.compile(exclPatterns, re.IGNORECASE)


class AudioCollection :

	def __init__(self) :
		self.rdf = RdfHub()
		self.gnat_processed = 0
		self.gnat_succeeded = 0
		self.fp_processed = 0
		self.fp_succeeded = 0

	def add(self, filepath):
		if os.path.isdir(filepath):
			count=0
			for root,dirs,files in os.walk(filepath) :
				for name in files :
					if (re.match(excludeRE, name) == None):
						filename = os.path.join(root,name)
						self.addFile(filename)
						count+=1
			info("Added %d files.", count)
		else:
			self.addFile(filepath)
			info("Added 1 file.")
				
	def addFile(self, filename):
		FilesContextName = "files"
		self.rdf.setContext(FilesContextName)
		self.rdf.addItemType(self.rdf.FilenameToURI(filename))

	def batch_gnat(self) :
		MDContextName = "batch gnat"
		self.rdf.setContext(MDContextName)
		self.rdf.dropAllLocks()
		for itemURIstr in self.rdf.getItemURIs(contextName=None):
			filename = self.rdf.URItoFilename(itemURIstr)
			self.gnat_processed = self.gnat_processed + 1
			debug("Considering "+filename)
			if self.rdf.have_URI(itemURIstr, MDContextName) == False:
				if self.rdf.lock(itemURIstr) :
					try :
						lookup = MbzTrackLookup(filename)
						mbzuri = lookup.getMbzTrackURI()
						mbzconvert = MbzURIConverter(mbzuri)
						self.rdf.addAvailableAs(mbzconvert.getURI(),itemURIstr)
						self.gnat_succeeded = self.gnat_succeeded + 1
						self.rdf.commit()
					except MbzLookupException, e:
						error(" - " + e.message)
					except FileTypeException, e:
						error(" - " + e.message)
						self.gnat_processed = self.gnat_processed -1
					self.rdf.unlock(itemURIstr)
			else :
				debug("Found existing URI in store")
				self.gnat_succeeded = self.gnat_succeeded + 1

		info('Files processed : ' +str(self.gnat_processed))
		info('Successful identifications : '+str(self.gnat_succeeded))
		
	def batch_fp(self) :
		lookup = FPTrackLookup()
		FPContextName = "batch fp"
		self.rdf.setContext(FPContextName)
		self.rdf.dropAllLocks()
		for itemURIstr in self.rdf.getItemURIs(contextName=None) :
			filename = self.rdf.URItoFilename(itemURIstr)
			debug("Considering "+filename)
			self.fp_processed += 1
			if self.rdf.have_URI(itemURIstr, FPContextName) == False:
				if self.rdf.lock(itemURIstr) :
					# TODO : We may have a PUID but no MBZID - If so, skip fingerprinting and just do PUIDTrackLookuplect
					results = lookup.fpFile(filename)
					if results.has_key("title"):
						self.rdf.addTitleL(itemURIstr, results["title"])
					if results.has_key("artist"):
						self.rdf.addArtistL(itemURIstr, results["artist"])
					if results.has_key("year"):
						self.rdf.addYearL(itemURIstr, results["year"])
					if results.has_key("genres"):
						for genre in results["genres"]:
							self.rdf.addGenreL(itemURIstr, genre)
					if results.has_key("puids"):
						success=False
						for puid in results["puids"]:
							self.rdf.addPUID(itemURIstr, puid)
							try:
								pl = PUIDTrackLookup(filename, puid, results)
								mbzuri = pl.getMbzTrackURI()
								mbzconvert = MbzURIConverter(mbzuri)
								self.rdf.addAvailableAs(mbzconvert.getURI(), itemURIstr)
								success=True
							except MbzLookupException, e:
								error(" - " + e.message)
						if success:
							self.fp_succeeded += 1							
					self.rdf.commit()
					self.rdf.unlock(itemURIstr)
					if self.fp_processed % 20 == 0:
						info('Files processed : ' +str(self.fp_processed))
						info('Successful identifications : '+str(self.fp_succeeded))
			else:
				debug("Found existing URI in store")
				self.fp_succeeded += 1
		info('Files processed : ' +str(self.fp_processed))
		info('Successful identifications : '+str(self.fp_succeeded))

	def crawl(self,path) :
		 for itemURIstr in self.rdf.getItemURIs(contextName=None) :
		 	filename = self.rdf.URItoFilename(itemURIstr)
			debug("Considering "+filename)
			manifURIs = self.rdf.availableAs(itemURIstr,contextName=None)
			for manifURI in manifURIs :
				#try :
				debug("Loading "+manifURI)
				self.rdf.load(manifURI) 
				self.rdf.commit()
				debug("Crawling from "+manifURI)
				self.rdf.crawl(manifURI,path)
				self.rdf.commit()
				#except Exception, e:
				#	error(" - " + str(e))


	def addExternalInfo(self):
		addIsophonicsTrackLinks(self.rdf)

	def serialize(self,type) :
		return self.rdf.getSerializedGraph(type)



if __name__ == '__main__':
	usage = "%prog [options] command [filepath]"
	parser = OptionParser(usage=usage)
	parser.add_option("-D", "--debug", action="store_true", dest="extradebug", default="false", \
						help="output extra debug messages")
	parser.add_option("-f", "--debug-file", action="store", type="string", dest="logfilename", \
						help="write messages to LOGFILE", metavar="LOGFILE", default="error.log")
	defaultdumpfilename="dump"	
	parser.add_option("-w", "--write-file", action="store", type="string", dest="dumpfilename", \
						help="write the resulting triplestore to DUMP", metavar="DUMP", default=defaultdumpfilename)
	parser.add_option("--write-format", action="store", type="string", dest="dumpformat", \
						help="use FORMAT format for the output file (default : 'xml')", metavar="FORMAT", default="xml")
	(opts,args) = parser.parse_args()

	nargs =  {"batch_gnat":0, "batch_fp":0, "addExternalInfo":0, "add":1, "dump":0, "crawl":4}
	commands = nargs.keys()

	if len(args) == 0:
		parser.error("Must supply a command : \t"+"\n\t\t\t\t\t\t\t".join(commands))

	command = args[0]
	if (command not in commands):
		parser.error("Unknown command !")
	
	if command <> "crawl" and nargs[command] <> (len(args) - 1) :
		parser.error("Incorrect number of arguments given ! Command \""+command+"\" expects "+str(nargs[command])+" arguments.")

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
	if command <> "dump" and command <> "crawl":
		getattr(ac, command)(*args[1:])
		ac.rdf.commit()

	if command == "crawl":
		path = args[1:]
		debug("Crawling using path: "+str(path))
		ac.crawl(path)

	if (command == "dump") or (opts.dumpfilename <> defaultdumpfilename):
		debug("Dumping data to file...")
		dumpfilename = opts.dumpfilename
		if dumpfilename==defaultdumpfilename:
			dumpfilename+="."+opts.dumpformat
		out = open(dumpfilename,'w')
		out.write(ac.serialize(opts.dumpformat))
		out.close()

	debug("--- Finished "+ asctime()  +" ---")
