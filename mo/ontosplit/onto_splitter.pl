:- module(onto_splitter,[split/0]).

/**
 * Just a util to split the ontology between terms defined by the document
 * and terms defined outside it
 *
 * Yves Raimond, C4DM, QMUL, 2007
 */

:- use_module(library('semweb/rdf_db')).
:- use_module(library('rdf')).


/**
 * Adjust these to your needs
 */
document('musicontology.rdfs').
primary_ns('http://purl.org/ontology/mo/').
output_core('musicontology-core.rdfs').
output_external('musicontology-external.rdfs').

/**
 * Top-level goal
 */
split :- 
	load,
	core,
	external.

/**
 * Load the document
 */
load :- 
	document(Doc),
	rdf_db:rdf_load(Doc).

/**
 * Extract and export the core (explores up to three bnodes)
 */
core :- 
	primary_ns(NS),
	findall(rdf(S,P,O),
		(rdf_db:rdf(A,rdfs:isDefinedBy,NS),description(A,rdf(S,P,O))),
		TriplesCore),
	output_core(Core),
	open(Core,write,CoreStream),
	rdf_write_xml(CoreStream,TriplesCore),
	close(CoreStream).

/**
 * Extract and export the externals
 */
external :-
	primary_ns(NS),
	findall(rdf(A,P,O),
		(rdf_db:rdf(A,rdfs:isDefinedBy,NS2),NS2\==NS,rdf_db:rdf(A,P,O)),
		TriplesExternal),
	output_external(External),
	open(External,write,ExternalStream),
	rdf_write_xml(ExternalStream,TriplesExternal),
	close(ExternalStream).

/**
 * All the triples describing a given ontology term
 * This predicates include blank-nodes closure
 */
description(A,rdf(A,P,O)) :-
	rdf_db:rdf(A,P,O).
description(A,rdf(S,P,O)) :-
	rdf_db:rdf(A,_,BN),
	rdf_db:rdf_is_bnode(BN),
	description(BN,rdf(S,P,O)).


