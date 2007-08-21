#!/usr/bin/env python
# encoding: utf-8
"""
PUIDTrackLookup.py

Created by Chris Sutton on 2007-08-06.
Copyright (c) 2007 Chris Sutton. All rights reserved.
"""

from MbzTrackLookup import *
from logging import log, error, warning, info, debug
import musicbrainz2.webservice as ws

class PUIDTrackLookup(MbzTrackLookup):

	def __init__(self,file,puid,mi=None):
		
		self.md={}
		
		# Extract metadata from MusicInfo obj
		if mi!=None:
			if hasattr(mi, "TrackIdx"):
				track = mi.TrackIdx.values()[0]
				if len(track.title) > 0:
					self.md["title"] = list(track.title)[0]
				if len(track.creator) > 0:
					artist = list(track.creator)[0]
					if len(artist.name) > 0:
						self.md["artist"] = list(artist.name)[0]
					
			
		self.puid = puid
		MbzTrackLookup.__init__(self,file=file)
	
	def mbzQuery(self):
		"""Uses the given PUID and metadata to find the MusicBrainz identifier for the track."""		
		query = CachedMBZQuery()
	
		track_filter = ws.TrackFilter(puid=self.puid)
		try:
			trackresults = query.getTracks(track_filter)
		except (ws.ConnectionError, ws.ResponseError):
			try:
				trackresults = query.getTracks(track_filter)
			except (ws.ConnectionError, ws.ResponseError, ws.WebServiceError), e:
				raise MbzLookupException("MBZ query failed."+str(e))
		tracks = [tr.getTrack() for tr in trackresults]
		self.track = self.choose(tracks)
		
	def choose(self, tracks):
		"""Choose the best match from among the given TrackResult objects."""
		if len(tracks) == 0:
			raise MbzLookupException("No tracks found matching PUID "+self.puid)
			return None
		elif len(tracks) == 1:
			debug("Single track matching PUID found.")
			if (self.md.has_key("artist")) and (tracks[0].getArtist().getName() <> self.md["artist"]):
				warning("Sanity check FAILS : MBZ artist name = "+tracks[0].getArtist().getName()+\
						" MusicDNS artist name = "+self.md["artist"]+\
						" local artist name = "+str(self.artist))
			return tracks[0]

		debug("Multiple tracks match PUID.")
		
		start_tracks = [t for t in tracks]
		tracks = self.strongFilter(self.filterByArtist, tracks)
		tracks = self.weakFilter(self.filterByTitle, tracks)
		tracks = self.weakFilter(self.filterByRelease, tracks)
		
		if len(tracks) == 0:
			debug("start_tracks:")
			printTracks(start_tracks)
			raise MbzLookupException('No results after filtering.')
		else:
			warning("Multiple matches after doing filtering - Just picking first result.")
			printTracks(tracks)
			return tracks[0]

	def strongFilter(self, function, tracks):
		return function(tracks)
	
	def weakFilter(self, function, tracks):
		filt_tracks = function(tracks)
		if len(filt_tracks) > 0:
			return filt_tracks
		else:
			debug("  filtering with "+function.im_func.func_name+" left no results. No filtering done.")
			return tracks
		
	def filterByArtist(self, tracks):
		debug("Filtering by artist...")
		if self.md.has_key("artist"):
			artist = self.md["artist"]
		else:
			debug(" no MusicDNS metadata, using local")
			artist = self.artist
			
		if artist <> None:
			tracks = [t for t in tracks if t.getArtist().getName()==artist]
			if len(tracks) == 0:
				debug("None match artist.")
		else:
			debug(" no local either :/ No artist filtering done.")
			
		return tracks

	def filterByTitle(self, tracks):
		debug("Filtering by title...")
		if self.md.has_key("title"):
			title = self.md["title"]
		else:
			debug(" no MusicDNS metadata, using local")
			title = self.title
			
		if title <> None:
			tracks = [t for t in tracks if t.getTitle()==title]
			if len(tracks)==0:
				debug("None match title.")
		else:
			debug(" no local either :/ No title filtering done.")
		
		return tracks
	
	def filterByRelease(self, tracks):
		debug("Filtering by release...")
		album = self.album
		if album <> None:
			tracks = [t for t in tracks if album in map(lambda x:x.getTitle(),t.getReleases())]
			if len(tracks)==0:
				debug("None match album.")
		else:
			debug(" no local album tag :/ No album filtering done.")
			
		return tracks

	def getMbzTrackURI(self):
		return self.track.getId()

def printTracks(tracks):
	for track in tracks:
		debug("track :")
		printTrack(track)

def printTrack(track):
	debug("Artist : name="+track.getArtist().getName()+"\t\t\t id="+track.getArtist().getId())
	debug("Title  : "+track.getTitle())
	for r in track.getReleases():
		debug("Release: name="+r.getTitle()+"\t\t\t id="+r.getId())

						
def main():
	pass


if __name__ == '__main__':
	main()

