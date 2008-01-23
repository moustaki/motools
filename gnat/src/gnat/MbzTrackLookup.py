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

	def __init__(self,file,threshold=60,duration_distance_threshold=10000) :
		self.file = file
		self.threshold = threshold
		self.ddt=duration_distance_threshold
		self.cleaner = re.compile(r"[^A-Za-z0-9 ]").sub
		try :
			self.audio = MP3(file,ID3=EasyID3)
		except : 
			try :
				self.audio = FLAC(file)
			except :
				try :
					self.audio = OggVorbis(file)
				except :
					try :
						self.audio = OggFLAC(file)
					except :
						try : 
							self.audio = OggTheora(file)
						except : 
							try :
								self.audio = APEv2(file)
							except :
								try :
									self.audio = ASF(file)
								except :
									try :
										self.audio = MP4(file)
									except : 
										try : 
											self.audio = Musepack(file)
										except :
											try :
												self.audio = TrueAudio(file)
											except :
												try : 
													self.audio = WavPack(file)
												except :
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
		self.mbzQuery()

	def mbzQuery(self) :
		query = CachedMBZQuery()
		
		debug(' - Trying to guess an ID for track \"'+str(self.title)+'\", artist \"'+str(self.artist)+'\", release \"'+str(self.album)+'\"')
		
		artist_filter = ws.ArtistFilter(name=str(self.artist))
		try:
			artists = query.getArtists(filter=artist_filter)

			artist_mapping = []
			release_mapping = []
			track_mapping = []

			if(self.album==None):
				debug("No release information, dropping release lookup")

			for artist in artists :
				artist_id = (MbzURIConverter(artist.artist.id)).getId()
				artist_mapping.append((artist.score,artist))
				if(self.album!=None) :
					release_filter = ws.ReleaseFilter(query='(release:'+str(self.album)+') '+' AND arid:'+artist_id)
					releases = query.getReleases(release_filter)
					if releases == [] :
						track_filter = ws.TrackFilter(query='(track:'+str(self.title)+') '+' AND arid:'+artist_id)
						tracks = query.getTracks(track_filter)
						for track in tracks :
							track_mapping.append(((track.score + artist.score)/2 ,track))
					for release in releases :
						release_id = (MbzURIConverter(release.release.id)).getId()
						release_mapping.append(((release.score + artist.score)/2,release))
						track_filter = ws.TrackFilter(query='(track:'+str(self.title)+') '+' AND reid:'+release_id)
						tracks = query.getTracks(track_filter)
						for track in tracks :
							track_mapping.append(((track.score +release.score + artist.score)/3 ,track))
				else :
					track_filter = ws.TrackFilter(query='(track:'+str(self.title)+') '+' AND arid:'+artist_id)
					tracks = query.getTracks(track_filter)
					for track in tracks :
						track_mapping.append(((track.score + artist.score)/2 ,track))
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
