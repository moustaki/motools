#!/usr/bin/env python
# encoding: utf-8
"""
mma2RDF.py

A small script to generate timeline/chord ontology RDF corresponding to a .mma file.

Created by Chris Sutton on 2007-09-17.
Copyright (c) 2007 Chris Sutton. All rights reserved.

TODO :
- Add bar and beat events
- Handle inversions properly ?? We do slash bass notation, but currently ignore >-type inversions

"""

import os
import mopy
from mopy.timeline import Interval, TimeLine
from mopy.chord import Chord, ChordEvent
from mopy.mo import Signal
from mopy.MusicInfo import MusicInfo, isBlind
import rdflib; from rdflib import ConjunctiveGraph, URIRef
from urllib import quote as urlencode

from optparse import OptionParser

mmabin = "/usr/local/bin/mma"
chordmap = {}

def mma2RDF(infilename, outfilename, format="xml", audiofilename=None, withdescriptions=False):
	if withdescriptions:
		commonchords = ConjunctiveGraph()
		commonchords.load("CommonChords.rdf")
		extrachords = ConjunctiveGraph()

	# Compile mma file and grab output
	lines = os.popen(mmabin + " \"" + infilename + "\" -nrw").readlines()
	print "\n".join(lines)
	
	
	#
	# Initial model bits
	#
	mi = mopy.MusicInfo()

	homepage = mopy.foaf.Document("http://sourceforge.net/projects/motools")
	mi.add(homepage)
	program = mopy.foaf.Agent()
	program.name = "mma2RDF.py"
	program.homepage = homepage
	mi.add(program)

	
	tl = TimeLine("#tl")
	tl.label = "Timeline derived from "+infilename
	tl.maker = program
	mi.add(tl)
		
	# extract tempo from mma file
	tempo = 60
	mmafile = open(infilename,'r')
	for line in mmafile:
		if line.startswith("Tempo "):
			tempo = int(line[len("Tempo "):].strip().split()[0])
			print "Found tempo = "+str(tempo)
			break
	
	lineNum = 1
	thisBar_i = None
	i = None
	t_secs = 0.0
	for line in lines:
		print "parsing line "+str(lineNum)
		try:
			#i = None
			barNum = getBarNum(line)
			
			lastBar_i = thisBar_i
			thisBar_i = Interval("#i_"+str(barNum))
			thisBar_i.beginsAtDuration = secondsToXSDDuration(t_secs)
			if lastBar_i != None:
				lastBar_i.endsAtDuration = secondsToXSDDuration(t_secs)
				thisBar_i.intervalAfter = lastBar_i
				lastBar_i.intervalBefore = thisBar_i
			mi.add(thisBar_i)
		
			chordMMASymbols = getChordSymbols(line)
			beatNum=1
			for chordMMASymbol in chordMMASymbols:
				if chordMMASymbol != '/':
					print " handling new chord symbol"
					if i != None:
						print " terminating last interval"
						i.endsAtDuration = secondsToXSDDuration(t_secs)
						mi.add(i)
				
					i = Interval("#i_"+str(barNum)+"_"+str(beatNum))
					i.onTimeLine = tl
					i.beginsAtDuration = secondsToXSDDuration(t_secs)
					
					chordURI = "http://purl.org/ontology/chord/symbol/"+mmaSymbolToChordSymbol(chordMMASymbol).replace("#","s").replace(",","%2C")

					if withdescriptions and \
					   len(list(commonchords.predicate_objects(URIRef(chordURI)))) == 0 and \
					   len(list(extrachords.predicate_objects(URIRef(chordURI)))) == 0:
						# Deref to grab chord info
						print "loading <"+chordURI+">..."
						extrachords.load(chordURI)

					c = Chord(chordURI)
					c_event = ChordEvent("#ce_"+str(barNum)+"_"+str(beatNum))
					c_event.chord = c
					c_event.time = i
					c_event.label = mmaSymbolToChordSymbol(chordMMASymbol)
					
					mi.add(c); mi.add(c_event); mi.add(i)
					print " added new chord event for "+chordURI
				else:
					if beatNum==1: # Need to continue the last seen chord
						print " continuing last bar's chord"
						#i = Interval("i_"+str(barNum)+"_"+str(beatNum))
						#i.onTimeLine = tl
						#i.beginsAtDuration = secondsToXSDDuration(t_secs)
						#c_event = ChordEvent("ce_"+str(barNum)+"_"+str(beatNum))
						#c_event.chord = c
						#c_event.time = i
						#mi.add(c_event); mi.add(i)
				
				beatNum+=1
				t_secs += 60.0/tempo
		except Exception, e:
			print("ERROR : Problem parsing input file at line "+str(lineNum)+" !\n")
			raise
		lineNum+=1
	
	# Finish up :
	if (thisBar_i):
		thisBar_i.endsAtDuration = secondsToXSDDuration(t_secs)
	if i != None:
		print " terminating last interval"
		i.endsAtDuration = secondsToXSDDuration(t_secs)
		mi.add(i)
	
	
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
	else:
		# Just put in a blank node for the signal :
		signal = Signal()
		signal.time = sig_int = Interval()
		sig_int.label="Whole signal interval";
		sig_int.beginsAtDuration = secondsToXSDDuration(0);
		sig_int.onTimeLine = tl
		mi.add(sig_int)
		mi.add(signal)

	if (withdescriptions):
		print "Adding extra chord descriptions to model..."
		chordmi = mopy.importRDFGraph(extrachords)
		for o in chordmi.MainIdx.values():
			mi.add(o)
	
	mopy.exportRDFFile(mi, outfilename, format)

def getBarNum(line):
	"""Pull out the bar number from a line of compiled mma."""
	l = line.strip()
	if l.find(':') == -1:
		raise Exception("No bar number found !")
	return l[0:l.find(':')]

def getChordSymbols(line):
	"""Pull out a list of chord symbols from a line of compiled mma."""
	colon_loc = line.find(':')
	if colon_loc == -1:
		raise Exception("No bar number found !")
	chordline = line[colon_loc+1:].strip()
	return chordline.split()

def mmaSymbolToChordSymbol(symbol):
	"""Return the Chord Ontology symbol corresponding to the given MMA chord symbol"""
	notes = ['A','B','C','D','E','F','G']
	modifiers = ['#','b']
	
	if symbol.startswith('z'):
		return chordmap['z']
	if '>' in symbol:
		symbol = symbol[0:symbol.find('>')] # strip off > inversions
	if 'z' in symbol:
	    symbol = symbol[0:symbol.find('z')] # strip off silence controls
	if symbol[0] in ['-','+']:
		symbol = symbol[1:] #strip off octave shifts
	symbol = symbol.replace('&','b')

	# Find start of shorthand
	shpos = 0
	if (symbol[shpos].upper() in notes):
		shpos+=1
	# Have to do these separately so they can't be mixed, eg "Gb#5" => "Gb with shorthand '#5'"
	while (shpos < len(symbol) and symbol[shpos] == '#'):
		shpos+=1
	while (shpos < len(symbol) and symbol[shpos] == 'b'):
		shpos+=1
	
	# Find start of bass note
	basspos = symbol.rfind('/')
	if basspos == -1:
		basspos = len(symbol)
    
	res = symbol[0:shpos] + ":" + chordmap[symbol[shpos:basspos]]
	if basspos < len(symbol):
		return res + "/" + str(scaleIntervalFromNoteNames(symbol[:shpos], symbol[basspos+1:]))
	return res
	
def secondsToXSDDuration(s):
	"""Return an xsd:duration string for the given number of seconds."""
	return "P"+str(float(s))+"S"

def scaleIntervalFromNoteNames(n1, n2):
	kNoteNames = ['C','D','E','F','G','A','B'] * 2
	kNoteDists =    [2,  2,  1,  2,  2,  2,  1] * 2	

	n1idx = kNoteNames.index(n1.upper()[0])
	n2idx = kNoteNames.index(n2.upper()[0], n1idx)
	if (n1idx < 0 or n2idx < 0):
		return -1
	base_interval = 1 + n2idx - n1idx

	st_dist = sum(kNoteDists[n1idx:n2idx])
	expected_dist = sum(kNoteDists[0:base_interval-1])

	mod_dist = n1.count('b') - n1.count('#') \
             + n2.count('#') - n2.count('b') \
             + st_dist - expected_dist
	if abs(mod_dist) > 2:
		return -1

	mods = ['bb','b','','#','##'][2 + mod_dist]
	return mods + str(base_interval)

#
# Chord map
#

chordmap = \
{#           MMA / BiaB            C4DM short
 # (courtesy of Matthias Mauch 04.10.07)
"          7           ":"    7             ",              
"          7omit3      ":"    7(*3)         ",              
"          7(omit3)    ":"    7(*3)         ",              
"          7b5b9       ":"    7(b5,b9)      ",       # Added for girl.mma
"          7b9#11      ":"    7(b9,s11)    ",              
"          7b9         ":"    7(b9)         ",              
"          7-9         ":"    7(b9)         ",              
"          7#11        ":"    7(s11)        ",              
"          7#9b13      ":"    7(s9,b13)    ",              
"          7#9#11      ":"    7(s9,s11)    ",              
"          7#9         ":"    7(s9)         ",              
"          7+9         ":"    7(s9)         ",              
"          9           ":"    9             ",              
"          9#11        ":"    9(s11)        ",             
"          +           ":"    aug           ",             
"          #5          ":"    aug           ",             
"          aug         ":"    aug           ",             
"          aug9M7      ":"    aug(7,9)      ",             
"          +9M7        ":"    aug(7,9)      ",             
"          +M7         ":"    aug(7)        ",              
"          M7+5        ":"    aug(7)        ",              
"          M7#5        ":"    aug(7)        ",              
"          MAJ7#5      ":"    aug(7)        ",              
"          aug9        ":"    aug(b7,9)    ",              
"          9#5         ":"    aug(b7,9)    ",              
"          +9          ":"    aug(b7,9)    ",              
"          9+5         ":"    aug(b7,9)    ",              
"          9+          ":"    aug(b7,9)    ",              
"          +7b9#11     ":"    aug(b7,b9,s11)",              
"          7#5b9       ":"    aug(b7,b9)   ",              
"          aug7b9      ":"    aug(b7,b9)   ",              
"          7#5#9       ":"    aug(b7,s9)   ",              
"          aug7#9      ":"    aug(b7,s9)   ",              
"          7+          ":"    aug(b7)       ",              
"          aug7        ":"    aug(b7)       ",              
"          +7          ":"    aug(b7)       ",              
"          7#5         ":"    aug(b7)       ",              
"          7+5         ":"    aug(b7)       ",              
"          MMA / BiaB  ":"    C4DM short    ",              
"          dim3        ":"    dim           ",              
"          m(b5)       ":"    dim           ",              
"          mb5         ":"    dim           ",              
"          dim7        ":"    dim7          ",              
"          dim         ":"    dim7          ",              
"          dim7(addM7) ":"    dim7(7)       ",              
"          m7-5        ":"    hdim7         ",               
"          m7b5        ":"    hdim7         ",               
"          m11b5       ":"    hdim7(9,11)  ",               
"          m9b5        ":"    hdim7(9)      ",               
"          m7b5b9      ":"    hdim7(b9)     ",               
"          M           ":"    maj           ",               
"                      ":"    maj           ",               
"          MAJ         ":"    maj           ",               
"          omit3add9   ":"    maj(*3,9)     ",               
"          omit3(add9) ":"    maj(*3,9)     ",               
"          5           ":"    maj(*3)       ",               
"          add9        ":"    maj(9)        ",               
"          6           ":"    maj6          ",               
"          M6          ":"    maj6          ",               
"          6(add9)     ":"    maj6(9)       ",               
"          MAJ7        ":"    maj7          ",               
"          maj7        ":"    maj7          ",               
"          M7          ":"    maj7          ",               
"          M7(add13)   ":"    maj7(13)      ",               
"          M7#11       ":"    maj7(s11)     ",               
"          maj9        ":"    maj9          ",               
"          MAJ9        ":"    maj9          ",               
"          M9          ":"    maj9          ",               
"          M9#11       ":"    maj9(s11)     ",               
"          m           ":"    min           ",               
"          m6          ":"    min(6)        ",               
"          m(sus9)     ":"    min(9)        ",               
"          m(add9)     ":"    min(9)        ",               
"          m6(add9)    ":"    min6(9)       ",               
"          m7          ":"    min7          ",               
"          m7(omit5)   ":"    min7(*5)      ",               
"          m7omit5     ":"    min7(*5)      ",               
"          m7(add11)   ":"    min7(11)      ",               
"          m7(add13)   ":"    min7(13)      ",               
"          m7b9#11     ":"    min7(b9,s11)  ",               
"          m7(b9)      ":"    min7(b9)      ",               
"          m7b9        ":"    min7(b9)      ",               
"          m7#9        ":"    min7(s9)      ",               
"          m7(#9)      ":"    min7(s9)      ",               
"          m9          ":"    min9          ",               
"          m9#11       ":"    min9(s11)     ",               
"          min#7       ":"    minmaj7       ",               
"          mM7         ":"    minmaj7       ",               
"          m#7         ":"    minmaj7       ",               
"          m(maj7)     ":"    minmaj7       ",               
"          min(maj7)   ":"    minmaj7       ",               
"          mMAJ7       ":"    minmaj7       ",               
"          m+7         ":"    minmaj7       ",               
"          mM7(add9)   ":"    minmaj7(9)    ",               
"          z           ":"    N             ",               
"          sus         ":"    sus4          ",               
"          sus4        ":"    sus4          ",              
"          13sus       ":"    sus4(b7,9,13) ",              
"          9sus        ":"    sus4(b7,9)    ",              
"          sus9        ":"    sus4(b7,9)    ",              
"          13susb9     ":"    sus4(b7,b9,13)",              
"          7susb9      ":"    sus4(b7,b9)   ",              
"          7sus        ":"    sus4(b7)      ",              
"          7sus4       ":"    sus4(b7)      ",
"          13#9        ":"    (1,3,5,b7,s9,13)",        
"          7b5         ":"    (1,3,b5,b7)     ",        
"          7-5         ":"    (1,3,b5,b7)     ",        
"          11          ":"    (1,5,b7,9,11)   ",        
"          M7b5        ":"    (1,3,b5,7)      ",        
"          9b5         ":"    (1,3,b5,b7,9)   ",        
"          2           ":"    (1,2,5)         ",        
"          13b5        ":"    (1,3,b5,b7,13)  ",        
"          9-5         ":"    (1,3,b5,b7,9)   ",        
"          m+7b9       ":"    (1,b3,s5,b7,b9) ",        
"          m+5         ":"    (1,b3,s5)       ",        
"          m+7#9       ":"    (1,b3,s5,b7,s9) ",        
"          m+7b9#11    ":"    (1,b3,s5,b7,b9,s11)",        
"          (b5)        ":"    (1,3,b5)        ",        
"          M7-5        ":"    (1,3,b5,7)      ",        
"          m#5         ":"    (1,b3,s5)       ",        
"          13#11       ":"    (1,3,5,b7,s11,13)",        
"          m13         ":"    (1,b3,5,b7,13)  ",        
"          M13#11      ":"    (1,3,5,7,s11,13)",        
"          m11         ":"    (1,b3,5,b7,9,11)",        
"          69          ":"    (1,3,5,9,13)    ",        
"          m69         ":"    (1,b3,5,9,13)   ",        
"          MAJ13       ":"    (1,3,5,7,13)    ",        
"          M13         ":"    (1,3,5,7,13)    ",        
"          maj13       ":"    (1,3,5,7,13)    ",        
"          7b5b9       ":"    (1,3,b5,b7,b9)  ",        
"          7alt        ":"    (1,3,b5,b7,b9)  ",        
"          sus2        ":"    (1,2,5)         ",        
"          7sus2       ":"    (1,2,5,b7)      ",        
"          11b9        ":"    (1,3,5,b7,b9,11)",        
"          13          ":"    (1,3,5,b7,13)   ",        
"          7b5#9       ":"    (1,3,b5,b7,s9)  ",        
"          13b9        ":"    (1,3,5,b7,b9,13)"}
chordmap = dict([(k.strip(), v.strip()) for k,v in chordmap.items()])
	
if __name__ == '__main__':

	usage = "%prog [options] infile.mma [outfile.rdf]"
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

	mma2RDF(infilename, outfilename, opts.format, opts.audiofilename, opts.descriptions)
