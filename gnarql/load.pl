:- module(load,[load/1,load/2]).

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
	atom_concat('file://',Dir,Base),
	load(Dir,Base).
load(Dir,BaseURI) :-
	forall(
		( walk(Dir,Walk),
		  atom_concat(Dir,Relative,Walk),
		  encode(Relative,RelativeWWW),
		  format(atom(URI),'~w~w/',[BaseURI,RelativeWWW]),
		  format(atom(Wildcard),'~w/~w',[Walk,'*.rdf']),
		  expand_file_name(Wildcard,Files),
		  member(File,Files),
		  nl,format(' - Loading ~w\n',File)
		  %convert_path(Walk,WalkWWW),
		  %convert_path(URI,URI2)
		  %format(atom(BaseURI),'file://~w/',[WalkWWW])
		  ),
		  catch(rdf_load(File,[base_uri(URI)]), _, print('caught exception while loading !'))
		).


% in case there are weird character in the relative path
encode(Relative,WWWRelative) :-
	concat_atom(List,'/',Relative),
	encode_all(List,WWWList),
	concat_atom(WWWList,'/',WWWRelative).
encode_all([],[]).
encode_all([H|T],[WH|WT]) :-
	www_form_encode(H,WH),
	encode_all(T,WT).


