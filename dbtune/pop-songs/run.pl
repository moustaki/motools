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


entailment(Ent) :- settings:set_setting(serql_parms:default_entailment, Ent).


server :-
        serql_server([port(2105)]).

server(Port) :-
        serql_server([port(Port)]).



