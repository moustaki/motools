# encoding: utf-8
"""
FPTrackLookup.py

Created by Chris Sutton on 2007-08-01.
Copyright (c) 2007 Chris Sutton. All rights reserved.
"""

import sys
import os
import rdflib
import xml.dom.minidom
import logging
from logging import log, error, warning, info, debug
from time import asctime
import re
from urllib import quote as urlencode

from PUIDTrackLookup import *
import mopy; from mopy import MusicInfo; from mopy.model import AudioFile, MusicArtist, Track, Signal

# NOTE : Specify an absolute or relative path here. Don't assume $PATH will do - some files will be "unanalyzable" if you do.
genpuidbin = "./genpuid" 
MusicDNSKey = "845c6a3ae981f1450eb13730183448d8" #Chris S's key

class FPTrackLookup :
	def __init__(self):
		pass

	def fpFile(self, filename):
		"""Looks up the MusicDNS PUID for the given filename using fingerprinting
		   and stores the resulting info in the given graph"""
		global genpuidbin, MusicDNSKey
		
		track = Track()
		audiofile = AudioFile(urlencode(os.path.basename(filename)))
		track.available_as = audiofile
		signal = Signal()
		signal.published_as = track
		mi = MusicInfo([track, audiofile, signal])
		
		filename = clean(filename)
		# TODO : If file isn't a WAV or MP3, use suitable decoder, and then pass the resulting wav to genpuid.
		res_xml = os.popen(genpuidbin + " " + MusicDNSKey + " -rmd=2 -xml -noanalysis \""+filename+"\"").readlines()
			
		retry_count=0
		while ("".join(res_xml).find("unanalyzable") > 0) and (retry_count < 5):
			warning("MusicDNS reports file is unanalyzable. Trying again...") # This can be caused by server hiccups
			retry_count+=1
			res_xml = os.popen(genpuidbin + " " + MusicDNSKey + " -rmd=2 -xml -noanalysis \""+filename+"\"").readlines()

		# parse results
		try:
			if (res_xml[0] == res_xml[1]):
				res_xml=res_xml[1:] # oddly, we see "<genpuid songs="1">\n" twice when the file is "unanalyzable"

			clean_xml = "".join(res_xml).replace("mip:","") # strip out unknown prefix so minidom can parse
			dom = xml.dom.minidom.parseString(clean_xml)
	
			root = dom.getElementsByTagName("genpuid")[0]

			if (root.hasAttribute("songs") == False) or (int(root.getAttribute("songs")) == 0):
				return MusicInfo()
			
			trackelem = root.getElementsByTagName("track")[0]
			
			if (trackelem.childNodes[0].nodeName=="#text") and (trackelem.childNodes[0].data == "unavailable"):
				info(" No PUID available for track : "+str(trackelem.childNodes[0].data))
				return MusicInfo()
			
			titles = trackelem.getElementsByTagName("title")
			if len(titles)>0:
				track.title = titles[0].childNodes[0].wholeText
			
			artists = trackelem.getElementsByTagName("artist")
			if len(artists)>0:
				artistobj=MusicArtist()
				artistobj.name = artists[0].getElementsByTagName("name")[0].childNodes[0].wholeText
				mi.add(artistobj)
				track.maker = artistobj
			
			puid_list = trackelem.getElementsByTagName("puid-list")
			puid_nodes = puid_list[0].getElementsByTagName("puid")
			puids = []
			
			for puid_node in puid_nodes:
				puids.append(puid_node.getAttribute("id"))
			if len(puids) == 0:
				info(" No PUID available for track : "+str(trackelem.childNodes[0].data))
				return MusicInfo()
		 	elif len(puids) > 1:
				warning("Multiple PUIDs returned for track !")
				
			puid = puids[0]
			signal.puid = puid
			

			# FIXME
			# years = trackelem.getElementsByTagName("first-release-date")
			# if len(years)>0:
			# 	year = years[0].childNodes[0].wholeText
			# else:
			# 	year = None

			# FIXME
			# release_dates = trackelem.getElementsByTagName("first-release_date")
			# if len(release_dates)>0:
			# 	release_date = release_dates[0]
			# else:
			# 	release_date = None
		
			# FIXME
			# genres = []
			# genre_lists = trackelem.getElementsByTagName("genre-list")
			# if len(genre_lists)>0:
			# 	for genre_list in genre_lists:
			# 		genre_nodes = genre_list.getElementsByTagName("genre")
			# 		for genre_node in genre_nodes:
			# 			genres.append(genre_node.getElementsByTagName("name")[0].childNodes[0].wholeText)
				
		except Exception, e:
			error("Failure while parsing results !")
			debug("xml :\n"+"".join(res_xml))
			error(str(e))
			return MusicInfo()
			 
		# Look up in MBZ using PUID and metadata :
		try:
			pl = PUIDTrackLookup(filename, puid, mi)
			mbzuri = pl.getMbzTrackURI()
			mbzconvert = MbzURIConverter(mbzuri)
			track.URI = mbzconvert.getURI()
			if (mbzconvert.getURI().find("track") == -1):
				error("Incomprehensible URI for track !")
			signal.URI = mbzconvert.getURI().replace("track","signal")
		except MbzLookupException, e:
			error(" - " + e.message)
		except FileTypeException, e:
			error(" - " + e.message)
	
		return mi


def clean(s):
	s = s.replace('`','\`') # FIXME : other shell-unfriendly characters should be handled too
	return s

def main():
	fp = FPTrackLookup()	
	fp.fpFile("test.mp3")
	
if __name__ == '__main__':
	
	loggingConfig = {"format":'%(asctime)s %(levelname)-8s %(message)s',
                     "datefmt":'%a, %d %b %Y %H:%M:%S',
					 "filename":'fpcrawler.log',
                     "filemode":'a',
					 "level":logging.DEBUG}
		
	logging.basicConfig(**loggingConfig)
	debug("--- Starting "+ asctime()  +" ---")
	main()

