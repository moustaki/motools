#!/usr/bin/env python
# encoding: utf-8
"""
myspace2rdf.py

Created by Kurt J on 2008-02-26.
Copyright (c) 2008 Centre for Digital Music Queen Mary U of London. All rights reserved.
"""

import sys
import getopt
from tryurl import *
from myspaceuris import *
from scraping import *
import mopy
from xml.dom import minidom as dom
import unicodedata
#Am making use of regular expressions
import re 
import urllib
from mpsSong import mpsSong


help_message = '''
Python back-end for myspace-to-rdf webservice by Kurt J 2/2008
Usage:
	-i <uid> : --id <the user id number from myspace>
	-u <url> : --url <the url of the myspace page>
	-h : --help print this message
	
	'''


class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg

class BadURL(Exception):
	def __init__(self, msg):
		self.msg = msg

class Scrape(object):
	def __init__(self, uid=""):
		self.uid = uid
		self.mi = mopy.MusicInfo()
		self.playlistID = False
		
	def getPage(self):
		'''just grab the web page'''
		url = viewProfileURLbase + str(self.uid)
		resp = try_open(url)
		if resp==None:
			raise BadURL, 'bad uid'
		self.page = resp.read()
		resp.close()
		
		## start building some mopy objects
		#self.subject = mopy.foaf.Person('http://dbtune.org/myspace/uid/'+str(self.uid))
		#self.name = scrapePage(self.page, [nameTag], '<')
		#self.subject.name.set(self.name)

	def getUserID(self, url):
		'''get the userID from the url of homepage'''
		url = "http://www.myspace.com/"+url
		
		resp = try_open(url)
		if resp == None:
			raise BadURL, 'bad url'
		self.page = resp.read()
		#print self.page
		resp.close()
		self.uid = scrapePage(self.page, [userIDTag[0]], userIDTag[1])
		# print self.uid
		#self.subject = mopy.foaf.Person('http://dbtune.org/myspace/uid/'+str(self.uid))
		#self.name = scrapePage(self.page, [nameTag], '<')
		#self.subject.name.set(self.name)
		
		
	def getFriends(self,artist):
		'''scrape the friends off a page...'''
		if self.page:
			#friendTupleList = scrapePageTuple(self.page, friendDict)
			friendUIDs = scrapePageWhile(self.page, friendTag[0], friendTag[1])
			friendNames = scrapePageWhile(self.page, friendNameTag[0], friendNameTag[1])
			friendPics = scrapePageWhile(self.page, friendPicTag[0], friendPicTag[1])
			
			#print friendUIDs
			print len(friendUIDs)
			print len(friendNames)
			# super kludge to fix this problem
			if len(friendUIDs) > len(friendNames):
				friendUIDs = friendUIDs[1:]
			
			for i in range(len(friendUIDs)):
				currentUID = friendUIDs[i]
				if currentUID.isdigit():
					friend = mopy.foaf.Person(dbtuneMyspace+'uid/' + str(friendUIDs[i]))
				else:
					friend = mopy.foaf.Person(dbtuneMyspace+str(friendUIDs[i]))
				friend.name.set(friendNames[i])
				try:
					img = mopy.foaf.Image(friendPics[i])
					friend.depiction.add(img)
				except:
					pass

				#if artist==False:
				#	self.subject.knows.add(friend)
				
				# self.subject.knows.add(friend)
				# since when did this happen??? mopy wont take foaf:knows as a prop of mo:MusicArtist
				
				self.subject.topFriend.add(friend)
				self.mi.add(friend)
				
		else:
			print "error! no page..."
			
	def isArtist(self):
		'''is current page an artist???
				- previously checked for the flash player
				- new check for genre tags instead'''
		
		if self.page:
			genrePresent = scrapePage(self.page, [genreTag[0]], genreTag[1])
			if genrePresent:
				self.subject = mopy.mo.MusicArtist(dbtuneMyspace+'uid/'+str(self.uid))
				# add foaf:primaryTopic
				ppd = mopy.foaf.PersonalProfileDocument("")
				ppd.primaryTopic.set(self.subject)
				self.mi.add(ppd)
				# assuming the 'name' tag must be present, if not it's a bad url
				self.name = scrapePage(self.page, [nameTag[0]], nameTag[1])
				if self.name:
					self.subject.name.set(self.name)
				else:
					print "seems to be an invalid url, try using the UID or the clean url"
				return True
			else:
				#self.subject = mopy.mo.Agent('http://dbtune.org/myspace/uid/'+str(self.uid))
				self.subject = mopy.foaf.Person(dbtuneMyspace+'uid/'+str(self.uid))
				# add foaf:primaryTopic
				ppd = mopy.foaf.PersonalProfileDocument("")
				ppd.primaryTopic.set(self.subject)
				self.mi.add(ppd)
				self.name = scrapePage(self.page, [nameTag[0]], nameTag[1])
				#print self.name
				if self.name:
					self.subject.name.set(self.name)
				else:
					print "seems to be an invalid url, try using the UID or the clean url"
				return False
		else:
			print "error - no page loaded..."
			
		
	def createArtistRDF(self):
		'''write RDF for an artist page'''		
		if self.scrapeArtistID() and self.scrapePlaylistNumber():
			pass
		else:
			print 'scrape failed'
		
		# get the image
		imageURL = scrapePage(self.page, [picTag[0]+str(self.uid)+'''"><img src="'''], picTag[1])
		img = mopy.foaf.Image(imageURL)
		self.subject.depiction.add(img)
		self.mi.add(img)
		
		# get the alternative url for page
		niceURL = scrapePage(self.page, [niceURLTag[0]], niceURLTag[1])
		if niceURL:
			niceURL = niceURL.rsplit('http://www.myspace.com/')[1]
			thing = mopy.owl.Thing('http://dbtune.org/myspace/'+niceURL)
			# thing2 = mopy.owl.Thing('http://dbtune.org/myspace/'+self.uid)
			self.subject.sameAs.set(thing)
			self.mi.add(thing)
			# self.subject.sameAs.set(thing2)
			# self.mi.add(thing2)
			
		if self.playlistID and self.artistID and self.uid:
			xmlPage = try_open(mediaBase[0] + str(self.artistID) + mediaBase[1] + str(self.playlistID) + mediaBase[2] + str(self.uid) + mediaBase[3])
			#print mediaBase[0] + str(self.artistID) + mediaBase[1] + str(self.playlistID) + mediaBase[2] + str(self.uid) + mediaBase[3]
		
			if xmlPage:
				self.xmlStruct = dom.parseString(''.join(xmlPage.readlines()))
				songList = self.xmlStruct.getElementsByTagName('song')
				for song in songList:
					# using ben's mpsSong class
					thisSong = mpsSong(self, song, 'downloadprefix')
					thisSong.getUri()
				
					track = mopy.mo.Track()
					track.title.set(thisSong.title)
					availableAs = thisSong.uri
					if availableAs:
						avas = mopy.mo.MusicalItem(availableAs)
						track.available_as.set(avas)
						self.mi.add(avas)
					self.subject.made.add(track)
					self.mi.add(track)
				
		
		self.createCommonRDF()
		self.scrapeGenre()
		self.mi.add(self.subject)
		graph = mopy.exportRDFGraph(self.mi)
		return graph.serialize()

	def scrapeArtistID(self):
		'''attempt to find via scrape of page the internal artist number.'''
		try:
			ids = scrapePageWhile(self.page, artistIDtag[0], artistIDtag[1])
			for i in ids:
				if i.isdigit():
					self.artistID = i
			# self.artistID = scrapePage(self.page, [artistIDtag[0]], artistIDtag[1])
			return True
		except Exception, err:
			print "Ran into trouble trying to scrape the ArtistID for page from " + self.source  + "\nError::" + str(err)
			return False
			
	def scrapePlaylistNumber(self):
		"""attempts to find via scrape of the internal identifier of an artist's playlist of songs"""
		try:
			# make sure we get a digit and not some crap - maybe should to regex
			ids = scrapePageWhile(self.page, playlistIDtag[0], playlistIDtag[1])
			for i in ids:
				if i.isdigit():
					self.playlistID = i
			#self.playlistID = scrapePage(self.page, [playlistIDtag[0]], playlistIDtag[1])
			return True
		except Exception, err:
			print "Ran into trouble trying to scrape the playlistID for page from " + self.source  + "\nError::" + str(err)
			return False
	
	
	def createRDF(self):
		'''write the info to RDF for non-artist page'''
		match = re.findall('viewAlbums&amp;friendID='+str(self.uid)+'">\s*<img border="\d*" alt="[^"]*" src="([^"]*?)"', str(self.page))
		if match:
			img = mopy.foaf.Image(match[0])
			self.subject.depiction.set(img)
			self.mi.add(img)
		#The previous method of depiction finding didnt work for user pages, added regex (sorry, I am not a fan of string matching)
		#imageURL = scrapePage(self.page, [picTag[0]+str(self.uid)+'''<img border="0" alt="" src="'''], picTag[1])

		niceURL = scrapePage(self.page, [niceURLTag[0]], niceURLTag[1])
		if niceURL:
			niceURL = niceURL.rsplit('http://www.myspace.com/')[1]
			thing = mopy.owl.Thing(dbtuneMyspace+niceURL)
			self.subject.sameAs.set(thing)
			self.mi.add(thing)
			
		#thing2 = mopy.owl.Thing('http://dbtune.org/myspace/uid/'+self.uid)
		#self.subject.sameAs.set(thing2)
		#self.mi.add(thing2)
		
		self.createCommonRDF()
		self.mi.add(self.subject)
		print self.mi
		graph = mopy.exportRDFGraph(self.mi)
		return graph.serialize()


	def createCommonRDF(self):
		'''write the common info which can be found on both Artist and User pages'''
		#Adds a bnode containing OnlineAccount information
		account = mopy.foaf.OnlineAccount()
		account.name.set("Myspace")
		doc = mopy.foaf.Document("http://www.myspace.com/")
		account.accountServiceHomepage.set(doc)
		account.accountName.set(self.uid)
		self.subject.holdsAccount.set(account)	
		self.mi.add(account)
		#Regexing for further information pertaining to the myspace user/artist
		#Find gender look for gender information in the title
		match = re.findall('- (Male|Female) -',str(self.page))
		if match:
			if match[0]=='Male':
				self.subject.gender.set("male")
			elif match[0]=='Female':
				self.subject.gender.set("female")
		#Get age
		match = re.findall('>(\d+?) years old',str(self.page))
		if match: 
			self.subject.age.set(match[0])

	
	def scrapeGenre(self):
		'''genreraw = scrapePage(self.page, [genreTag[0]], genreTag[1])
		if genreraw == None:
			return genreraw
		genreraw = str(genreraw).lstrip()
		genreraw = genreraw.rstrip()
		genres = genreraw.split('/')
		genresfixed = []
		for genre in genres:
			genre = genre.rstrip()
			genre = genre.lstrip()
			g = mopy.mo.Genre(myspaceOntology+urllib.quote(str(genre)))
			g.name.set(genre)
			self.mi.add(g)
			self.subject.genreTag.add(g)
			genresfixed.append(genre)
		return genresfixed'''
		localGenres = scrapePage(self.page, [genreTag[0]], genreTag[1])
		if localGenres == None:
			return None
		genreNums = re.findall(''':"(.|..|...)"''', localGenres) # should return only 2 or 3 char string between 
		genres = []
		for gnum in genreNums:
			try:
				genre = mopy.mo.Genre(myspaceOntology+urllib.quote(genreDict[int(gnum)]))
			except KeyError:
				pass
			else:
				genre.name.set(genreDict[int(gnum)])
				self.mi.add(genre)
				self.subject.genreTag.add(genre)
				genres.append(genre)

		return genres
		
		




def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "ho:vi:u:", ["help", "output=", "id=", "url="])
		except getopt.error, msg:
			raise Usage(msg)
	
		# option processing
		for option, value in opts:
			if option == "-v":
				verbose = True
			if option in ("-i", "--id"):
				s = Scrape(value)
				try:
					s.getPage()
				except BadURL:
					print "invalid user id or problems w/ myspace server. if you are sure the id is correct, try again in a few seconds..."
					sys.exit(2)
			if option in ("-u", "--url"):
				s = Scrape()
				try:
					s.getUserID(value)
				except BadURL:
					print "invalid myspace url or problems w/ myspace server. if you are sure the url is correct, try again in a few seconds..."
					sys.exit(2)
			if option in ("-h", "--help"):
				raise Usage(help_message)
			if option in ("-o", "--output"):
				output = value
			
			
			artist = s.isArtist()
			s.getFriends(artist)
			
			if artist:
				s.createArtistRDF()
			else:
				s.createRDF()
	
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2


if __name__ == "__main__":
	sys.exit(main())
