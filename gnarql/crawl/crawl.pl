:- module(crawl,[crawl/0]).


:- use_module(library('semweb/rdf_db')).
:- consult('../namespaces').

crawl :-
        start_crawl,
        repeat,
        sleep(5),
        \+thread_peek_message(jobs,_),
        findall(R,
                (
                        rdf(G,rdf:type,gnarql:'CrawledSource'),
                        resource_in_graph(R,G),
                        uncrawled_uri(R)
                ),
                Bag),
        forall(member(R,Bag),thread_send_message(jobs,R)),
        fail.


start_crawl :-
        findall(R,(start_graph(G),resource_in_graph(R,G),uncrawled_uri(R)),Bag),
        forall(member(R,Bag),thread_send_message(jobs,R)).



start_graph(G) :-
        rdf(A,rdf:type,gnarql:'MusicCollection'),
        rdf(A,gnarql:path,literal(Path)),
        rdf_source(G),sub_atom(G,_,_,_,Path).

resource_in_graph(R,G) :-
        rdf(_,P,R,G:_),
        R\=literal(_),P\='http://www.w3.org/1999/02/22-rdf-syntax-ns#type'.
resource_in_graph(R,G) :-
        rdf(R,_,_,G:_).

uncrawled_uri(A) :-
        atom_concat('http://',_,A),
        \+((rdf(C,rdf:type,gnarql:'MusicCollection'),sub_atom(A,_,_,_,C))),
        \+rdf(A,rdf:type,gnarql:'CrawledSource').

