:- module(namespaces,[]).

:- use_module(library('semweb/rdf_db')).


:- rdf_register_ns(mo,'http://purl.org/ontology/mo/').
:- rdf_register_ns(lfm,'http://purl.org/ontology/last-fm/').
:- rdf_register_ns(dc,'http://purl.org/dc/elements/1.1/').
:- rdf_register_ns(foaf,'http://xmlns.com/foaf/0.1/').

