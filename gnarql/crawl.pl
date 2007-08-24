:- module(crawl,[crawl/1]).

:- prolog_load_context(directory, Dir),
   atom_concat(Dir,'/swic',SWICDir),
   asserta(user:file_search_path(swic, SWICDir)).

:- use_module(library('semweb/rdf_db')) .
:- use_module('swic/swic').
:- use_module('swic/query').
%:- use_module('swic/sparql').
%:- use_module('swic/namespaces').

crawl(URI) :- findall((P,O,G), <?> [rdf(URI, P,O,G)], Triples),
	forall(member((P,O,G), Triples), rdf_assert(URI,P,O,G)),
	length(Triples, N),
	format('Imported ~w triples from ~w', [N, URI]) .

