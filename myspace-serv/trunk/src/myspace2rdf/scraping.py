#! /usr/bin/env python

import logging
from xml.dom import minidom as dom

def scrapePage(page, patterns, termChar):
	"""Scrape the page at sock for each pattern in "patterns" and return the identifier occurring after the
	  last pattern (which is assumed to be terminated by a double-quote symbol)"""
	#if sock == None:
	#	   return None;
	#page = sock.read()
	#sock.close()
	
	#logging.debug("Pulling out link...")
	idx = 0
	idx_end = len(page)
	for pattern in patterns:
		#logging.debug("pattern : "+pattern)
		idx = page.find(pattern, idx)
		#logging.debug("idx = "+str(idx))
		if (idx > idx_end): # Couldn't find this pattern before re-occurrence of last pattern
			logging.debug("Traversal failed !")
			logging.debug(page[max(0,idx-1000):idx+5000])
			return None;
		idx_end = page.find(pattern,idx+1) # find next occurrence
		if idx_end == -1:
			idx_end = len(page)
		#logging.debug("idx_end = "+str(idx_end))

	if idx != -1:
		idx += len(patterns[-1])
	# idx should now point to the start of the identifier we want
	id_end = page.find(termChar, idx)
	identifier = unicode(page[idx:id_end], 'utf8')
	
	if len(identifier) == 0:
		#logging.debug("Identifier not found...")
		return None;

	return identifier;

def scrapePageWhile(page, patterns, termChar):
	"""Scrape the page at sock for each pattern and return a list with each identifier occurring after the
	  last pattern (which is assumed to be terminated by a double-quote symbol)"""
	#if sock == None:
	#	   return None;
   
	#page = sock.read()
	#sock.close()
	
	#logging.debug("Pulling out link...")
	idx = 0
	idx_end = len(page)
	identifiers = []
	itsFound = 1
	while itsFound:
		pattern = patterns
		idx = page.find(pattern, idx)
		#logging.debug("idx = "+str(idx))
		if (idx > idx_end): # Couldn't find this pattern before re-occurrence of last pattern
			logging.debug("Traversal failed !")
			logging.debug(page[max(0,idx-1000):idx+5000])
			return None;
		
		idx_end = page.find(pattern,idx+1) # find next occurrence
		if idx_end == -1:
			idx_end = len(page)
		#logging.debug("idx_end = "+str(idx_end))
	
		if idx != -1:
			idx += len(patterns)
		# idx should now point to the start of the identifier we want
		id_end = page.find(termChar, idx)
		identifier = unicode(page[idx:id_end], 'utf8')
	
		if len(identifier) == 0:
			#logging.debug("Identifier not found...")
			itsFound = 0
			
		if identifier!='':
			#logging.debug("Found identifier : "+identifier)
			identifiers.append(identifier)
			
	return identifiers;



