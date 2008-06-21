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

for row in g.query(query):
	print "brand %s played artist %s times" % row

g.commit()

#print "loading %s" % seed
#g.load(seed)





