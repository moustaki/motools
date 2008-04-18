:- module(csv,[csv/1,parse/1,save_to/1,reset/0]).

/**
 * A small Prolog module to parse CSV file into Prolog
 *
 * Yves Raimond, C4DM, QMUL
 */

:-dynamic csv/1.
parse(File) :-
	open(File,read,S,[]),
	forall(
		line(S,Line)
	,
		(parse_line(Line,List),assert(csv(List)))
		).
reset :- retractall(csv(_)).
save_to(File) :-
	open(File,write,S,[]),
	forall(csv(X),
		(
			write_term(S,csv(X),[quoted(true)]),write(S,'.\n')
		)),close(S).

line(S,Line) :-
	line(S,[],Line).
line(S,Line,Line) :-
	at_end_of_stream(S),!.
line(S,LineSoFar,Line) :-
	get_char(S,Char),
	(Char = '\n' -> (LineSoFar=Line;line(S,[],Line));(
		append(LineSoFar,[Char],Line2),
		line(S,Line2,Line)
		)).
parse_line(Line,List) :-
	parse_line_l_out(Line,'',List).
parse_line_l_out([],At,[At]):-!.
parse_line_l_out([','|T1],At,[At|T2]) :-
	!,
	parse_line_l_out(T1,'',T2).
parse_line_l_out(['"'|T1],'',T2) :-
	!,
	parse_line_l_in(T1,'',T2).
parse_line_l_out([H|T1],At,T2) :-
	atom_concat(At,H,NewAt),
	parse_line_l_out(T1,NewAt,T2).
parse_line_l_in(['\\','"'|T1],At,T2) :-
	!,
	atom_concat(At,'"',NewAt),
	parse_line_l_in(T1,NewAt,T2).
parse_line_l_in(['"',','|T1],At,[At|T2]) :-
	!,
	parse_line_l_out(T1,'',T2).
parse_line_l_in(['"'|_],At,[At]) :- !.
parse_line_l_in([H|T1],At,T2) :-
	atom_concat(At,H,NewAt),
	parse_line_l_in(T1,NewAt,T2).


:- 
	nl,
	writeln(' - Usage: '),nl,
	writeln(' *  parse(''file.csv''). to parse a CSV file into csv/1 predicates'),
	writeln(' *  save_to(''file.pl''). saves every available csv/1 predicates in a Prolog file'),
	writeln(' *  reset. resets the csv/1 database'),nl.

