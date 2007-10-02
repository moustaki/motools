#!/usr/local/bin/pl -s

:- use_module(onto_spec).
:- use_module(library('semweb/rdf_db')).
:- use_module(library('semweb/rdf_turtle')).

:- rdf_load('../rdf/audio_features.n3').

:- gen('../doc/audio_features.html').


