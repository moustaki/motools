#!/usr/bin/env python
# encoding: utf-8
"""
lastfm.py

Created by Kurt Jacobson on 2007-11-14.
Copyright (c) 2007 __MyCompanyName__. All rights reserved.
"""
import urllib

import sys
import getopt
try:
	import pylast
except:
	print "pylast not installed... exiting..."
	sys.exit(2)
	
try:
	import rdflib
except:
	print "rdflib not installed... exiting..."
	sys.exit(2)

API_KEY = "908f1a693236e128cc35fef9b6e4d8de"
API_SECRET = "f9a797118e9d34878f174cc39d354866"

DBTUNE_PREFIX = "http://dbtune.org/last-fm/artists/"

help_message = '''
	$ python artistlookup.py [flags]
			-n		: 		last.fm artist name (use quotes around name)
			-m		:		musicbrainz id of artist
			please use just one or the other!!!
'''

# set namespaces globally?
FOAF = rdflib.Namespace("http://xmlns.com/foaf/0.1/")
MO = rdflib.Namespace("http://purl.org/ontology/mo/")
MUSIM = rdflib.Namespace("http://purl.org/ontology/musim#")
DC = rdflib.Namespace("http://purl.org/dc/elements/1.1/")

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg

class LastFMSession:
	'''
	Object for wrapping a last.fm api session
	'''
	def __init__(self, artistname=None):
		self.graph = rdflib.ConjunctiveGraph()
		self.artistname = artistname
		self.Artist = None
		self.session_key = None
		self.similarArtists = {}

	def authenticate(self):
		'''
		authenticate using this linkedopendata account
		'''
		username = "linkedopendata"
		md5_pwd = pylast.md5("nopassword")
		self.session_key = pylast.SessionKeyGenerator(API_KEY, API_SECRET).get_session_key(username, md5_pwd)
	
	def getLastFMdata(self, mbid=None):
		'''
		actually get the artist data
		'''
		if self.artistname == None and mbid != None:
			self.Artist = pylast.get_artist_by_mbid(mbid, API_KEY, API_SECRET, self.session_key)
			self.artistname = self.Artist.get_name();
		elif self.artistname != None:
			self.Artist = pylast.Artist(self.artistname, API_KEY, API_SECRET, self.session_key)
		else:
			print "error retrieving artist data - bad name or mbid"
			sys.exit(2)
		
		# will actually not fail unti here if there's problems	
		try:
			self.similarArtists = self.Artist.get_similar()
		except pylast.ServiceException, msg:
			print "error retrieving artist data - " +str(msg)
			sys.exit(2)
		
		# do a bunch of getting
		self.bio = self.Artist.get_bio_content()
		self.bio_summary = self.Artist.get_bio_summary()
		self.image_url = self.Artist.get_image_url()
		self.mbid = self.Artist.get_mbid()
		
	def createRDFGraph(self):
		'''
		actually build the RDF graph
		'''
		
		
		if not self.Artist:
			print "error, need to call getLstFMData() first"
			return
		
		# lets make pretty namespaces
		self.graph.namespace_manager.bind("mo", rdflib.URIRef("http://purl.org/ontology/mo/"))
		self.graph.namespace_manager.bind("foaf", rdflib.URIRef("http://xmlns.com/foaf/0.1/"))
		self.graph.namespace_manager.bind("musim", rdflib.URIRef("http://purl.org/ontology/musim#"))
		self.graph.namespace_manager.bind("dc", rdflib.URIRef("http://purl.org/dc/elements/1.1/"))

		try:
			aNode = rdflib.BNode(DBTUNE_PREFIX+"mbid/"+self.mbid)
		except TypeError:
			aNode = rdflib.BNode(DBTUNE_PREFIX+urllib.quote(self.artistname))
			
		
		lastfm = rdflib.BNode("http://last.fm")
		
		# add the type and name of the main guy
		self.graph.add((aNode, rdflib.RDF.type, MO['MusicArtist']))
		self.graph.add((aNode, FOAF['name'], rdflib.Literal(self.artistname)))
		
		
		
		# creat node for each similar artist
		#keys = self.similarArtists.keys()
		nodeList = []
		assList = []
		for artistinfo in self.similarArtists:
			try:
				if artistinfo[1]:
					nodeList.append(rdflib.BNode(DBTUNE_PREFIX+"mbid/"+artistinfo[1]))
					assList.append(rdflib.BNode(urllib.quote(str(aNode)+"-ContextSim-"+artistinfo[1])))
				else:
					nodeList.append(rdflib.BNode(DBTUNE_PREFIX+urllib.quote(str(artistinfo[0]).encode('ascii','replace'))))
					assList.append(rdflib.BNode(urllib.quote(str(aNode)+"-ContextSim-"+urllib.quote(str(artistinfo[0]).encode('ascii','replace')))))
					
			except UnicodeEncodeError:
				nodeList.append(rdflib.BNode())
				assList.append(rdflib.BNode())
					
		
		for idx, node in enumerate(nodeList):
			# adding similar artists and there names
			self.graph.add((node, rdflib.RDF.type, MO['MusicArtist']))
			self.graph.add((node, FOAF['name'], rdflib.Literal(self.similarArtists[idx][0])))
			
			# from artist nodes to similarity
			self.graph.add((node, MUSIM['object_of'], assList[idx]))
			self.graph.add((aNode, MUSIM['subject_of'], assList[idx]))
			
			# create the contextsimilarity object and add subs/obs
			self.graph.add((assList[idx], rdflib.RDF.type, MUSIM['ContextualSimilarity']))
			self.graph.add((assList[idx], MUSIM['has_subject'], aNode))
			self.graph.add((assList[idx], MUSIM['has_object'], node))
			self.graph.add((assList[idx], MUSIM['weight'], rdflib.Literal(self.similarArtists[idx][2])))
			
			# add this is made by last.fm
			self.graph.add((assList[idx], DC['creator'], lastfm))
		
		print self.graph.serialize()
		
def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "hvn:m:", ["help", "name=","mbid="])
		except getopt.error, msg:
			raise Usage(msg)
	
		artistname = None
		mbid = None
		# option processing
		for option, value in opts:
			if option == "-v":
				verbose = True
			if option in ("-h", "--help"):
				raise Usage(help_message)
			if option in ("-n", "--name"):
				artistname = value
			if option in ("-m", "--mbid"):
				mbid = value
				
		if mbid != None and artistname != None:
			raise Usage("please use just one or the other")
	
		if artistname != None:
			l = LastFMSession(urllib.unquote(artistname))
			l.authenticate()
			l.getLastFMdata()
			l.createRDFGraph()
		elif mbid != None:
			l = LastFMSession()
			l.authenticate()
			l.getLastFMdata(mbid)
			l.createRDFGraph()
		else:
			raise Usage("must supply name or mbid!!!")
	
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2


if __name__ == "__main__":
	sys.exit(main())
