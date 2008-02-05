"""
  Perform a track lookup on the Musicbrainz database, using
  embedded ID3 tags

  You need the SVN version of python-musicbrainz2 in order to 
  make this run (as of 02/08/2007)
  
  Yves Raimond, C4DM, Queen Mary, University of London
  yves.raimond (at) elec.qmul.ac.uk
"""

from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.apev2 import APEv2
from mutagen.mp3 import MP3
from mutagen.asf import ASF
from mutagen.mp4 import MP4
from mutagen.musepack import Musepack
from mutagen.oggvorbis import OggVorbis
from mutagen.oggflac import OggFLAC
from mutagen.oggtheora import OggTheora
from mutagen.trueaudio import TrueAudio
from mutagen.wavpack import WavPack
from MbzURIConverter import *
from CachedMBZQuery import *
from musicbrainz2.webservice import ResponseError, ConnectionError, WebServiceError
import musicbrainz2.webservice as ws
import sys
import logging
from logging import log, error, warning, info, debug
import re


class MbzLookupException :

	def __init__(self,message) :
		self.message = message

	def __str__(self) :
		return self.message

class FileTypeException :
	
	def __init__(self,message) :
		self.message = message
	
	def __str__(self) :
		return self.message

class MbzTrackLookup :

	def __init__(self,file,metadata=None,threshold=60,duration_distance_threshold=10000) :
		self.file = file
		self.threshold = threshold
		self.ddt=duration_distance_threshold
		self.cleaner = re.compile(r"[^A-Za-z0-9 ]").sub
		self.audio = None
		
		if metadata is not None: # We trust provided metadata over local tags
			self.audio = metadata
		else:
			# Try MP3 last cause it doesn't seem to throw an exception on wrong filetypes...
			handlers = [FLAC,OggVorbis,OggFLAC,OggTheora,APEv2,ASF,MP4,Musepack,TrueAudio,WavPack,lambda x: MP3(x,ID3=EasyID3)]
			for handler in handlers:
				if self.audio is None:
					try:
						self.audio = handler(file)
					except:
						pass
			if self.audio is None:
				raise FileTypeException('Unknown file type, no metadata, or file not found.')
			
		try :
			[title] = self.audio['title']
			self.title = self.__clean_literal(str(title))
		except :
			self.title = None
		try :
			[artist] = self.audio['artist']
			self.artist = self.__clean_literal(str(artist))
		except :
			self.artist = None
		try :
			[album] = self.audio['album']
			self.album = self.__clean_literal(str(album))
		except :
			self.album = None
		try :
			# Note : I think we're too sensitive to track number
			# Before adding this check for track numbers of the form 'x/y' mapping would fail when it should probably have succeeded
			[tracknumber] = self.audio['tracknumber']
			if tracknumber.find('/') > 0:
				self.tracknumber = int(self.__clean_literal(str(tracknumber[0:tracknumber.find("/")])))
			else:
				self.tracknumber = int(self.__clean_literal(str(tracknumber)))
		except :
			self.tracknumber = None
		
		
		self.mbzQuery()

	def mbzQuery(self) :
		self.query = CachedMBZQuery()
		
		debug(' - Trying to guess an ID for track \"'+str(self.title)+'\", artist \"'+str(self.artist)+'\", release \"'+str(self.album)+'\", track number '+str(self.tracknumber))
		
		try:
			artists = self.getArtists()

			artist_mapping = []
			release_mapping = []
			track_mapping = []

			if(self.album==None):
				debug("No release information, dropping release lookup")
			
			for artist in artists :
				artist_id = (MbzURIConverter(artist.artist.id)).getId()
				artist_mapping.append((artist.score,artist))
				if(self.album!=None) :
					releases = self.getReleases(artist_id)
					if releases == [] :
						tracks = self.getTracks(artist_id)
						for track in tracks :
							track_mapping.append(((track.score + artist.score)/2 ,track))
					for release in releases :
						release_id = (MbzURIConverter(release.release.id)).getId()
						release_mapping.append(((release.score + artist.score)/2,release))
						tracks = self.getTracks(artist_id,release_id)
						for track in tracks :
							track_mapping.append(((track.score +release.score + artist.score)/3 ,track))
				else :
					tracks = self.getTracks(artist_id)
					for track in tracks :
						track_mapping.append(((track.score + artist.score)/2 ,track))
			if artists==[] :
				if(self.album!=None) :
					releases = self.getReleases()
					if releases == [] :
						tracks = self.getTracks()
						for track in tracks :
							track_mapping.append((track.score ,track))
					for release in releases :
						release_id = (MbzURIConverter(release.release.id)).getId()
						release_mapping.append((release.score,release))
						tracks = self.getTracks(None,release_id)
						for track in tracks :
							track_mapping.append(((track.score +release.score)/2 ,track))
						
		except ResponseError, e:
			raise MbzLookupException('Musicbrainz response error')
		except ConnectionError, e:
			raise MbzLookupException('Musicbrainz connection error')
		except WebServiceError, e:
			raise MbzLookupException('Musicbrainz webservice error')
		
		track_mapping.sort()
		track_mapping.reverse()
		self.track_mapping = track_mapping
		if self.empty_results() : 
			raise MbzLookupException('No results')
		if not self.confident() :
			raise MbzLookupException('Not confident enough about matching MBZ tracks')
		self.clean_results()
		if self.ambiguous() :
			debug('Disambiguating through duration')
			self.disambiguate_through_duration()
		if self.empty_results() :
			raise MbzLookupException('No results')
		debug('ID Found : '+self.track_mapping[0][1].track.getId())
	
	def getArtists(self) :
		if self.artist == None :
			return []
		else :
			artist_filter = ws.ArtistFilter(name=str(self.artist))
			artists = self.query.getArtists(filter=artist_filter)
			return artists

	def getTracks(self,artist_id=None,release_id=None) :
		if self.title == None  or (self.tracknumber == None and release_id == None) or (self.tracknumber==None and artist_id==None):
			return []
		else :
			if not(self.tracknumber == None) and not(release_id == None) :
				track_filter = ws.TrackFilter(query='tnum:'+str(self.tracknumber)+ ' AND reid:'+release_id)
			elif release_id==None and not(self.tracknumber == None) and not(self.title == None) and not(artist_id==None):
				track_filter = ws.TrackFilter(query='(track:"'+str(self.title)+'" AND tnum:'+str(self.tracknumber)+' )'+' AND arid:'+artist_id)
			elif artist_id==None and release_id==None :
				track_filter = ws.TrackFilter(query='(track:"'+str(self.title)+'")')
			elif release_id==None :
				track_filter = ws.TrackFilter(query='(track:"'+str(self.title)+'") '+' AND arid:'+artist_id)
			elif artist_id==None :
				track_filter = ws.TrackFilter(query='(track:"'+str(self.title)+'") '+' AND reid:'+release_id)
			else :
				track_filter = ws.TrackFilter(query='(track:"'+str(self.title)+'") '+' AND reid:'+release_id+' AND arid:'+artist_id)
			tracks = self.query.getTracks(track_filter)
			return tracks

	def getReleases(self,artist_id=None) :
		if self.album == None :
			return []
		else :
			if artist_id==None:
				release_filter = ws.ReleaseFilter(query='(release:'+str(self.album)+')')
			else :
				release_filter = ws.ReleaseFilter(query='(release:"'+str(self.album)+'") '+' AND arid:'+artist_id)
			releases = self.query.getReleases(release_filter)
			return releases


	def getMbzTrackURI(self) :
		return self.track_mapping[0][1].track.getId()
	
	# returns true if the first result have a confidence higher than the confidence threshold
	def confident(self) :
		if self.track_mapping[0][0] > self.threshold :
			return True
		else :
			return False

	# returns true in case there are no results, false otherwise
	def empty_results(self) :
		return self.track_mapping == []

	# drop results with not the highest confidence
	def clean_results(self) :
		samescoreresults = []
		k = 0
		while k < len(self.track_mapping) and self.track_mapping[k][0] == self.track_mapping[0][0] :
			samescoreresults.append(self.track_mapping[k])
			k = k + 1
		self.track_mapping = samescoreresults

	# returns true if two results have the same confidence, false otherwise
	def ambiguous(self)  :
		if self.empty_results() :
			return False
		a = self.track_mapping
		if len(a) == 1 :
			return False
		else :
			return True

	def disambiguate_through_duration(self) :
		if not hasattr(self.audio,"info"): # no duration info available (eg. with CSV input)
			self.track_mapping = []
			return
			
		duration = self.audio.info.length * 1000
		debug('Duration of the audio file (ms):' + str(duration))
		closest = self.ddt
		for result in self.track_mapping :
			if (result[1].track).getDuration()!=None :
				debug('Duration of matching track in MBZ: '+ str((result[1].track).getDuration()))
				if abs(duration - (result[1].track).getDuration()) < closest :
					closest = duration - (result[1].track).getDuration()
					closest_result = result
		if closest==self.ddt :
			self.track_mapping = []
		else :
			self.track_mapping = [closest_result]


	def __clean_literal(self,literal) :
		t = self.cleaner("", literal)
		return re.sub(r' {2,}',' ',t)
