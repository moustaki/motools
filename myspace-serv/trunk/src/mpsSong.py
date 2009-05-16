#!/usr/bin/env python
# encoding: utf-8
'''
mpsSong.py - for handling myspace songs

by Ben Fields
'''

from xml.dom import minidom as dom
import unicodedata
from tryurl import *
from myspaceuris import *

class mpsSong:
	"""a class that wraps around the downloading, feature extracting and modeling of a piece of media attached to a mpsUser
	mpsSong object instances have the following public variables:
		parent           --     a weakref to the mpsUser that generated the mpsSong instance
        uri              --     lo res cached download link
        betterUri        --     hi res cached download link (not always available)
        downloadprefix   --     local prefix to stick the file when downloaded
        extractionprefix --     local prefix to stick the feature files when extracted
        title            --     title of song
        image            --     url to get image associated with song
        playcount        --     number of times song has been played via myspace player
        trackNum         --     track number based on order presented on myspace
        totalTracks      --     number of songs available for parent
        filename         --     name used for local lofi file, when downloaded
        HIFIfilename     --     name used for local hifi file, when downloaded
        beats            --     local name of beat segmentaton file, used to do variable segment length feature extraction

	"""
	def __init__(self, parent, xmlNode, downloadprefix = '', extractionprefix = ''):
		"""initializes the mpsSong class.  Parent is a pointer to the calling mpsUser, xmlNode should be a DOM object with the songs info.  downloadprefix is the local directory prefix where the media will be put, default is an empty string.  If no extractionprefix is given, extracted features will be places in the dir pointed to by downloadprefix"""
		#self.parent = weakref.ref(parent)
		self.xmlNode = xmlNode
		self.getUri()
		#the nicer file download is currently broken...
		#self.betterURI = xmlNode.getAttribute('downloadable')
		self.downloadprefix = downloadprefix
		if extractionprefix == '':
			self.extractionprefix = downloadprefix
		else:
			self.extractionprefix = extractionprefix
		self.title = self.exhaustiveXML.getElementsByTagName('title')[0].firstChild.nodeValue
		self.image = self.exhaustiveXML.getElementsByTagName('small')[0].firstChild.nodeValue
		self.playcount = xmlNode.getElementsByTagName('stats')[0].getAttribute('plays')
		self.comments = "" #this is a blank string hold for the comments fields.  Might be used later.
		self.trackNum, self.totalTracks = None, None
		self.filename, self.HIFIfilename = None, None
		self.beats = None

	def getUri(self):
		self.songID = self.xmlNode.getAttribute('songId')
		xmlPage = try_open(songBase[0] + str(self.songID) + songBase[1])
		self.exhaustiveXML = dom.parseString(''.join(xmlPage.readlines()))
		xmlPage.close()
		try:
			self.uri = self.exhaustiveXML.getElementsByTagName('link')[0].firstChild.nodeValue
		except AttributeError, err:
			#logging.info("mpsUser::getUri ran into a problem finding the download link for a song by artist with uid: " + 
			#	str(self.parent().uid) + " link will be left blank.\n\tError msg: " + str(err))
			self.uri = ''

	def setTrackNum(self, trackNumber, totalTracks):
		'''set the track number for this song and the number of tracks in the album it is in.'''
		self.trackNum = trackNumber
		self.totalTracks = totalTracks

	def download(self):
		'''download the track.  
		Upon success set self.filename to the local location of the downloaded song and return true.  
		On FAIL return false.'''
		logging.debug("downloading " + self.title + " by " + self.parent().artist +  " to " + self.downloadprefix)
		if self.trackNum != None:
			filename = unicode(str(self.trackNum), 'utf8')  + u'_' +  self.title + u'.mp3'
		else:
			filename =   self.title + u'.mp3'
		if try_get(self.uri, os.path.join(self.downloadprefix, filename)) != None:
			logging.debug("success on " +  self.title + " by " + self.parent().artist +  " to " + os.path.join(self.downloadprefix,filename))
			self.filename = filename
			return True
		else:
			logging.debug("FAIL on " + self.title + " by " + self.parent().artist +  " to " + os.path.join(self.downloadprefix,filename))
			return False

	def downloadHIFI(self):
		'''if it exists, download the hi fidelity version of the track.  
		Upon success set self.HIFIfilename to the local location of the downloaded song and return true.  
		On FAIL return false.'''
		if not self.betterURI:
			logging.info("NO hi-fi version of " + self.title + " by " + self.parent().artist + " but we did look for it.")
			return False
		logging.debug("downloading hifi copy of " + self.title + "by" + self.parent().artist +  " to " + self.downloadprefix)
		if self.trackNum != None:
			filename = unicode(str(self.trackNum), 'utf8') + u'_' + self.title + u'_hifi.mp3'
		else:
			filename =  self.title + u'_hifi.mp3'
		if (try_get(self.betteruri, os.path.join(self.downloadprefix,filename)) != None):
			logging.debug("success on hi-fi version of " + self.title + " by " + self.parent().artist +  " to " + os.path.join(self.downloadprefix,filename))
			self.HIFIfilename = filename
			return True
		else:
			logging.debug("FAIL on hi-fi version of " + self.title + " by " + self.parent().artist +  " to " + os.path.join(self.downloadprefix,filename))
			return False


	def tag(self, hifi = False):
		'''create or modify the id3 tag for downloaded song associated with self. set optional hifi arg to tag the hifi download'''
		if hifi:
			fileToTag = os.path.join(self.downloadprefix,self.HIFIfilename)
		else:
			fileToTag = os.path.join(self.downloadprefix,self.filename)
		if fileToTag == None:
			logging.info("asked to tag a file associated with uid: " + str(self.parent().uid) + " but the song does not exist locally")			
		logging.debug("adding tags to " + fileToTag)
		try: id3 = mutagen.id3.ID3(fileToTag)
		except mutagen.id3.ID3NoHeaderError:
			logging.info("No ID3 header found for " + fileToTag + "; creating tag from scratch")
			id3 = mutagen.id3.ID3()
		except Exception, err:
			logging.error(str(err))
			return
		id3.add(mutagen.id3.TIT2(encoding=3,text=self.title))
		id3.add(mutagen.id3.TPE1(encoding=3,text=self.parent().artist))
		id3.add(mutagen.id3.COMM(encoding=3,text=self.comments, lang="eng", desc=""))
		#id3.add(mutagen.id3.COMM(encoding=3,text=relationshipLink, lang="eng", desc="MusicGrabberSig"))	
		id3.add(mutagen.id3.TALB(encoding=3,text=self.parent().album))
		if self.trackNum != None:
			id3.add(mutagen.id3.TRCK(encoding=3,text=str(self.trackNum) + '/' + str(self.totalTracks)))
		id3.add(mutagen.id3.POPM(encoding=3,email=str(self.parent().uid)+"@myspace", rating = 128, count=self.playcount))
		if self.image == None:
			logging.error("No image present for " + self.title + ", " + self.parent().artist)
		try:
			logging.debug("trying to get image from " + self.image)
			localImgPath, imgHeader = try_get(self.image, os.path.join("/tmp",os.path.basename(self.image)))
			imgHandle = open(localImgPath)
			id3.add(mutagen.id3.APIC(encoding=3, mime=imgHeader.type, data=imgHandle.read(), type=17, desc="Song pic from myspace.com"))
		except:
			logging.error("Unable to retieve image for " + self.title + ", " + self.parent().artist)
		try:
			id3.save(fileToTag)
		except Exception, err:
			logging.error(str(err) + ";couldn\'t save the tag for " + self.title + " by " + self.parent().artist)
