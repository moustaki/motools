#!/usr/bin/env python
# encoding: utf-8
"""
labchords2RDF.py

A small script to generate timeline/chord ontology RDF corresponding to a .lab label file with
chord symbols as described in Harte, 2005 (ISMIR proceedings)

Created by Chris Sutton on 2007-09-14.
Copyright (c) 2007 Chris Sutton. All rights reserved.
"""

import os
import mopy
from mopy.timeline import Interval, RelativeTimeLine
from mopy.chord import Chord
from mopy.MusicInfo import MusicInfo, isBlind
import rdflib; from rdflib import ConjunctiveGraph, URIRef
from urllib import quote as urlencode

from optparse import OptionParser

def labchords2RDF(infilename, outfilename, format="xml", audiofilename=None, withdescriptions=False):
	if withdescriptions:
		commonchords = ConjunctiveGraph()
		commonchords.load("CommonChords.rdf")
		extrachords = ConjunctiveGraph()
	
	infile = open(infilename, 'r')
	lines = infile.readlines()

	mi = mopy.MusicInfo()

	homepage = mopy.foaf.Document("http://sourceforge.net/projects/motools")
	mi.add(homepage)
	program = mopy.foaf.Agent()
	program.name = "labchords2RDF.py"
	program.homepage = homepage
	mi.add(program)

	
	tl = RelativeTimeLine("#tl")
	tl.label = "Timeline derived from "+infilename
	tl.maker = program
	mi.add(tl)
	
	intervalNum = 0
	for line in lines:
		i = Interval("#i"+str(intervalNum))
		try:
			[start_s, end_s, label] = parseLabLine(line)
			i.beginsAtDuration = secondsToXSDDuration(start_s)
			i.endsAtDuration = secondsToXSDDuration(end_s)
			i.label = "Interval containing "+label+" chord."
			i.onTimeLine = tl
			
			# Produce chord object for the label :
			chordURI = "http://purl.org/ontology/chord/symbol/"+label.replace("#","s").replace(",","%2C")

			if withdescriptions and \
			   len(list(commonchords.predicate_objects(URIRef(chordURI)))) == 0 and \
			   len(list(extrachords.predicate_objects(URIRef(chordURI)))) == 0:
				# Deref to grab chord info
				print "loading "+chordURI+"..."
				extrachords.load(chordURI)
				
			c = mopy.chord.Chord(chordURI)
			c_event = mopy.chord.ChordEvent("#ce"+str(intervalNum))
			c_event.chord = c
			c_event.time = i
		except Exception, e:
			raise Exception("Problem parsing input file at line "+str(intervalNum+1)+" !\n"+str(e))
		mi.add(i)
		mi.add(c)
		mi.add(c_event)
		intervalNum+=1
	
	# Extract extra info from audio file :
	if audiofilename != None:
		absaudiofilename = os.path.abspath(audiofilename)
		ac_module = __import__("gnat.AudioCollection",[],[],["AudioCollection"])
		ac = ac_module.AudioCollection()
		cwd = os.getcwd()
		os.chdir("./gnat") # so we can find genpuid etc.
		fp_mi = ac.fingerprint(absaudiofilename)
		if hasattr(fp_mi, "TrackIdx") and len(fp_mi.TrackIdx) > 0 and not isBlind(fp_mi.TrackIdx.values()[0]):
			print "Adding info from audiofile fingerprinting."
			for o in fp_mi.MainIdx.values():
				mi.add(o)
			if hasattr(fp_mi, "SignalIdx") and len(fp_mi.SignalIdx) > 0:
				fp_mi.SignalIdx.values()[0].time = sig_int = Interval()
				sig_int.label="Whole signal interval";
				sig_int.beginsAtDuration = secondsToXSDDuration(0);
				sig_int.onTimeLine = tl
				mi.add(sig_int)
		else:
			print "Fingerprinting failed, trying metadata lookup..."
			md_mi = ac.metadata(absaudiofilename)
			if hasattr(md_mi, "TrackIdx") and len(md_mi.TrackIdx) > 0 and not isBlind(md_mi.TrackIdx.values()[0]):
				print "Adding info from audiofile metadata lookup."
				for o in md_mi.MainIdx.values():
					mi.add(o)
				signal = Signal()
				signal.published_as = md_mi.TrackIdx.values()[0]
				signal.time = sig_int = Interval()
				sig_int.label="Whole signal interval";
				sig_int.beginsAtDuration = secondsToXSDDuration(0);
				sig_int.onTimeLine = tl
				mi.add(sig_int)
				mi.add(signal)
		os.chdir(cwd)

	print "Adding extra chord descriptions to model..."
	chordmi = mopy.importRDFGraph(extrachords)
	for o in chordmi.MainIdx.values():
		mi.add(o)
	
	mopy.exportRDFFile(mi, outfilename, format)


def parseLabLine(line):
	"""Split a line from a .lab file into start time, end time and the label."""
	[start_s, end_s, label_w_cr] = line.split(None, 2)  # split by whitespace
	if label_w_cr[-1:] == "\n":
		label = label_w_cr[:-1]
	else:
		label = label_w_cr
	return [start_s, end_s, label]
	

def secondsToXSDDuration(s):
	"""Return an xsd:duration string for the given number of seconds."""
	return "P"+str(float(s))+"S"

if __name__ == '__main__':

	usage = "%prog [options] infile.lab [outfile.rdf]"
	parser = OptionParser(usage=usage)
	parser.add_option("--format", action="store", type="string", dest="format", \
						help="format for output (xml or n3)", metavar="FORMAT", default="xml")
	parser.add_option("-f", "--audiofile", action="store", type="string", dest="audiofilename",\
						help="audio file to analyse for extra info", metavar="FILENAME", default=None)
	parser.add_option("-d", "--descriptions", action="store_true", dest="descriptions",\
						help="include descriptions of uncommon chords", default=False)
	(opts,args) = parser.parse_args()
	
	if len(args) < 1 or len(args) > 2:
		parser.error("Wrong number of arguments !")
	else:
		infilename = args[0]
		
	if len(args) == 1:
		dotpos=infilename.rfind(".")
		if dotpos == -1:
			outfilename = infilename+".rdf"
		else:
			outfilename = infilename[:dotpos]+".rdf"
	else:
		outfilename = args[1]
	
	validFormats=["xml", "n3"]
	if opts.format not in validFormats:
		parser.error("Invalid format specified ! Must be one of : "+", ".join(validFormats))

	labchords2RDF(infilename, outfilename, opts.format, opts.audiofilename, opts.descriptions)
