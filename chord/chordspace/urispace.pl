:- module(urispace,[init/0]).


:- use_module(library('http/thread_httpd')).
:- use_module(library('semweb/rdf_db')).
:- use_module(log).
:- use_module(chord_parser).

:- style_check(-discontiguous).

server(Port, Options) :-
        http_server(reply,[ port(Port),timeout(20)| Options]).



namespace('http://purl.org/ontology/chord/symbol').

/**
 * Handles documents
 */
reply(Request) :-
	log:log(Request),
	member(path(Path),Request),
	%atom_concat(SymbolT,'.rdf',Path),
	%atom_concat('/',Symbol,SymbolT),
	atom_concat('/',Symbol,Path),
	!,
	process(Symbol).

process(Symbol) :-
	(parse(Symbol,RDF) ->
		(format('Content-type: application/rdf+xml~n~n', []),
		current_output(S),
		rdf_write_xml(S,RDF));
		(
		throw(http_reply(server_error('The specified chord symbol is not valid~n~n')))
		)).

/**
 * Sends back 303 to RDF document describing the resource
 */
%reply(Request) :-
%	member(path(Path),Request),
%	member(accept(AcceptHeader),Request),
%	log:log('Accept header: ~w ',[AcceptHeader]),
%	accept_rdf(AcceptHeader),
%	!,
%	namespace(NS),
%	format(atom(Redirect),'~w~w.rdf',[NS,Path]),
%	log:log('Sending a 303 towards ~w',Redirect),
%	throw(http_reply(see_other(Redirect),[])).

accept_rdf('application/rdf+xml').
accept_rdf('text/xml').
accept_rdf(AcceptHeader) :-
	sub_atom(AcceptHeader,_,_,_,'application/rdf+xml').
accept_rdf(AcceptHeader) :-
        sub_atom(AcceptHeader,_,_,_,'text/xml').
%remove this, otherwise it will always serve rdf
accept_rdf(_).

/**
 * Sends back towards the default representation of the resource
 * (usually html)
 */

html('http://www4.wiwiss.fu-berlin.de/rdf_browser/?browse_uri=').
reply(Request) :-
        member(path(Path),Request),
        !,
        html(Html),namespace(Namespace),
	format(atom(Redirect),'~w~w~w',[Html,Namespace,Path]),
	log:log('Sending a 303 towards ~w',Redirect),
        throw(http_reply(see_other(Redirect),[])).

port(1111).
init :- 
        port(P),
        server(P,[]),
        nl,
        writeln(' - Server launched'),nl.

:-
 nl,writeln('----------------'),nl,
 writeln(' - Launch the server on port 1111 by running ?-init.'),
 nl,writeln('----------------'),nl.


