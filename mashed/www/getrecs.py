#!/home/c4dm/local/bin/python

lastfmURI = "http://dbtune.org/lastfm/"


import cgi
import urllib
import rdflib

def Main():

	uriQuery = cgi.FieldStorage()                # Get the query string from the URI
	lastfm = uriQuery['lastfm'].value
	lasttype = uriQuery['lastfm'].type
	gnat = uriQuery['gnat'].value #.getfirst('gnat','')
	gnat2 = uriQuery['gnat'].type
	#lines = gnat.open()#.readlines()
	print "Content-type: text/html\n\n"
	
	print lastfm+ str(lasttype)+"<br>"

	print "getfirst " + str(gnat) + "<br>"
	print ".type: " + str(gnat2) +"<br>"
	print dir(gnat)
	#for line in lines:
		#print line

Main()
