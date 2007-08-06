#!/usr/bin/env python
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

genpuidbin = "../../bin/genpuid"
MusicDNSKey = "845c6a3ae981f1450eb13730183448d8" #Chris S's key

class FPTrackLookup :
	def __init__(self):
		pass

	def fpFile(self, filename):
		"""Looks up the MusicDNS PUID for the given filename using fingerprinting and stores the resulting info in the given graph"""
		global genpuidbin, MusicDNSKey
		
		res_xml = os.popen(genpuidbin + " " + MusicDNSKey + " -rmd=2 -xml -noanalysis \""+filename+"\"").readlines()
	
		# parse results
		try:
			clean_xml = "".join(res_xml).replace("mip:","") # strip out unknown prefix so minidom can parse
			dom = xml.dom.minidom.parseString(clean_xml)
	
			root = dom.getElementsByTagName("genpuid")[0]

			if (root.hasAttribute("songs") == False) | (int(root.getAttribute("songs")) == 0):
				return {}
			
			track = root.getElementsByTagName("track")[0]
			
			if (track.childNodes[0].nodeName=="#text") & (track.childNodes[0].data=="unavailable"):
				info("No PUID available for track.")
				return {}
			
			titles = track.getElementsByTagName("title")
			if len(titles)>0:
				title = titles[0].childNodes[0].wholeText
			else:
				title = None
			
			artists = track.getElementsByTagName("artist")
			if len(artists)>0:
				artist = artists[0].getElementsByTagName("name")[0].childNodes[0].wholeText
			else:
				artist = None

			years = track.getElementsByTagName("first-release-date")
			if len(years)>0:
				year = years[0].childNodes[0].wholeText
			else:
				year = None
			
			puid_list = track.getElementsByTagName("puid-list")
			puid_nodes = puid_list[0].getElementsByTagName("puid")
			puids = []
			for puid_node in puid_nodes:
				puids.append(puid_node.getAttribute("id"))
		
			release_dates = track.getElementsByTagName("first-release_date")
			if len(release_dates)>0:
				release_date = release_dates[0]
			else:
				release_date = None
		
			genres = []
			genre_lists = track.getElementsByTagName("genre-list")
			if len(genre_lists)>0:
				for genre_list in genre_lists:
					genre_nodes = genre_list.getElementsByTagName("genre")
					for genre_node in genre_nodes:
						genres.append(genre_node.getElementsByTagName("name")[0].childNodes[0].wholeText)
				
		except Exception, e:
			error("Failure while parsing results !")
			debug("xml :\n"+"".join(res_xml))
			error(str(e))
			return {}
	
	
		results = {}

		if title:
			info("title : "+title)
			results["title"] = title
		if artist:
			info("artist : "+artist)
			results["artist"] = artist
		if year:
			info("year : "+year)
			results["year"] = year
		if len(puids)>0:
			info("puids : "+",".join(puids))
			results["puids"]=[]
			for puid in puids:
				results["puids"].append(puid)
		if len(genres)>0:
			info("genres : "+",".join(genres))
			results["genres"]=[]
			for genre in genres:
				results["genres"].append(genre)
			
		debug("results :"+str(results))
		return results

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

