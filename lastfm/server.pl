:- module(server, [server/0]).

:- use_module(library('http/thread_httpd')).
:- use_module(log).
:- use_module(lastfm_scrobbles).
:- use_module(lastfm_friends).
:- use_module(library('semweb/rdf_db')).


server(Port, Options) :-
        http_server(reply,[ port(Port),timeout(20)| Options]).



reply(Request) :-
	member(path(Path),Request),
	atom_concat('/',UserRdf,Path),
	atom_concat(User,'.rdf',UserRdf),!,
	format('Content-type: application/rdf+xml~n~n', []),
	current_output(S),
	log:log('Generating RDF scrobble for ~w',[User]),
	scrobble_rdf(User,Triples1),
	friends_rdf(User,Triples2),
	append(Triples1,Triples2,Triples3),
	rdf_global_term(Triples3,Triples),
	rdf_write_xml(S,Triples).

reply(Request) :-
	member(path(Path),Request),
	atom_concat('/',User,Path),!,
	host(H),
	format(atom(Redirect),'~w/~w.rdf',[H,User]),
	throw(http_reply(see_other(Redirect),[])).
	
	


server :- 
	server(3060,[]),nl,
	writeln(' - Server launched'),nl. 
        

