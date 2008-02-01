:- module(server, [server/0]).

:- use_module(library('http/thread_httpd')).
:- use_module(library('http/http_client')).
:- use_module(library('http/http_mime_plugin')).


ns('http://dbtune.org/people/').


server(Port, Options) :-
        http_server(reply,[ port(Port),timeout(20)| Options]).


reply(Request) :-
	member(method(post), Request), !,
	http_read_data(Request,Data,[]),
	member((turtle=Turtle),Data),
	member((name=Name),Data),
	((exists_directory(Name),!);(make_directory(Name))),
	ns(NS),
	format(atom(File),'~w/content.ttl',[Name]),
	format(user_output,[' - Dumping ~w\n',[File]),
	open(File,write,S),
	write(S,Turtle),
	close(S),
	atom_concat(NS,File,URL),
	throw(http_reply(see_other(URL),[])).




server :- server(1112,[]).

