:- module(server, [server/0,reset/0]).

:- use_module(library('http/thread_httpd')).
:- use_module(library('http/http_client')).
:- use_module(library('http/http_mime_plugin')).
:- use_module(library('semweb/rdf_db')).
:- use_module(library('semweb/rdf_turtle')).
:- use_module(library('semweb/rdf_persistency')).

ns('http://localhost:3019/').

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

server(Port, Options) :-
        http_server(reply,[ port(Port),timeout(20)| Options]).


reply(Request) :-
    member(path('/'), Request),
	member(method(post), Request), !,
	http_read_data(Request,Data,[]),
	member((rdf=RDF),Data),
    member((type=Type),Data),
	load_data(RDF,Type),
    format('Content-type: text/plain~n~n', []),
	format('RDF document parsed and loaded~n',[]).

reply(Request) :-
    member(path(Path), Request),
    member(method(get), Request),
    concat_atom(['/',Object], Path),!,
    ns(NS),
    parse_url(NS,Parsed),
    member(host(Host),Parsed),
    parse_url(SparqlURL,[protocol(http), host(Host), port(3020)]),
    concat_atom([SparqlURL,'/sparql/?query=describe%20%3C',NS,Object,'%3E'], Redirect),
    throw(http_reply(see_other(Redirect))).

load_data(RDF,Type) :-
	tmp_file(Type,Tmp),
    concat_atom([Tmp,'.',Type],File),
    format(user_output,'~w\n',[File]),
	open(File,write,S),
	write(S,RDF),
	close(S),
    ns(NS),
	rdf_load(File,[base_uri=NS]).


server :- server(3019,[]), serql_server([port(3020)]).
reset :- rdf_reset_db.

