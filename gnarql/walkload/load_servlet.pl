:- module(load_servlet,[]).

:- use_module(library('http/http_session')).
:- use_module(library('http/http_parameters')).
:- use_module(library('http/http_dispatch')).
:- use_module(library('http/html_write')).
:- use_module(library('semweb/rdf_db')).

:- use_module(load).
:- consult('../namespaces').

:- http_handler(prefix('/load'), walkload, []).

:- http_handler(prefix('/reload'), reload, []).

:- http_handler(prefix('/make'), make, []).

:- http_handler(prefix('/echo'), echo, []).




:- dynamic path/1.
:- dynamic path/2.

walkload(Request) :-
	member(search(Search),Request),
	member(path=Path,Search),
	member(base=Base,Search),
	!,
	rdf_assert(Base,gnarql:path,literal(Path)),
	rdf_assert(Base,rdf:type,gnarql:'MusicCollection'),
	thread_create(load(Path,Base),_,[detached(true)]),
	loaded(Path).
walkload(Request) :-
	member(search(Search),Request),
	member(path=Path,Search),
	rdf_bnode(Id),
	rdf_assert(Id,gnarql:path,literal(Path)),
	rdf_assert(Id,rdf:type,gnarql:'MusicCollection'),
	thread_create(load(Path),_,[detached(true)]),
	loaded(Path).

loaded(Path) :-
	format('Content-type: text/html~n~n'),
	format('Walking and loading RDF files under ~w~n',[Path]).

make(_) :-
	thread_create(rdf_make,_,[detached(true)]),
        format('Content-type: text/html~n~n', []),
        format('Reloading RDF files~n').

reload(_) :-
	format('Content-type: text/html~n~n'),
	setof(collection(Base,Path),rdf(Base,gnarql:path,literal(Path)),Set),
	forall(member(collection(Base,Path),Set),
		(
			(rdf_is_bnode(Base) -> 
				(
					thread_create(load(Path),_,[detached(true)])
				) ; thread_create(load(Path,Base),_,[detached(true)])),
			reloaded(Base)
		)).

reloaded(Base) :-
	format('Reloading RDF files under ~w~n',[Base]).


echo(R) :-
	format('Content-type: text/html~n~n'),
	term_to_atom(R,Ra),
	format(Ra),format('~n').

