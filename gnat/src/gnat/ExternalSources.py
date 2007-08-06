#!/usr/bin/env python
# encoding: utf-8
"""
ExternalSources.py

Created by Chris Sutton on 2007-08-03.
Copyright (c) 2007 Chris Sutton. All rights reserved.
"""

from logging import log, error, warning, info, debug

def addIsophonicsTrackLinks(rdfhub):
	"""Add links to isophonics.net resources.
	   
	   For each subject URI beginning http://zitgist.com/track/ in the given rdf db,
	   adds an owl:sameAs link to the corresponding http://isophonics.net/track resource.
	"""
	
	zgURIs = rdfhub.getSubjURIsWithBase("http://zitgist.com/music/track/", "batch_fp")
	for zgURI in zgURIs:
		ipURI = zgURI.replace("http://zitgist.com/music/", "http://isophonics.net/")
		debug("Adding sameAs link from %s to %s", zgURI, ipURI)
		rdfhub.addSameAs(zgURI, ipURI)