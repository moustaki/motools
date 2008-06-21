#!/home/c4dm/local/bin/python

lastfmURI = "http://dbtune.org/lastfm/"


import cgi
import cgitb; cgitb.enable()
import urllib
import mopy

def Main():

	uriQuery = cgi.FieldStorage()                # Get the query string from the URI
	lastfmUser = uriQuery['lastfm'].value
	
	gnatFile = uriQuery['gnat'].file.read()
	print "Content-type: text/html\n\n"
	f = open('temp.rdf', 'w')


	print "tracks: "
	print "<br><br>"

	for char in gnatFile:
		f.write(char)
		#print char

	f.close()
	rdf = mopy.importRDFFile('temp.rdf')
	tracks = rdf.TrackIdx.keys()
	print tracks

Main()
