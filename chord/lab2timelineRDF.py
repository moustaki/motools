#!/usr/bin/env python
# encoding: utf-8
"""
lab2timelineRDF.py

A small script to generate timeline ontology RDF corresponding to a .lab label file

Created by Chris Sutton on 2007-09-14.
Copyright (c) 2007 Chris Sutton. All rights reserved.
"""

import mopy
from mopy.timeline import Interval, RelativeTimeLine
import rdflib

from optparse import OptionParser

def lab2timelineRDF(infilename, outfilename, format="xml"):
	infile = open(infilename, 'r')
	lines = infile.readlines()

	mi = mopy.MusicInfo()

	homepage = mopy.foaf.Document("http://sourceforge.net/projects/motools")
	mi.add(homepage)
	program = mopy.foaf.Agent()
	program.name = "lab2timelineRDF.py"
	program.homepage = homepage
	mi.add(program)

	
	tl = RelativeTimeLine("tl")
	tl.label = "Timeline derived from "+infilename
	tl.maker = program
	mi.add(tl)
	
	intervalNum = 0
	for line in lines:
		i = Interval("i"+str(intervalNum))
		try:
			[start_s, end_s, label] = parseLabLine(line)
			i.beginsAtDuration = secondsToXSDDuration(start_s)
			i.endsAtDuration = secondsToXSDDuration(end_s)
			i.label = label
			i.onTimeLine = tl
		except Exception, e:
			raise Exception("Problem parsing input file at line "+str(intervalNum+1)+" !\n"+str(e))
		mi.add(i)
		intervalNum+=1
			
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

	lab2timelineRDF(infilename, outfilename, opts.format)