:- module(walk,[walk/2]).

/**
 * An equivalent of the Python "walk"
 *
 * Yves Raimond, C4DM, QMUL (c) 2007
 */


walk(Base,Base).
walk(Base,Walk) :-
	directory(Base,Dir),
	walk(Dir,Walk).

directory(Base,Dir) :-
	format(atom(Wildcard),'~w/~w',[Base,'*']),
	expand_file_name(Wildcard,D),
	member(Dir,D),
	exists_directory(Dir).



