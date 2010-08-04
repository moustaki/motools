:- module(namespaces,[]).

:- use_module(library('semweb/rdf_db')).

/** <module> Last.fm API to RDF converter namespaces

This module is for the namespaces of the Last.fm to RDF converter.

@author		Yves Raimond, 
		Thomas Gängler
@version	2.0 
@copyright 	Yves Raimond, Thomas Gängler; 2008 - 2010
*/

:- rdf_register_ns(mo,'http://purl.org/ontology/mo/').
:- rdf_register_ns(lfm,'http://purl.org/ontology/last-fm/').
:- rdf_register_ns(dc,'http://purl.org/dc/elements/1.1/').
:- rdf_register_ns(foaf,'http://xmlns.com/foaf/0.1/').
:- rdf_register_ns(event,'http://purl.org/NET/c4dm/event.owl#').
:- rdf_register_ns(tl,'http://purl.org/NET/c4dm/timeline.owl#').
:- rdf_register_ns(wgs,'http://www.w3.org/2003/01/geo/wgs84_pos#').
:- rdf_register_ns(xsd,'http://www.w3.org/2001/XMLSchema#').
:- rdf_register_ns(v,'http://www.w3.org/2006/vcard/ns#').
:- rdf_register_ns(terms,'http://purl.org/dc/terms/').
:- rdf_register_ns(ov,'http://open.vocab.org/terms/').
:- rdf_register_ns(tags,'http://www.holygoat.co.uk/owl/redwood/0.1/tags/').
:- rdf_register_ns(pbo,'http://purl.org/ontology/pbo/core#').
:- rdf_register_ns(co,'http://purl.org/ontology/co/core#').
:- rdf_register_ns(is,'http://purl.org/ontology/is/core#').
:- rdf_register_ns(rec,'http://purl.org/ontology/rec/core#').
:- rdf_register_ns(isi,'http://purl.org/ontology/is/inst/').
:- rdf_register_ns(time,'http://www.w3.org/2006/time#').


