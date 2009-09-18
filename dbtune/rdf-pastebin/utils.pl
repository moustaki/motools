:- module(utils, [
        load_interests/0,
        load_basednears/0
    ]).

:- use_module(library('semweb/rdf_db')).
:- use_module(library('semweb/rdf_http_plugin')).

load_all(List) :-
    forall(member(M,List), rdf_load(M)).

:- rdf_register_ns(foaf,'http://xmlns.com/foaf/0.1/').

load_interests :-
    findall(Interest, S^rdf(S,foaf:interest, Interest), Interests),
    load_all(Interests).

load_basednears :-
    findall(Place, S^rdf(S,foaf:based_near, Place), Places),
    load_all(Places).

