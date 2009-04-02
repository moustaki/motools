#!/usr/local/bin/pl -s -q

:- module(server, [server/0]).

:- use_module(library('http/thread_httpd')).
:- use_module(log).
:- use_module(library('semweb/rdf_db')).
:- use_module(config).


server(Port, Options) :-
        http_server(reply,[ port(Port),timeout(20)| Options]).

reply(Request) :-
	member(path(Path),Request),
	atom_concat('/mbid/',UidRdf,Path),
	atom_concat(Uid,'.rdf',UidRdf),!,
	Uid\='None',
	log(Request),
	format('Content-type: application/rdf+xml; charset=UTF-8~n~n', []),
	current_output(S),
	set_stream(S,encoding(utf8)),
	format(user_output,'Generating RDF profile for myspace uid ~w~n',[Uid]),
	format(atom(Command),'python ~w -m ~w',['artistlookup.py',Uid]),
	log(Command),
	open(pipe(Command),read,C),
	copy_stream_data(C,S),close(C).



reply(Request) :-
	member(path(Path),Request),
	atom_concat('/',Uid,Path),!,
	host(H),
	format(atom(Redirect),'~w/mbid/~w.rdf',[H,Uid]),
	throw(http_reply(see_other(Redirect),[])).

reply(Request) :-
	member(path(Path),Request),
	atom_concat('/',UidRdf,Path),
	atom_concat(Uid,'.rdf',UidRdf),!,
	Uid\='None',
	log(Request),
	format('Content-type: application/rdf+xml; charset=UTF-8~n~n', []),
	current_output(S),
	set_stream(S,encoding(utf8)),
	format(user_output,'Generating RDF profile for myspace uid ~w~n',[Uid]),
	format(atom(Command),'python ~w -n ~w',['artistlookup.py',Uid]),
	log(Command),
	open(pipe(Command),read,C),
	copy_stream_data(C,S),close(C).



reply(Request) :-
	member(path(Path),Request),
	atom_concat('/mbid/',Uid,Path),!,
	host(H),
	format(atom(Redirect),'~w/mbid/~w.rdf',[H,Uid]),
	throw(http_reply(see_other(Redirect),[])).



server :- 
	server(2059,[]),nl,
	writeln(' - Server launched'),nl. 
        
:- server.
