#!/usr/bin/env python
# encoding: utf-8
"""
lastfm.py

Created by Kurt Jacobson on 2007-11-14.
Copyright (c) 2008 Centre for Digital Music. All rights reserved.
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

DBTUNE_PREFIX = "http://dbtune.org/artists/last-fm/"
DBTUNE_MBZ = "http://dbtune.org/musicbrainz/resource/artist/"
BBC_PREFIX = "http://www.bbc.co.uk/music/artists/"


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
OWL = rdflib.Namespace("http://www.w3.org/2002/07/owl#")

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg

class LastFMSession:
	'''
	Object for wrapping a last.fm api session
	'''
	def __init__(self, artistname=None):
		self.graph = rdflib.ConjunctiveGraph()
		if artistname != None:
			self.artistname = urllib.unquote(artistname)
		else:
			self.artistname = None
		self.Artist = None
		self.session_key = None
		self.similarArtists = {}
		self.mbid = None

	def authenticate(self):
		'''
		authenticate using this linkedopendata account
		'''
		username = "linkedopendata"
		md5_pwd = pylast.md5("nopassword")
		self.session_key = pylast.SessionKeyGenerator(API_KEY, API_SECRET).get_session_key(username, md5_pwd)
	
	def getMBID(self):
		'''check for an mbid to do a redirect'''
		self.Artist = pylast.Artist(self.artistname, API_KEY, API_SECRET, self.session_key)
		return self.Artist.get_mbid()
	
	def getLastFMdata(self, mbid=None):
		'''
		actually get the artist data
		'''
		
		#if self.Artist == None:
		if self.artistname == None and mbid != None:
			self.Artist = pylast.get_artist_by_mbid(mbid, API_KEY, API_SECRET, self.session_key)
			self.artistname = self.Artist.get_name();
		elif self.artistname != None:
			self.Artist = pylast.Artist(self.artistname, API_KEY, API_SECRET, self.session_key)
		else:
			print "error retrieving artist data - bad name or mbid"
			#sys.exit(2)
		
		# will actually not fail unti here if there's problems	
		try:
			self.similarArtists = self.Artist.get_similar()
		except pylast.ServiceException, msg:
			print "error retrieving artist data - " +str(msg)
			#sys.exit(2)
		
		# do a bunch of getting
#		try:
#			self.bio = self.Artist.get_bio_content()
#		except pylast.ServiceException, msg:
#			print "error retrieving artist data - " +str(msg)
#			
		try:
			self.mbid = self.Artist.get_mbid()
		except:
			print "error retrieving artist data - " +str(msg)
			
#		try:
#			self.Artist.get_image_url(0)
#		except:
#			pass
		
		
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
		self.graph.namespace_manager.bind("owl", rdflib.URIRef("http://www.w3.org/2002/07/owl#"))

		try:
			# try using the mbid first
			aNode = rdflib.URIRef(DBTUNE_PREFIX+"mbid/"+self.mbid)
		except TypeError:
			# use last.fm artist name as backup
			aNode = rdflib.URIRef(DBTUNE_PREFIX+urllib.quote(self.artistname))
		
		lastfm = rdflib.BNode("http://last.fm")
		
		# add the type and name of the main guy
		self.graph.add((aNode, rdflib.RDF.type, MO['MusicArtist']))
		self.graph.add((aNode, FOAF['name'], rdflib.Literal(self.artistname)))
		if self.mbid != None:
			self.graph.add((aNode, MO['musicbrainz'], rdflib.Literal(self.mbid)))
			self.graph.add((aNode, OWL['sameAs'], rdflib.URIRef(BBC_PREFIX+self.mbid)))
			self.graph.add((aNode, OWL['sameAs'], rdflib.URIRef(DBTUNE_MBZ+self.mbid)))
		
		
		
		# create node for each similar artist
		# using nested lists
		#		similarArtists[idx][0] - Artist object
		#		similarArtists[idx][1] - artist musicbrainz id
		#		similarArtists[idx][2] - last.fm match value
		nodeList = [] # a list of artist nodes mo:MusicArtists
		assList = []  # a list of musim:Associations
		for artistinfo in self.similarArtists:
			try:
				if artistinfo[1]:
					nodeList.append(rdflib.URIRef(DBTUNE_PREFIX+"mbid/"+artistinfo[1]))
					assList.append(rdflib.BNode(urllib.quote(str(aNode)+"-ContextSim-"+artistinfo[1])))
				else:
					nodeList.append(rdflib.URIRef(DBTUNE_PREFIX+urllib.quote(str(artistinfo[0]))))#.encode('ascii','replace'))))
					assList.append(rdflib.BNode(urllib.quote(str(aNode)+"-ContextSim-"+urllib.quote(str(artistinfo[0])))))#.encode('ascii','replace')))))
					
			except UnicodeEncodeError:
				# if we just can't encode the artist name at all, use a blank node
				nodeList.append(rdflib.BNode())
				assList.append(rdflib.BNode())
					
		
		for idx, node in enumerate(nodeList):
			# adding similar artists and there names
			# using nested lists
			#		similarArtists[idx][0] - Artist object
			#		similarArtists[idx][1] - artist musicbrainz id
			#		similarArtists[idx][2] - last.fm match value
			self.graph.add((node, rdflib.RDF.type, MO['MusicArtist']))
			self.graph.add((node, FOAF['name'], rdflib.Literal(self.similarArtists[idx][0])))
			if self.similarArtists[idx][1] != None:
				self.graph.add((node, OWL['sameAs'], rdflib.URIRef(BBC_PREFIX+self.similarArtists[idx][1])))
				self.graph.add((node, OWL['sameAs'], rdflib.URIRef(DBTUNE_MBZ+self.similarArtists[idx][1])))
				self.graph.add((node, MO['musicbrainz'], rdflib.Literal(self.similarArtists[idx][1])))
			
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
			
			# let's add mo:similar_to while we're at it
			self.graph.add((aNode, MO['similar_to'], node))
		
		#print self.graph.serialize()
		return self.graph.serialize()
		
def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "hn:m:", ["help", "name=","mbid="])
		except getopt.error, msg:
			raise Usage(msg)
	
		artistname = None
		mbid = None
		# option processing
		for option, value in opts:
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
