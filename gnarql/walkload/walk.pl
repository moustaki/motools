:- module(walk,[walk/2]).

/**
 * An equivalent of the Python "walk"
 *
 * Yves Raimond, C4DM, QMUL (c) 2007
 */

:- multifile failed_dir/1.
:- dynamic failed_dir/1.

walk(Base,Base).
walk(Base,Walk) :-
	directory(Base,Dir),
	walk(Dir,Walk).

directory(Base,Dir) :-
	format(atom(Wildcard),'~w/~w',[Base,'*']),
	expand_file_name(Wildcard,D),
	member(Dir,D),
	catch(exists_directory(Dir),_,assert(failed_dir(Dir))).



