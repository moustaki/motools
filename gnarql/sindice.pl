:- module(sindice,[sindice_q/1,sindice_r/2]).

/**
 * A SWI-Prolog module to access
 * the Sindice Semantic Web search
 * engine.
 *
 * http://sindice.com/
 *
 * Yves Raimond, C4DM, Queen Mary, University of London
 */


:- use_module(library('semweb/rdf_db')).
:- use_module(library('semweb/rdf_http_plugin')).


/**
 * Queries Sindice for an URI
 * Store results within the local RDF KB
 */
sindice_q(URI) :-
	sindice_query_url(URI,Query),
	rdf_load(Query).

/**
 * What was retrieved from Sindice,
 * and what results did it give?
 */
sindice_r(QueryURI,URI) :-
	rdf_db:rdf(QueryURI,rdfs:seeAlso,URI),
	sindice_host(H),
	parse_url(T,[protocol(http),host(H)]),
	atom_concat(T,_,QueryURI).


/**
 * Sindice host
 */
sindice_host('sindice.com').


/**
 * Creates a Query URI
 * from an URI to look-up
 */
sindice_query_url(URI,QueryURL) :-
	sindice_host(DN),
	www_form_encode(DN,DNe),
	parse_url(QueryURL,[protocol(http),host(DNe),path('/query/lookup'),search([uri=URI])]).
	





