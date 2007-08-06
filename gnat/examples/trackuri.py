#!/usr/bin/python2.4

#
# Just a small python script to get a URI for a track 
# (looking up using ID3 metadata, no fingerprinting yet)
#
# TODO: output as RDF
#
# Yves Raimond, C4DM, Queen Mary, University of London
# yves.raimond (at) elec.qmul.ac.uk
#

import sys
import os
import os.path

sys.path.append(os.path.abspath("")+"/../src/gnat/")

print sys.path

from MbzURIConverter import *
from MbzTrackLookup import *
from RdfHub import *
from Id3Writer import *



def usage() :
        print
        print 'Usage:'
        print 'python trackuri.py <path of track> ([xml|n3])'
	print
        print ' - NOTE: without specified RDF format, the program will'
	print '   write in the Id3v2 UFID header the URI of the '
	print '   corresponding manifestation'
	print
        sys.exit()

if len(sys.argv)!=2 and len(sys.argv)!=3 : 
	usage()

elif len(sys.argv)==2 :
	try :
		lookup = MbzTrackLookup(sys.argv[1])
		mbzuri = lookup.getMbzTrackURI()
		mbzconvert = MbzURIConverter(mbzuri)

		print
		print ' - ID3 tags'
		print
		print 'Artist: ', lookup.artist
		print 'Title: ', lookup.title
		print 'Album: ', lookup.album
		print

		print 
		print ' - Zitgist URI'
		print
		print mbzconvert.getURI()
		print
		
		mbzconvert = MbzURIConverter(mbzuri,'http://musicbrainz.org/')

		print
		print ' - Musicbrainz URI'
		print
		print mbzuri
		print

		id3w = Id3Writer(sys.argv[1])
		id3w.writeUri(mbzconvert.getURI())

	except MbzLookupException, e :
		print
		print ' - Failed'
		print e.message
		print

elif len(sys.argv)==3 :
	try :
		type = sys.argv[2]
	
		lookup = MbzTrackLookup(sys.argv[1])
		mbzuri = lookup.getMbzTrackURI()
		mbzconvert = MbzURIConverter(mbzuri)
	
		rdf = RdfHub()
		rdf.addAvailableAs(mbzconvert.getURI(),'')
		print rdf.getSerializedGraph(type)
	
	except MbzLookupException, e :
		print
		print ' - Failed'
		print e.message
		print
