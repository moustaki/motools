#!/home/c4dm/local/bin/python

lastfmURI = "http://dbtune.org/lastfm/"


import cgi
import cgitb; cgitb.enable()
import urllib
import rdflib

def Main():

	uriQuery = cgi.FieldStorage()                # Get the query string from the URI
	lastfmUser = uriQuery['lastfm'].value
	
	gnatFile = uriQuery['gnat'].file.read()
	print "Content-type: text/html\n\n"


	print len(gnatFile)
	print "<br><br>"

	for line in gnatFile:
		print line

Main()
