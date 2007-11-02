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
		  nl,format(' - Loading ~w\n',File),
		  convert_path(Walk,WalkWWW),
		  format(atom(BaseURI),'file://~w/',[WalkWWW])
		  ),
		  catch(rdf_load(File,[base_uri(BaseURI)]), _, print('caught exception while loading !'))
		).



convert_path(Path,C) :-
	atom_chars(Path,Chars),
	replace(Chars,Chars2),
	atom_chars(C,Chars2).

replace([],[]).
replace([H1|T1],L2) :-
	r(H1,H2),append(H2,T2,L2),!,
	replace(T1,T2).
replace([H|T1],[H|T2]) :-
	replace(T1,T2).


r(' ',['%','2','0']).
