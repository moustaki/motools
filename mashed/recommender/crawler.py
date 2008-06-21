#!/usr/bin/env python

from rdflib import Graph,ConjunctiveGraph, Namespace
from rdflib.store import Store
from sys import argv
from rdflib import plugin
#from SPARQLWrapper import SPARQLWrapper
import sys


store = plugin.get('SQLite',Store)('rdfstore')
rt = store.open('db',create=False)
g = Graph(store)
#g.load("brands_artist.n3",format='n3')

#mbz = SPARQLWrapper("http://dbtune.org/musicbrainz/sparql")

PC = Namespace('http://purl.org/ontology/playcount/')
PO = Namespace('http://purl.org/ontology/po/')
MO = Namespace('http://purl.org/ontology/mo/')


seed = argv[1]

#query = """
#PREFIX foaf: <http://xmlns.com/foaf/0.1/>
#PREFIX mo: <http://purl.org/ontology/mo/>
#SELECT ?art WHERE
#{<%s> foaf:maker ?art}
#""" % seed
#print query
#mbz.setQuery(query)
#artists = mbz.query()
#for artist in artists:
#	print artist

try:
	g.load(seed)
except Exception, e :
	print "uri already loaded"

query ="""
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX pc: <http://purl.org/ontology/playcount/>
SELECT ?brand ?count
WHERE {
<%s> foaf:maker ?artist. 
?pc 
	pc:object ?artist;
	pc:count ?count.
?brand pc:playcount ?pc.
}
""" % seed
print query

k=-1
brands =[]
playcounts = []
for row in g.query(query):
	print "brand %s played artist %s times" % row
	k = k+1
	brands.append(row[0])
	playcounts.append(row[1])


for brand in brands:
	print brand
	g.load(brand)
	q = "SELECT ?e WHERE {<%s> <http://purl.org/ontology/po/episode> ?e.}" % brand
	print q
	for e in g.query(q):
		print e
		g.load(e[0])
		q2 = "SELECT ?v WHERE {<%s> <http://purl.org/ontology/po/version> ?v.}" % e
		for v in g.query(q2):
			g.load(v[0])
			q3 = "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT ?start ?dur WHERE {?broadcast <http://purl.org/ontology/po/broadcast_of> <%s>; <http://purl.org/NET/c4dm/event.owl#time> ?time. ?time <http://purl.org/NET/c4dm/timeline.owl#start> ?start; <http://purl.org/NET/c4dm/timeline.owl#duration> ?dur.}" % v
			for row in g.query(q3):
				if row[0].startswith('2008'):
					print "start %s duration %s" % row
	


g.commit()

#print "loading %s" % seed
#g.load(seed)





