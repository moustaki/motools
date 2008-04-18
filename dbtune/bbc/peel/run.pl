#!/usr/local/bin/pl -g serql_welcome -L0 -G0 -T0 -s

:- dynamic
        user:file_search_path/2.
:- multifile
        user:file_search_path/2.

:- prolog_load_context(directory, Dir),
   atom_concat(Dir,'/p2r/SeRQL',SeRQLDir),
   asserta(user:file_search_path(serql, SeRQLDir)).

:- load_files([ serql(load)
              ],
              [ silent(true)
              ]).

:- use_module('p2r/p2r_entailment').
:- use_module('p2r/rdf_dump').
:- use_module('p2r/rdf_compile').

entailment(Ent) :- settings:set_setting(serql_parms:default_entailment, Ent).

server :-
        serql_server([port(2106)]).

server(Port) :-
        serql_server([port(Port)]).



:- use_module(peel_match).

:- 
 nl,
 writeln('-----------------'),
 nl,
 writeln(' - 1) Load your match file and the corresponding prolog modules'),
 writeln(' - 2) CODE: entailment(p2r) (changing the default entailment to the one defined in p2r)'),
 nl,
 writeln(' Then, to make things go faster, you can "compile" all possible RDF statements (therefore the system will no more look dynamically for prolog predicates when resolving a RDF query)'),
 writeln(' - CODE: '),
 writeln('   - 1st time: Load match files, prolog modules, and run init_db,rdf_compile.'),
 writeln('   - nth time: init_db, entailment(none) (or rdf, or rdfs, or rdfslite...)'),
 nl,
 writeln(' You can also dump everything in a rdf/xml file using rdf_dump/0'),
 nl,
 writeln(' - Then, run the server using server/0 or server(+Port)'),nl,
 writeln('-----------------').

