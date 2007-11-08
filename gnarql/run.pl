#!/usr/local/bin/pl -g serql_welcome -L1G -G1G -T1G -s


:- dynamic
        user:file_search_path/2.
:- multifile
        user:file_search_path/2.
:- multifile base_uri/1.
:- multifile music_path/1.
:- multifile timeout/1.

:- prolog_load_context(directory, Dir),
   atom_concat(Dir,'/SeRQL',SeRQLDir),
   asserta(user:file_search_path(serql, SeRQLDir)).

:- load_files([ serql(load)
              ],
              [ silent(true)
              ]).

server :-
        serql_server([port(2020)]).

server(Port) :-
        serql_server([port(Port)]).

:- use_module(namespaces).
:- use_module(load).
:- use_module(library('semweb/rdf_persistency')).
:- use_module(control).
:- use_module(crowl).

:-
	server,admin_interface.
attach :- 
	rdf_db:rdf_attach_db('db',[concurrency(1)]).

:- [config].
load :- 
	\+base_uri(_),
	music_path(Path),
	load(Path).
load :- 
	base_uri(Uri),
	music_path(Path),
	load(Path,Uri).

:- crowl:init.

%:- user_db:openid_add_server('http://www.myopenid.com/server',[]).

