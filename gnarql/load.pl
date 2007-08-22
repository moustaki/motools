:- module(load,[load/1]).

/**
 * Just a small util to load every rdf file
 * available under a given directory into
 * a Prolog RDF kb
 *
 * Yves Raimond, C4DM, Queen Mary, University of London
 * (c) 2007
 */

:- use_module(library('semweb/rdf_db')).
:- use_module(walk).

load(Dir) :-
	forall(
		( walk(Dir,Walk),
		  format(atom(Wildcard),'~w/~w',[Walk,'*.rdf']),
		  expand_file_name(Wildcard,Files),
		  member(File,Files),
		  nl,format(' - Loading ~w\n',File)
		  ),
		  rdf_load(File)
		).


