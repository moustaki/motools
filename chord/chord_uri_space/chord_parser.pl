:- module(chord_parser,[chord/2]).

/**
 * A SWI DCG for parsing chord textual representation
 * as defined in Harte, 2005 (ISMIR proceedings)
 *
 * Yves Raimond, C4DM, Queen Mary, University of London
 */

chord --> 
	note, 
	[':'],
	shorthand,
	optdegreelist,
	optdegree,!.
chord -->
	node,
	[':'],
	['('],
	degreelist,
	[')'],
	optdegree,!.
chord -->
	note,
	optdegree,!.
chord.
	

note --> 
	natural.
node -->
	note,
	modifier.

optdegreelist -->
	['('],degreelist,[')'],!.
optdegreelist --> [].

optdegree -->
	['/'],degree,!.
optdegree --> [].

natural --> ['A'].
natural --> ['B'].
natural --> ['C'].
natural --> ['D'].
natural --> ['E'].
natural --> ['F'].
natural --> ['G'].

modifier --> ['b'].
modifier --> ['#']. %will perhaps have to change it

degreelist --> 
	['*'],!,
	degree,
	degreelist.
degreelist --> 
	degree,!,
	degreelist.
degreelist --> [].

degree -->
	interval.
degree --> 
	modifier,
	degree.

interval --> 
	[N], 
	{member(N,['1','2','3','4','5','6','7','8','9','10','11','12'])}.

shorthand --> 
	['maj'].
shorthand --> 
	['min'].
shorthand --> 
	['dim'].
shorthand -->
	['aug'].
shorthand -->
	['maj7'].
shorthand -->
	['min7'].
shorthand -->
	['7'].
shorthand -->
	['dim7'].
shorthand -->
	['hdim7'].
shorthand -->
	['minmaj7'].
shorthand -->
	['maj6'].
shorthand -->
	['min6'].
shorthand -->
	['9'].
shorthand -->
	['maj9'].
shorthand -->
	['min9'].
shorthand -->
	['sus4'].


