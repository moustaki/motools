#!/usr/bin/env python

from rdflib import ConjunctiveGraph, Namespace
from sys import argv
#from SPARQLWrapper import SPARQLWrapper
import sys

PC = Namespace('http://purl.org/ontology/playcount/')
PO = Namespace('http://purl.org/ontology/po/')
MO = Namespace('http://purl.org/ontology/mo/')

g = ConjunctiveGraph()
g.load("brands_artist.n3",format='n3')

#mbz = SPARQLWrapper("http://dbtune.org/musicbrainz/sparql")

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

g.load(seed)

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

for row in g.query(query):
	print "brand %s played artist %s times" % row



#print "loading %s" % seed
#g.load(seed)





