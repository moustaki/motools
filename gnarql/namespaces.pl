:- module(namespaces,[]).

/**
 * Some common namespaces GNARQL might need
 */


:- use_module(library('semweb/rdf_db')).

:- rdf_register_ns(mo,'http://purl.org/ontology/mo/').
:- rdf_register_ns(dc,'http://purl.org/dc/elements/1.1/').
:- rdf_register_ns(foaf,'http://xmlns.com/foaf/0.1/').
:- rdf_register_ns(xsd,'http://www.w3.org/2001/XMLSchema#').
:- rdf_register_ns(time,'http://www.w3.org/2006/time#').
:- rdf_register_ns(tl,'http://purl.org/NET/c4dm/timeline.owl#').
:- rdf_register_ns(event,'http://purl.org/NET/c4dm/event.owl#').
:- rdf_register_ns(tags,'http://www.holygoat.co.uk/owl/redwood/0.1/tags/').
