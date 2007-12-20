#!/usr/bin/env python
# encoding: utf-8
"""
GScsv2RDF.py

A small script to generate timeline/chord ontology RDF corresponding to a .csv file.

Takes CSV files of the form :

crotchetnumber, timestamp (ms), rootnotenumber, chordtype

Where root notes are numbered from 0=C to 11=B and chordtype may be one of :

major, minor, dim, sus4, sus9

Created by Chris Sutton on 2007-12-03.
Copyright (c) 2007 Chris Sutton. All rights reserved.

"""

import os
import mopy
from mopy.timeline import Interval, TimeLine
from mopy.chord import Chord, ChordEvent
from mopy.mo import Signal, Track, MusicArtist
from mopy.MusicInfo import MusicInfo, isBlind
import rdflib; from rdflib import ConjunctiveGraph, URIRef
from urllib import quote as urlencode

from optparse import OptionParser


def GScsv2RDF(infilename, outfilename, format="xml", withdescriptions=False):
	if withdescriptions:
		commonchords = ConjunctiveGraph()
		commonchords.load("CommonChords.rdf")
		extrachords = ConjunctiveGraph()

	lines = open(infilename).readlines()
	
	#
	# Initial model bits
	#
	mi = mopy.MusicInfo()

	homepage = mopy.foaf.Document("http://sourceforge.net/projects/motools")
	mi.add(homepage)
	program = mopy.foaf.Agent()
	program.name = "GScsv2RDF.py"
	program.homepage = homepage
	mi.add(program)

	tl = TimeLine("#tl")
	tl.label = "Timeline derived from "+infilename
	tl.maker = program
	mi.add(tl)

	[artistStr, titleStr] = [f.strip() for f in lines[0].split("\t")]
	# Add artist & title metadata
	signal = Signal()
	signal.time = sig_int = Interval()
	sig_int.label="Whole signal interval";
	sig_int.beginsAtDuration = secondsToXSDDuration(0);
	sig_int.onTimeLine = tl
	signal.published_as = track = Track()
	artist = MusicArtist()
	artist.made = track
	artist.name = artistStr
	track.title = titleStr
	mi.add(sig_int)
	mi.add(signal)
	mi.add(track)
	mi.add(artist)
	
	
	
	
	lineNum = 1
	segmentNum = 0
	thisSegment_i = None
	chordSymbol=''

	t_secs = 0.0
	
	for line in lines[1:]:
#		print "parsing line "+str(lineNum)
		try:
			lastChordSymbol = chordSymbol
			t_secs = getTimestamp(line)
			chordSymbol = getChordSymbol(line)
			if chordSymbol != lastChordSymbol:
#				print " handling new chord symbol"
				segmentNum += 1

				lastSegment_i = thisSegment_i
				thisSegment_i = Interval("#i_"+str(segmentNum))
				thisSegment_i.beginsAtDuration = secondsToXSDDuration(t_secs)
				if lastSegment_i != None:
#					print " terminating last interval"
					lastSegment_i.endsAtDuration = secondsToXSDDuration(t_secs)
					thisSegment_i.intervalAfter = lastSegment_i
					lastSegment_i.intervalBefore = thisSegment_i
				mi.add(thisSegment_i)
				
			
				chordURI = "http://purl.org/ontology/chord/symbol/"+chordSymbol.replace("#","s").replace(",","%2C")

				if withdescriptions and \
				   len(list(commonchords.predicate_objects(URIRef(chordURI)))) == 0 and \
				   len(list(extrachords.predicate_objects(URIRef(chordURI)))) == 0:
					# Deref to grab chord info
					print "loading <"+chordURI+">..."
					extrachords.load(chordURI)

				c = Chord(chordURI)
				c_event = ChordEvent("#ce_"+str(segmentNum))
				c_event.chord = c
				c_event.time = thisSegment_i
				c_event.label = chordSymbol
					
				mi.add(c); mi.add(c_event);
#				print " added new chord event for "+chordURI
							
		except Exception, e:
			print("ERROR : Problem parsing input file at line "+str(lineNum)+" !\n")
			raise
		lineNum+=1
	
	# Finish up :
	if (thisSegment_i):
		thisSegment_i.endsAtDuration = secondsToXSDDuration(t_secs)
	
	if (withdescriptions):
		print "Adding extra chord descriptions to model..."
		chordmi = mopy.importRDFGraph(extrachords)
		for o in chordmi.MainIdx.values():
			mi.add(o)
	
	mopy.exportRDFFile(mi, outfilename, format)

def getTimestamp(line):
	"""Pull out the millisecond timestamp from a line of CSV"""
	try:
		[crotchetnum, timestamp, rootnum, ctype] = line.split(',')
	except Exception,e :
		print "Exception ! Trying to split line : "+line
		raise
	return float(timestamp)/1000

def getChordSymbol(line):
	"""Pull out a chord symbols from a line of CSV."""

	# FIXME : Shouldn't assume sharp note names, but need CO to be extended to allow nameless root notes.
	notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
	
	try:
		[crotchetnum, timestamp, rootnum, ctype] = line.split(',')
	except Exception,e :
		print "Exception ! Trying to split line : "+line
		raise

	rootnote = notes[int(rootnum)]
	
	shorthandmap = {'major' : 'maj', 'minor' : 'min', 'sus4' : 'sus4', 'dim' : 'dim', 'sus9' : '(1,5,9)'}
	
		
	return rootnote+':'+shorthandmap[ctype.strip()]
	
def secondsToXSDDuration(s):
	"""Return an xsd:duration string for the given number of seconds."""
	return "P"+str(float(s))+"S"


if __name__ == '__main__':

	usage = "%prog [options] (infile.csv | dirname) [outfile.rdf]"
	parser = OptionParser(usage=usage)
	parser.add_option("--format", action="store", type="string", dest="format", \
						help="format for output (xml or n3)", metavar="FORMAT", default="xml")
	parser.add_option("-d", "--descriptions", action="store_true", dest="descriptions",\
						help="include descriptions of uncommon chords", default=False)
	(opts,args) = parser.parse_args()

	if len(args) < 1 or len(args) > 2:
		parser.error("Wrong number of arguments !")
	else:
		infilename = args[0]

	if len(args) == 1:
		if os.path.isfile(infilename):
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
	
	if os.path.isfile(infilename):
		GScsv2RDF(infilename, outfilename, opts.format, opts.descriptions)
	else:
		for f in os.listdir(infilename):
			if not f.endswith(".csv"):
				continue
			print f
			fullname=os.path.join(infilename,f)
			if os.path.isfile(fullname):
				dotpos=f.rfind(".")
				if dotpos == -1:
					outfilename = fullname+".rdf"
				else:
					outfilename = os.path.join(infilename,f[:dotpos]+".rdf")
				GScsv2RDF(fullname, outfilename, opts.format, opts.descriptions)			
