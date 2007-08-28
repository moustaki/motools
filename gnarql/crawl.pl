:- module(crawl,[crawl/1, crawl_from_local/0]).

:- prolog_load_context(directory, Dir),
   atom_concat(Dir,'/swic',SWICDir),
   asserta(user:file_search_path(swic, SWICDir)).

:- use_module(library('semweb/rdf_db')) .
:- use_module('rdf_http_plugin').
%:- use_module('swic/swic').
%:- use_module('swic/query').
%:- use_module('swic/sparql').
%:- use_module('swic/namespaces').

crawl(URI) :-
	rdf_load(URI).
%or load swic, and <?> [rdf(URI,_,_,_)].

crawl_from_local :- 
	music_path(Path),
	atom_concat('file://',Path,PathURI),
	findall((S,P,O,Filename:LineNum),
	 		(
				rdf_db:rdf(S,P,O,Filename:LineNum),
				atom_concat(PathURI,_,Filename)
			),
 			Quads),
	(forall((member((S,P,O,G), Quads),atom_concat('http://',_,S)),
		   (format(' File : ~w : Gonna crawl ~w',[G,S]),nl,crawl(S))
		  ); true),
	forall((member((S,P,O,G), Quads),atom_concat('http://',_,O)),
		   (format(' File : ~w : Gonna crawl ~w',[G,O]),nl,crawl(O))
		  ) .
