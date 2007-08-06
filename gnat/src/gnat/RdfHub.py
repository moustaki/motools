import rdflib
from rdflib import ConjunctiveGraph,Graph
from rdflib import Literal,Namespace,URIRef
import inspect
import logging
import MySQLdb
import sys
from logging import log, error, warning, info, debug

"""
  Just a small wrapper for RDFLib
"""

class RdfHub :

	def __init__(self, contextName="UNSET") :
		self.MO = Namespace('http://purl.org/ontology/mo/')
		self.DC = Namespace("http://purl.org/dc/elements/1.1/")
		self.OWL= Namespace("http://www.w3.org/2002/07/owl#")
		self.AC = Namespace("http://temp.tmp/AudioCollection/")
		self.contextName = contextName
		idname = 'db'
		db = 'triplestore'
		usr = 'rdflib'
		pwd = 'gRaCiOuS'
		hst = 'localhost'
		cfgstr = "db=%s,user=%s,password=%s,host=%s" % (db,usr,pwd,hst)
		dbstore = rdflib.plugin.get('MySQL', rdflib.store.Store)(idname)
		try:
			dbstore.open(cfgstr, False) # Try opening existing
			debug("Opened existing MySQL DB")
		except Exception, e:
			pass
			try:
				dbstore.open(cfgstr, True) # Otherwise create new
				debug("Created new MySQL DB")
			except Exception, e:
				error("Exception opening MySQL DB" + str(e))
				sys.exit(1)
		
		self.graph = ConjunctiveGraph(dbstore)
		self.graph.commit()
	
	#
	# High-level mutators
	#
	
	def addAvailableAs(self,manifestation,item) :
		self.addNamed((URIRef(manifestation),self.MO['availableAs'],URIRef(item)))
	
	def addSameAs(self, thing_one, thing_two):
		self.addNamed((URIRef(thing_one), self.OWL['sameAs'], URIRef(thing_two)))

	def addItemType(self, item):
		self.addNamed((URIRef(item),rdflib.RDF.type, self.MO['Stream']))
	
	def addTrackType(self, manifestation):
		self.addNamed((URIRef(manifestation), rdflib.RDF.type, self.MO['Track']))

	def addPUID(self, item, PUID):
		self.addNamed((URIRef(item), self.AC["PUID"], Literal(PUID)))

	# Add metadata literals to an item :
	def addTitleL(self, item, title):
		self.addNamed((URIRef(item), self.DC['title'], Literal(title)))
		
	def addArtistL(self, item, artist):
		self.addNamed((URIRef(item), self.DC['creator'], Literal(artist)))
		
	def addGenreL(self, item, genre):
		self.addNamed((URIRef(item), self.MO['Genre'], Literal(genre)))
		
	def addYearL(self, item, year):
		self.addNamed((URIRef(item), self.AC['releaseYear'], Literal(year)))

	
	#
	# High-level Accessors
	#
	
	def getSerializedGraph(self,type='xml') :
		return self.graph.serialize(format=type)

	def getSubjURIsWithBase(self, base,	contextName=""):
		"""Returns a generator of URIs which appear as the subject in the graph 
		   with given context name (defaults to RdfHub's set context)"""
		if contextName=="":
			contextName = self.contextName
		return (str(s) for s,p,o,graph in self.graph.quads((None,None,None)) \
						   if ( (graph.identifier == URIRef(contextName))\
						      & (str(s).startswith(base))\
						      )
				)

	def have_URI(self,filename,contextName=""):
		"""Check if we already know about an associated URI. Pass contextName=None to check all contexts."""
		if contextName=="":
			contextName = self.contextName
		fileURI = URIRef("file://"+filename)
		quads = [(s,p,o) for s,p,o,graph \
						in self.graph.quads((None,self.MO["availableAs"], fileURI)) \
						if contextName==None or graph.identifier == URIRef(contextName) \
				]
		return (len(quads) > 0)

	def haveMD_URI(self,filename):
		"""Check if we already know a metadata-derived URI for this filename."""
		return self.have_URI(filename,"batch_gnat")



	#
	# Locking - fairly shoddy approach, but there's not much harm done if two processes acquire the same lock 
	#

	def lock(self, item, contextName=""):
		if contextName=="":
			contextName = self.contextName
		locks = [(s,p,o) for s,p,o,graph \
						 in self.graph.quads((URIRef(item), self.AC['lock'], Literal("lock"))) \
						 if graph.identifier == URIRef(contextName) \
				]
		if (len(locks) == 0):
			#debug("<lock>")
			self.addNamed((URIRef(item), self.AC['lock'], Literal("lock")), contextName)
			self.commit()
			return True
		else:
			debug("<lock already taken>")
			return False

	def unlock(self, item, contextName=""):
		if contextName=="":
			contextName = self.contextName
		self.removeNamed((URIRef(item), self.AC['lock'], Literal("lock")), contextName)
		self.commit()

	def dropAllLocks(self, contextName=""):
		"""Drop all locks in the named context. Defaults to RdfHub's set context.
		   To drop all locks across all contexts, pass contextName=None."""
		if contextName == "":
			contextName = self.contextName
		if contextName == None:
			self.graph.remove((None, self.AC['lock'], Literal("lock")))
		else:
			self.removeNamed((None, self.AC['lock'], Literal("lock")), contextName)
		self.commit()


	#
	# Low-level ops
	#

	def addNamed(self, triple, contextName=""):
		"""Adds the given triple to our graph, tagging with 
		   the specified context name (defaults to caller's method name)."""
		if contextName=="":
			contextName = self.contextName
		self.graph.addN([triple+(URIRef(contextName),)])
		#debug(list(self.graph.quads((None,None,None))))
	
	def removeNamed(self, triple, contextName=""):
		"""Removes the given triple from the graph with 
		   the specified context name (defaults to caller's method name)"""
		if contextName=="":
			contextName = self.contextName
		namedGraphs = [ graph for graph in list(self.graph.contexts()) \
										if graph.identifier == URIRef(contextName) \
					  ]
		for ng in namedGraphs:
			try:
				ng.remove(triple)
			except MySQLdb.OperationalError, e:
				pass

	def commit(self):
		self.graph.commit()
		
	def setContext(self, contextName):
		self.contextName = contextName

