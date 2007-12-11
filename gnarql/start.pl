#!/usr/local/bin/pl -G1G -T1G -L1G -s

:- [namespaces].
:- use_module('walkload/load_servlet').
:- use_module('crawl/crawl_servlet').
:- use_module(library('semweb/rdf_persistency')).


:- ['ClioPatria/server/server.pl'].

:- server.

