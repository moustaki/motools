#!/home/c4dm/local/bin/python

lastfmURI = "http://dbtune.org/last-fm/"


import cgi
import cgitb; cgitb.enable()
import urllib
import mopy
import crawler
import threading
import brand_recommender

class callCrawl(threading.Thread):
	#broadcastsLock = threading.Lock()
	def __init__(self, track):
		self.track = track
		threading.Thread.__init__(self)
	def run(self):
		crawler.find(self.track)

def Main():

	uriQuery = cgi.FieldStorage()                # Get the query string from the URI
	if uriQuery.has_key('lastfm') or uriQuery.has_key('gnat'):
		if uriQuery.has_key('lastfm'):
			lastfmUser = uriQuery['lastfm'].value
			# mopy can't handle the last-fm service
			# lastfmRDF = mopy.importRDFFile(lastfmURI+lastfmUser)




		if uriQuery.has_key('gnat'):
			gnatFile = uriQuery['gnat'].file.read()
			print "Content-type: text/html\n\n"
			f = open('temp.rdf', 'w')
			for char in gnatFile:
				f.write(char)

			f.close()
			try:
				rdf = mopy.importRDFFile('temp.rdf')
				tracks = rdf.TrackIdx.keys()
				op = []
			except:
				print "bad file, maybe not a GNAT output..."
				return
			#try:
			for track in tracks:
				#t = callCrawl(track)
				#t.start()
				#crawler.find(track)
				brand_recommender.find(track)
			#except:
			#	print "threading problem"
			#	return
				#print op
			
			print "gnat tracks: <br>"
			print tracks
			print op
	else:
		print "must submit an RDF file"

Main()
