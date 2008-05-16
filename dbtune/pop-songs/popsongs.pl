:- module(popsongs,[load/0]).

:- use_module(library('semweb/rdf_db')).
:- use_module(library('semweb/rdf_http_plugin')).
:- use_module(library('semweb/rdf_persistency')).
:- use_module(library('http/http_open')).
:- use_module(library('semweb/rdf_turtle')).


:- rdf_attach_db(db,[]).

load :-
	rdf_load('index.ttl'),!,
	findall(T,rdf(_,rdfs:seeAlso,T),Ts),!,
	forall(member(T,Ts),(rdf_load(T))).


