#!/usr/local/bin/pl -G1G -T1G -L1G -s

:- [namespaces].
:- use_module(library('semweb/rdf_db')).
:- use_module(library('semweb/rdf_persistency')).


:- ['ClioPatria/server/server.pl'].

:- rdf_attach_db(db,[]).

:- server.




