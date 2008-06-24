#!/usr/local/bin/pl -g serql_welcome -L0 -G0 -T0 -s

:- dynamic
        user:file_search_path/2.
:- multifile
        user:file_search_path/2.

:- prolog_load_context(directory, Dir),
   atom_concat(Dir,'/SeRQL',SeRQLDir),
   asserta(user:file_search_path(serql, SeRQLDir)).

:- load_files([ serql(load)
              ],
              [ silent(true)
              ]).



entailment(Ent) :- settings:set_setting(serql_parms:default_entailment, Ent).


server :-
        serql_server([port(2105)]).

server(Port) :-
        serql_server([port(Port)]).


:- rdf_db:rdf_register_ns(pc,'http://purl.org/ontology/playcount/').
:- use_module(library('semweb/rdf_http_plugin')).

crawl :-
	findall(Musicbrainz,rdf_db:rdf(_,pc:object,Musicbrainz),Mbzs),
	forall(member(M,Mbzs),rdf_db:rdf_load(M)),
	findall(Bbc,rdf_db:rdf(Bbc,pc:playcount,_),BBCs),
	forall(member(U,BBCs),(debug_uri(U,V),rdf_db:rdf(load(V)))).

debug_uri(U,V) :-
	concat_atom(L,'#',U),
	L = [Base,_],
	atom_concat(Base,'.rdf',V).

