#!/usr/local/bin/pl -s

:- use_module(onto_spec).
:- use_module(library('semweb/rdf_db')).
:- use_module(library('semweb/rdf_turtle')).

:- rdf_load('../rdf/audio_features.n3').

author_name('Yves Raimond').
author_foaf('http://moustaki.org/foaf.rdf').
page_title('Ontology Specification').

:- gen('../doc/audio_features.html').


