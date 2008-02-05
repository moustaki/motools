#!/usr/bin/python
# encoding: utf-8
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
from mopy.mo import AudioFile, Track

exclPatterns = r".*(jpg|jpeg|txt|ini|db|DS\_Store|m3u|pls|xml|log|png|\.directory)$"
excludeRE = re.compile(exclPatterns, re.IGNORECASE)


class AudioCollection :

	def __init__(self) :
		self.rdf = RdfFile()
		self.processed = 0
		self.succeeded = 0
		
	def walk(self, commandName, filepath, CSVoutput=False):
		dcount=0; fcount=0
		if os.path.isdir(filepath):
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
		else:
			if filepath.endswith('.csv') and commandName == "metadata":
				f=open(filepath)
				if CSVoutput:
					f_out=open('info_metadata.csv','w')
				else:
					if not self.rdf.open("info_"+commandName+".rdf"):
						error("Existing info_"+commandName+".rdf file found !")
						raise Exception("Couldn't create output file !")
				try:
					for line in f:
						fields = parse_csv(line)
						res = self.metadata(fields["URI"], fields, just_URI=CSVoutput)
						if CSVoutput:
							f_out.write(fields["URI"]+","+res+"\n")
						else:
							self.rdf.addMusicInfo(res)
						fcount+=1
					if not CSVoutput:
						self.rdf.write()
						self.rdf.clear()
				except Exception, e:
					error("Malformed CSV !")
					raise
			else:
				error("Filepath given is not a directory ! "+filepath)
		info("Succeeded for %d/%d files across %d directories.", self.succeeded, fcount, dcount)

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
	
	def metadata(self, filename, true_md=None, just_URI=False) :
		debug("Considering "+filename)
		mi = MusicInfo()
		try :
			lookup = MbzTrackLookup(filename,true_md)
			mbzuri = lookup.getMbzTrackURI()
			mbzconvert = MbzURIConverter(mbzuri)
			if just_URI:
				return mbzconvert.getURI()
			if (filename.startswith("http://")):
				af = AudioFile(filename)
			else:
				af = AudioFile(urlencode(os.path.basename(filename)))
			mbz = Track(mbzconvert.getURI())
			mbz.available_as = af
			mi.add(af); mi.add(mbz)
			self.succeeded+=1
		except MbzLookupException, e:
			error(" - " + e.message)
		except FileTypeException, e:
			error(" - " + e.message)
		if just_URI:
			return ""
		return mi

	def fingerprint(self, filename) :
		lookup = FPTrackLookup()
		debug("Considering "+filename)
		mi = lookup.fpFile(filename)
		if hasattr(mi, "TrackIdx") and len(mi.TrackIdx) > 0:
			if not isBlind(mi.TrackIdx.values()[0]):
				self.succeeded+=1
		return mi


# Parses a line of CSV containing : URI, artist name, album name, track name [, tracknumber]
def parse_csv(line):
	fields=[x.strip() for x in line.split(',')]
	res = {"URI":fields[0]}
	if len(fields[1])>0:
		res["artist"] = [fields[1]]
	if len(fields[2])>0:
		res["album"] = [fields[2]]
	if len(fields[3])>0:
		res["title"] = [fields[3]]
	if len(fields)>4 and len(fields[4])>0:
		res["tracknumber"] = [fields[4]]
	debug(" parsed as : "+str(res))
	return res


if __name__ == '__main__':

	usage = "%prog [options] command filepath"
	parser = OptionParser(usage=usage)
	parser.add_option("-D", "--debug", action="store_true", dest="extradebug", default=True, \
						help="output extra debug messages")
	parser.add_option("-f", "--debug-file", action="store", type="string", dest="logfilename", \
						help="write messages to LOGFILE", metavar="LOGFILE", default="error.log")
	parser.add_option("-c", "--csv-output", action="store_true", dest="CSVoutput", default=False,\
						help="write CSV as output (only if using CSV input)")

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
		ac.walk(commandName=args[0],filepath=args[1],CSVoutput=opts.CSVoutput)
	debug("--- Finished "+ asctime()  +" ---")
