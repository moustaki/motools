#!/home/c4dm/local/bin/python

import cgi
import urllib

def Main():

	uriQuery = cgi.FieldStorage()                # Get the query string from the URI
	lastfm = uriQuery.getfirst('lastfm','')
	#gnat = uriQuery.getfirst('gnat','')
	print "Content-type: text/html\n\n"
	
	print lastfm
	#print gnat

Main()
