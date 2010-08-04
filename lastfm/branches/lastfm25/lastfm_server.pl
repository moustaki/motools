:- module(lastfm_server, 
		[ server/0	
		]).

:- use_module(library('http/thread_httpd')).
:- use_module(library('semweb/rdf_db')).

:- use_module(log).

:- use_module(lastfm_scrobbles).
:- use_module(lastfm_friends).
:- use_module(lastfm_events).
:- use_module(lastfm_config).

/** <module> Last.fm API to RDF converter server

This module is the http server for processing the request from the web frontend.

@author		Yves Raimond
@version 	1.0 
@copyright	Yves Raimond; 2008 - 2010
*/

server(Port, Options) :-
        http_server(reply,[ port(Port),timeout(20)| Options]).

%%	reply(+Request)
%
%	Processes the request and writes the RDF to XML.

reply(Request) :-
	member(path(Path),Request),
	atom_concat('/',UserRdf,Path),
	atom_concat(User,'.rdf',UserRdf),!,
	format('Content-type: application/rdf+xml; charset=UTF-8~n~n', []),
	current_output(S),
	set_stream(S,encoding(utf8)),
	log:log('Generating RDF from Last.fm for ~w',[User]),
	catch(tracks_rdf(User,Triples1),_,Triples1=[]),
	catch(friends_rdf(User,Triples2),_,Triples2=[]),
	catch(events_rdf(User,Triples3),_,Triples3=[]),
	flatten([Triples1,Triples2,Triples3],Triples4),
	rdf_global_term(Triples4,Triples),
	rdf_write_xml(S,Triples).

%%	reply(+Request)
%
%	Redirects to the output RDF on the defined host/1.

reply(Request) :-
	member(path(Path),Request),
	atom_concat('/',User,Path),!,
	host(H),
	format(atom(Redirect),'~w/~w.rdf',[H,User]),
	throw(http_reply(see_other(Redirect),[])).
	
	

%%	server
%
%	Starts the httpd server.
%	Here you can also set the port of this server.

server :- 
	server(3060,[]),nl,
	writeln(' - Server launched'),nl. 
        

