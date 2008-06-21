#!/home/c4dm/local/bin/python

lastfmURI = "http://dbtune.org/lastfm/"


import cgi
import urllib
import rdflib

def Main():

	uriQuery = cgi.FieldStorage()                # Get the query string from the URI
	lastfm = uriQuery.getfirst('lastfm','')
	gnat = uriQuery.getfirst('gnat','')
	print "Content-type: text/html\n\n"
	
	print lastfm
	print gnat

Main()
