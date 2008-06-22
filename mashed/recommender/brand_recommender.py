#!/usr/bin/env python

from rdflib import Graph,ConjunctiveGraph, Namespace
from rdflib.store import Store
from sys import argv
from rdflib import plugin
#from SPARQLWrapper import SPARQLWrapper
import sys
import operator

store = plugin.get('SQLite',Store)('rdfstore')
rt = store.open('db',create=False)
g = Graph(store)
#g.load("brands_artist.n3",format='n3')

broadcasts = []

#mbz = SPARQLWrapper("http://dbtune.org/musicbrainz/sparql")

PC = Namespace('http://purl.org/ontology/playcount/')
PO = Namespace('http://purl.org/ontology/po/')
MO = Namespace('http://purl.org/ontology/mo/')

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

def find(seed,service=None):
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
} ORDER BY DESC(?pc)
	""" % seed
	#print query

	k=-1
	brands =[]
	playcounts = []
	for row in g.query(query):
		k = k+1
		t = int(row[1])
		brands.append((row[0],t))
	brands.sort(key=operator.itemgetter(1))
	brands.reverse()
	for (brand,pc) in brands:
		g.load(fix_uri(brand))
		g.commit()
		q = "SELECT ?e ?s WHERE {<%s> <http://purl.org/dc/elements/1.1/title> ?e; <http://purl.org/ontology/po/short_synopsis> ?s } " % brand
		for row in g.query(q):
			print "---"
			print "Brand:"
			print "%s" % row[0]
			print "Synopsis:"
			print "%s" % row[1]
		#print q

#print "loading %s" % seed
#g.load(seed)

def check_date(date):
	#print date
	ds = date.split('-')
	return ds[0]=='2008' and (ds[1]=='05' or ds[1]=='06')

def parse_service(uri):
	return (uri.split("http://bbc-programmes.dyndns.org/"))[1]

def create_content_url(start, duration, service):
	b = start.split('+')[0]
	s = int((start.split('+')[1]).split(':')[0])
	ns = int((b.split(':')[0]).split('T')[1]) + s
	if s<10:
		ns = '0'+str(s)
	else:
		ns = str(s)
	start = (b.split(':')[0]).split('T')[0]+'T'+ns+':'+b.split(':')[1]+':'+b.split(':')[2]+'Z'
	#print start
	return "http://10.88.88.88/archives/"+service+"_"+start+"_"+duration+".mp2"

def fix_uri(uri):
	return uri.split('#')[0]+".rdf"

def print_html():
	for b in broadcasts:
		print "<a href=\"%s\">broadcast</a>"

#find(argv[1])
