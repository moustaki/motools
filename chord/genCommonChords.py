#!/usr/bin/env python
# encoding: utf-8
"""
genCommonChords.py

Created by Chris Sutton on 2007-10-10.
Copyright (c) 2007 Chris Sutton. All rights reserved.
"""

import sys
import os
import rdflib; from rdflib import ConjunctiveGraph

def main():
#	f = open("CommonChords.rdf",'w');
	g = ConjunctiveGraph()
	
	prefix = "http://purl.org/ontology/chord/symbol/"
	notes = ['C','D','E','F','G','A','B']
	mods = ['b','','s']
	bases = ['', ':maj', ':min', ':dim', ':aug', ':maj7', ':min7', ':7', ':dim7', \
			':hdim7', ':minmaj7', ':maj6', ':min6', ':9', ':maj9', ':min9', ':sus4', ':sus2']

	chordURI = prefix+'N'
	print "loading "+chordURI
	g.load(chordURI)
	for note in notes:
		for mod in mods:
			for base in bases:
				chordURI = prefix+note+mod+base
				#f.write(prefix+note+mod+base+"\n")
				print "loading "+chordURI
				g.load(chordURI)
				
	print "Writing graph out..."
	g.serialize('CommonChords.rdf','xml')
	
if __name__ == '__main__':
	main()

