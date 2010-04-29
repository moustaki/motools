:- module(config,
		[ host/1,			% +HOST
		  lastfm_api_key/1,		% +LFM_API_KEY
		  lastfm_api_secret/1,		% +LFM_API_SECRET
		  lastfm_api_host/1,		% +LFM_API_HOST
		  lastfm_host/1,		% +LFM_HOST
		  lastfm_api_sessionkey/1	% +LFM_API_SESSIONKEY
		]).

/** <module> Last.fm API to RDF converter configuration

This module is for configuration of the Last.fm to RDF converter.

@author		Yves Raimond,
		Thomas Gängler
@version	2.0
@copyright	Yves Raimond, Thomas Gängler; 2008 - 2010 
*/

%%	host(+HOST) is det.
%
%	Configure here the host for call-back (the host where you set up the server).
 
host('http://localhost:3060').

%%	lastfm_api_key(+LFM_API_KEY) is det.
%
%	Set here your Last.fm API key.
 
lastfm_api_key('Your Last.fm API Key').

%%	lastfm_api_secret(+LFM_API_SECRET) is det.
%
%	Set here your Last.fm secret.
 
lastfm_api_secret('Your Last.fm API Secret').

%%	lastfm_api_host(+LFM_API_HOST) is det.
%
%	Set here the Last.fm API host (It might change in the future :-) ).
 
lastfm_api_host('http://ws.audioscrobbler.com/2.0/').

%%	lastfm_host(+LFM_HOST) is det.
%
%	Set here the default Last.fm host.
 
lastfm_host('http://www.last.fm/').

%%	lastfm_api_sessionkey(+LFM_API_SESSIONKEY) is det.
%
%	A Last.fm session key - stored for testing purpose.
 
lastfm_api_sessionkey('A valid Session Key').

%%	musicbrainz_host(+MUSICBRAINZ_HOST) is det.
%
%	Set here the default MusicBrainz host.
 
musicbrainz_host('http://musicbrainz.org/').


