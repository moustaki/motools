:- module(control,[admin_interface/0]).

/**
 * A small servlet allowing to perform
 * some administration operation on the store
 *
 * Yves Raimond, C4DM, QMUL, 2007
 */

:- use_module(library('http/thread_httpd')).
:- use_module(library('semweb/rdf_db')).
:- use_module(log).

/**
  * Closes the servlet
  */
reply(Request) :-
        log:log(Request),
        member(path('/quit'), Request), !,
        format('Connection: close~n', []),
        format('Content-type: text/html~n~n', []),
        format('Bye Bye~n').

/**
  * Run rdf_make
  */
reply(Request) :-
	member(path('/reload'),Request),!,
	log:log('Running rdf_make'),
	rdf_make,
	format('Content-type: text/html~n~n', []),
	format('Reloading RDF files~n').


/**
  * Init the servlet
  */

admin_interface :-
	http_server(reply,[ port(1111),timeout(20)]).

