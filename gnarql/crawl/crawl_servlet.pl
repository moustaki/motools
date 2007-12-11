:- module(crawl_servlet,[]).

/**
 * A module handling crawling
 * from a local SWI RDF store
 *
 * Yves Raimond (c) 2007
 * Queen Mary, University of London
 */



:- use_module(library('http/http_session')).
:- use_module(library('http/http_parameters')).
:- use_module(library('http/http_dispatch')).
:- use_module(library('http/html_write')).
:- use_module(library('semweb/rdf_db')).

:- consult('../namespaces').

:- use_module(pool).
:- use_module(crawl).

:- http_handler(prefix('/crawl/start'), crawl, []).

:- http_handler(prefix('/crawl/init'), crawl_init, []).


crawl_init(Request) :-
	member(search([n=N]),Request),atom_to_term(N,NT,[]),
	catch(
	  (
		create_crawlers_pool(NT),
		format('Content-type: text/html~n~n'),
		format('Crawler threads created: ~w~n',[N])
	  ),_,
	  (
	  format('Content-type: text/html~n~n'),
	  format('Not a valid number ( ~w ), or threads already created~n',[NT])
	  )
	  ).

crawl(_) :-
	thread_create(crawl,_,[detached(true)]),
	format('Content-type: text/html~n~n'),
	format('Crawling process started~n').


