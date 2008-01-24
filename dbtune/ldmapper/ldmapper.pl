:- module(ldmapper,[map/3,map_jamendo_mbz/2]).


:- use_module(library('semweb/rdf_db')).
:- use_module('rdf_http_plugin').
:- use_module(library(rdf)).


% similar_to(Type,Node1,Node2,Confidence)
:- multifile similar_to/4.

% Path to follow (two paths in case the ontologies
% used in the two datasets are not exactly similar)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
path_1([
                'http://xmlns.com/foaf/0.1/made'
        ,       'http://purl.org/ontology/mo/has_track'
        ]).

path_2([
                'http://xmlns.com/foaf/0.1/made'
        ,       'http://purl.org/ontology/mo/has_track'
        ]).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% top-level predicate
% takes the result with the highest confidence, if it is
% more than the threshold
mapping(Node,Mapping) :-
        findall(Confidence-M,map(Node,M,Confidence),Set),
        keysort(Set,ISortedSet),
        reverse(ISortedSet,SortedSet),
        threshold(Threshold),
        cut_list(SortedSet,Cut,Threshold),
        findall(Map,member(_-Map,Cut),Maps),
        flatten(Maps,Mapping2),
        list_to_set(Mapping2,Mapping).


map(Node,Mapping,Confidence) :-
	path_1(Path1),
	path_2(Path2),
	map(Node,_,Path1,Path2,Mapping,0,Confidence).
map(Node1,Node2,[],[],[],CurrentConfidence,Confidence) :-
	similar_to(Node1,Node2,SConfidence),
	Confidence is CurrentConfidence + SConfidence.
map(_,_,[],[],[],Confidence,Confidence).
map(Node1,Node2,[Prop1|TP1],[Prop2|TP2],[rdf(Node1,'http://www.w3.org/2002/07/owl#sameAs',Node2),rdf(NNode1,'http://www.w3.org/2002/07/owl#sameAs',NNode2)|T],CurrentConfidence,Confidence) :-
	similar_to(Node1,Node2,SConfidence),
	NewConfidence is CurrentConfidence + SConfidence,
	findall(NNode1,rdf(Node1,Prop1,NNode1),Bag1),list_to_set(Bag1,Set1),
	findall(NNode2,rdf(Node2,Prop2,NNode2),Bag2),list_to_set(Bag2,Set2),
	member(NNode1,Set1),
	member(NNode2,Set2),
	map(NNode1,NNode2,TP1,TP2,T,NewConfidence,Confidence).
map(Node1,Node2,[Prop1|TP1],[Prop2|TP2],[rdf(Node1,'http://www.w3.org/2002/07/owl#sameAs',Node2),rdf(NNode1,'http://www.w3.org/2002/07/owl#sameAs',NNode2)|T],CurrentConfidence,Confidence) :-
	\+var(Node2),
	format(' - Loading (alternative path) ~w\n',[Node2]),
	rdf_load(Node2),
	findall(NNode1,rdf(Node1,Prop1,NNode1),Bag1),list_to_set(Bag1,Set1),
	findall(NNode2,rdf(Node2,Prop2,NNode2),Bag2),list_to_set(Bag2,Set2),
	member(NNode1,Set1),
	member(NNode2,Set2),
	map(NNode1,NNode2,TP1,TP2,T,CurrentConfidence,Confidence).


similar_to(Node1,Node2,Confidence) :-
	format(' - Loading (main path) ~w\n',[Node1]),
	rdf_load(Node1), 
	rdf(Node1,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',Type),
	(
		atomic(Node2) -> (
			format(' - Loading (alternative path) ~w\n',[Node2]),
			rdf_load(Node2),
			similar_to(Type,Node1,Node2,Confidence)
		);(
			similar_to(Type,Node1,Node2,Confidence),
			format(' - Loading (alternative path) ~w\n',[Node2]),
			rdf_load(Node2)
		)
	).


% Music ontology specific lookup mechanisms / similarity 
% measures
%
% Uses the NLP library of SWI-Prolog for free-text search
% (metaphone algorithm)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
:- use_module(musicbrainz).
:- use_module(library('semweb/rdf_litindex')).

threshold(280).
threshold_artist(90).

% top-level predicate
% takes the result with the highest confidence, if it is
% more than the threshold
map_jamendo_mbz(Node,Mapping) :-
	mapping(Node,Mapping).


similar_to('http://purl.org/ontology/mo/MusicArtist',Node1,Node2,Confidence) :-
	rdf(Node1,'http://xmlns.com/foaf/0.1/name',literal(type(_,Name))),
	find_artist_id(Name,Id,Confidence),
	threshold_artist(T),Confidence > T,
	atom_concat('http://zitgist.com/music/artist/',Id,Node2).

%in case i want to use MBZ web service, also for records
%similar_to('http://purl.org/ontology/mo/Record',Node1,Node2,Confidence) :-
%	rdf(Node1,'http://purl.org/dc/elements/1.1/title',literal(type(_,Title))),
%	find_release_id(Title,Id,Confidence),
%	atom_concat('http://zitgist.com/music/record/',Id,Node2).

similar_to('http://purl.org/ontology/mo/Record',Node1,Node2,100) :-
	rdf(Node1,'http://purl.org/dc/elements/1.1/title',literal(type(_,Title))),
        literal_to_search_spec(Title,Spec),
	rdf_find_literals(Spec,TitleList),
        member(Title2,TitleList),
	rdf(Node2,'http://purl.org/dc/elements/1.1/title',literal(Title2)),
        rdf(Node2,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://purl.org/ontology/mo/Record'),
        Node1\==Node2.

similar_to('http://purl.org/ontology/mo/Track',Node1,Node2,100) :-
	rdf(Node1,'http://purl.org/dc/elements/1.1/title',literal(type(_,Title))),
	literal_to_search_spec(Title,Spec),
	rdf_find_literals(Spec,TitleList),
	member(Title2,TitleList),
	rdf(Node2,'http://purl.org/dc/elements/1.1/title',literal(Title2)),
	rdf(Node2,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://purl.org/ontology/mo/Track'),
	Node1\==Node2.

% in case i want to use mbz web service for track lookup
%similar_to('http://purl.org/ontology/mo/Track',Node1,Node2,Confidence) :-
%	rdf(Node1,'http://purl.org/dc/elements/1.1/title',literal(type(_,Title))),
%	find_track_id(Title,Id,Confidence),
%	atom_concat('http://zitgist.com/music/track/',Id,Node2).

% cheap utils
literal_to_search_spec(Lit,Spec) :-
	%remove_char(Lit,'''',Lit2),
	%remove_char(Lit2,'’',Lit3),
	%remove_char(Lit3,'.',Lit4),
	%concat_atom(List,' ',Lit3),
	%clean_small_words(List,ListCleaned),
	rdf_tokenize_literal(Lit,List),
	search_spec(List,Spec).

search_spec([H],HH) :- integer(H),!,term_to_atom(H,HH).
search_spec([H],case(H)) :- !.
search_spec([H|T1],and(HH,T2)) :-
	integer(H),!,term_to_atom(H,HH),
	search_spec(T1,T2).
search_spec([H|T1],and(case(H),T2)) :-
	search_spec(T1,T2).

remove_char(Lit,Char,Lit2) :-
	concat_atom(List,Char,Lit),
	concat_atom(List,' ',Lit2).

clean_small_words([],[]).
clean_small_words([H|T1],[H|T2]) :-
	atom_chars(H,C), length(C,N), N > 2,
	!,clean_small_words(T1,T2).
clean_small_words([_|T1],T2) :-
	clean_small_words(T1,T2).

cut_list([S-_|_],[],T) :-
        (S < T ; S=T),!.
cut_list([S-H|T1],[S-H|T2],T) :-
        S > T,
        cut_list(T1,T2,T).


