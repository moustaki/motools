#!/usr/bin/env python
# encoding: utf-8
"""
PUIDTrackLookup.py

Created by Chris Sutton on 2007-08-06.
Copyright (c) 2007 Chris Sutton. All rights reserved.
"""

from MbzTrackLookup import *
from logging import log, error, warning, info, debug

class PUIDTrackLookup(MbzTrackLookup):

	def __init__(self,file,puid,metadata=None):
		if metadata==None:
			metadata={}
		self.md=metadata
		self.puid = puid
		MbzTrackLookup.__init__(self,file=file)
	
	def mbzQuery(self):
		"""Uses the given PUID and metadata to find the MusicBrainz identifier for the track."""		
		query = CachedMBZQuery()
	
		track_filter = ws.TrackFilter(puid=self.puid)
		trackresults = query.getTracks(track_filter)
		tracks = [tr.getTrack() for tr in trackresults]
		self.track = self.choose(tracks)
		
	def choose(self, tracks):
		"""Choose the best match from among the given TrackResult objects."""
		if len(tracks) == 0:
			raise MbzLookupException("No tracks found matching PUID "+self.puid)
			return None
		elif len(tracks) == 1:
			debug("Single track matching PUID found.")
			return tracks[0]

		debug("Multiple tracks match PUID.")
		tracks = self.filterByArtist(tracks)
		if len(tracks) > 1:
			tracks = self.filterByTitle(tracks)
		if len(tracks) > 1:
			tracks = self.filterByRelease(tracks)					
		
		if len(tracks) == 0:
			raise MbzLookupException('No results after filtering.')
		else:
			warning("Multiple matches after doing filtering - Just picking first result.")
			return tracks[0]
		

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
			ts = [t for t in tracks if album in map(lambda x:x.getTitle(),t.getReleases())]
			if len(ts)==0:
				debug("None match album, no album filtering done.")
				return tracks
		else:
			debug(" no local album tag :/ No album filtering done.")
			return tracks
		return ts

	def getMbzTrackURI(self):
		return self.track.getId()
						
def main():
	pass


if __name__ == '__main__':
	main()

