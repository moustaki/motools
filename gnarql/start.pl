#!/usr/local/bin/pl -s

:- [namespaces].
:- use_module('walkload/load_servlet').
:- use_module('crawl/crawl_servlet').
:- use_module(library('semweb/rdf_persistency')).


:- ['ClioPatria/server/server.pl'].

:- server.

