#!/usr/local/bin/pl -s

:- use_module(onto_spec).
:- use_module(library('semweb/rdf_db')).


:- rdf_db:rdf_load('musicontology-core.rdfs').

:- gen 'musicontology-core.html'.

:- rdf_db:rdf_retractall(_,_,_).

:- rdf_db:rdf_load('musicontology-external.rdfs').

:- gen 'musicontology-external.html'.

:- halt.
