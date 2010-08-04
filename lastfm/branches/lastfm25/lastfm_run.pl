#! /usr/local/lib/swipl-5.10.1/bin/x86_64-linux/swipl -G64m -T64m -L32m -s

/** <module> Last.fm run

This module is to start the Last.fm API to RDF converter server.
Please set the correct SWI-Prolog path.

@author 	Yves Raimond
@version 	1.0 
@copyright 	Yves Raimond; 2008 - 2010
*/

:- consult(lastfm_server).
:- server.

