:- module(server, [server/0]).

:- use_module(library('http/thread_httpd')).
:- use_module(library('http/http_client')).
:- use_module(library('http/http_mime_plugin')).
:- use_module(library('semweb/rdf_db')).
:- use_module(library('semweb/rdf_turtle')).

ns('http://dbtune.org/people/').


server(Port, Options) :-
        http_server(reply,[ port(Port),timeout(20)| Options]).


reply(Request) :-
	member(method(post), Request), !,
	http_read_data(Request,Data,[]),
	format(user_output,'~w\n',[Data]),
	member((turtle=Turtle),Data),
	parse_turtle(Turtle,Triples),
	member((name=Name),Data),
	((exists_directory(Name),!);(make_directory(Name))),
	ns(NS),
	format(atom(File),'~w/content.rdf',[Name]),
	format(user_output,' - Dumping ~w\n',[File]),
	open(File,write,S),
	parse_turtle(Turtle,Triples),
	rdf_write_xml(S,Triples),
	close(S),
	atom_concat(NS,File,URL),
	throw(http_reply(see_other(URL),[])).


parse_turtle(Turtle,Triples) :-
	tmp_file(ttl,Tmp),
	open(Tmp,write,S),
	write(S,Turtle),
	close(S),
	rdf_load_turtle(Tmp,Triples,[base_uri('')]).
	


server :- server(1112,[]).

