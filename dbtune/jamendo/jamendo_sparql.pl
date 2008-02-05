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


:- use_module(p2r_entailment).
:- use_module(rdf_compile).
:- use_module(library('semweb/rdf_persistency')).


entailment(Ent) :- settings:set_setting(serql_parms:default_entailment, Ent).

%Jamendo specific stuff
:- use_module(jamendo_ns).

jamendo_p2r :-
	use_module(jamendo_xml),
	use_module(jamendo),
	use_module(jamendo_match).


server :-
        serql_server([port(2105)]).

server(Port) :-
        serql_server([port(Port)]).



:-
 nl,
 writeln(' - Jamendo RDF server'),
 writeln('   Yves Raimond, Centre for Digital Music, Queen Mary, University of London'),
 nl,
 writeln(' - you can dump all available RDF statements in one file by running ''rdf_dump.'''),
 nl,
 writeln('USAGE'),
 writeln(' --------------------------------'),nl,
 writeln(' - Two choices:'),nl,
 writeln('   * Use P2R (slow, but dynamic, use that if you wrap web services, DBs, ...'),
 writeln('     CODE: jamendo_p2r,compile,entailment(p2r).'),
 nl,
 writeln('   * Use a RDF dump (fast, but static)'),
 writeln('     CODE: (1st time) jamendo_p2r,init_db,rdf_compile (nth time) init_db,entailment(none)'),
 writeln('     You can reset the DB by deleting the db/ directory'),
 nl,
 writeln(' --------------------------------'),
 nl,
 writeln(' - Then, launch the server using server/0 or server(+Port)'),nl.

