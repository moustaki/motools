#! /usr/local/lib/pl-5.8.3/bin/x86_64-linux/pl -G64m -T64m -L32m -s

/** <module> Last.fm run

This module is to start the Last.fm API to RDF converter server.
Please set the correct SWI-Prolog path.

@author 	Yves Raimond
@version 	1.0 
@copyright 	Yves Raimond; 2008 - 2010
*/

:- consult(lastfm_server).
:- server.

