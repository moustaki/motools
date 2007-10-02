#!/usr/local/bin/pl -g serql_welcome -L0 -G0 -T0 -s


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

server :-
        serql_server([port(2020)]).

server(Port) :-
        serql_server([port(Port)]).

:- use_module(namespaces).
:- use_module(load).
:- use_module(library('semweb/rdf_persistency')).
:- consult(config).
:- use_module(control).

:-
	server,admin_interface.
:- 
	rdf_db:rdf_attach_db('db',[]).

load :- 
	music_path(Path),
	load(Path).

