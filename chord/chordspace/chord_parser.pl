:- module(chord_parser,[chord/4,tokenise/2,parse/2]).

/**
 * A SWI DCG for parsing chord textual representation
 * as defined in Harte, 2005 (ISMIR proceedings)
 *
 * Yves Raimond, C4DM, Queen Mary, University of London
 */

:- use_module(library('semweb/rdf_db')).


parse(ChordSymbol,RDF) :-
	tokenise(ChordSymbol,Tokens),
	phrase(chord(ChordSymbol,RDF),Tokens).


% DCG

namespace('http://purl.org/ontology/chord/symbol/').

chord(Symbol,
	[
		rdf(ID,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://purl.org/ontology/chord/Chord')
	,	rdf(ID,'http://www.w3.org/2002/07/owl#sameAs','http://purl.org/ontology/chord/noChord')
	]
	) -->
	{namespace(NS),atom_concat(NS,Symbol,ID)},
	['N'].
chord(Symbol,
	[
		rdf(ID,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://purl.org/ontology/chord/Chord')
	,	rdf(ID,'http://purl.org/ontology/chord/root',NoteURI)
	,	rdf(ID,'http://purl.org/ontology/chord/base_chord',ShorthandURI)
	|	Tail
	]
	) --> 
	{namespace(NS),atom_concat(NS,Symbol,ID)},
	note(NoteURI,T1), 
	[':'],
	shorthand(ShorthandURI),
	optdegreelist(ID,T2),
	optdegree(ID,T3),
	!,
	{flatten([T1,T2,T3],Tail)}.
chord(Symbol,
	[
		rdf(ID,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://purl.org/ontology/chord/Chord')
	,	rdf(ID,'http://purl.org/ontology/chord/root',NoteURI)
	|	Tail
	]
	) -->
	{namespace(NS),atom_concat(NS,Symbol,ID)},
	note(NoteURI,T1),
	[':'],
	['('],
	degreelist(ID,T2),
	[')'],
	optdegree(ID,T3),!,
	{flatten([T1,T2,T3],Tail)}.
chord(Symbol,
	[
		rdf(ID,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://purl.org/ontology/chord/Chord')
	,	rdf(ID,'http://purl.org/ontology/chord/root',NoteURI)
	,	rdf(ID,'http://purl.org/ontology/chord/base_chord','http://purl.org/ontology/chord/maj')
	|	Tail
	]
	) -->
	{namespace(NS),atom_concat(NS,Symbol,ID)},
	note(NoteURI,T1),
	optdegree(ID,T2),!,
	{append(T1,T2,Tail)}.
chord([]) --> [].
	

note(ID,[
		rdf(ID,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://purl.org/ontology/chord/Note')
	,	rdf(ID,'http://purl.org/ontology/chord/modifier',Modifier)
	,	rdf(ID,'http://purl.org/ontology/chord/natural',NoteURI)	
	]) -->
	{rdf_bnode(ID)},
	natural(NoteURI),
	modifier(Modifier),!.
note(NoteURI,[]) -->
        natural(NoteURI).

optdegreelist(ID,Triples) -->
	['('],degreelist(ID,Triples),[')'],!.
optdegreelist(_,[]) --> [].

optdegree(ID,[rdf(ID,'http://purl.org/ontology/chord/bass',BassNode),rdf(BassNode,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://purl.org/ontology/chord/ScaleInterval')|Triples]) -->
	{rdf_bnode(BassNode)},
	['/'],degree(BassNode,Triples),!.
optdegree(_,[]) --> [].

natural('http://purl.org/ontology/chord/note/A') --> ['A'].
natural('http://purl.org/ontology/chord/note/B') --> ['B'].
natural('http://purl.org/ontology/chord/note/C') --> ['C'].
natural('http://purl.org/ontology/chord/note/D') --> ['D'].
natural('http://purl.org/ontology/chord/note/E') --> ['E'].
natural('http://purl.org/ontology/chord/note/F') --> ['F'].
natural('http://purl.org/ontology/chord/note/G') --> ['G'].

modifier('http://purl.org/ontology/chord/flat') --> ['b'].
modifier('http://purl.org/ontology/chord/sharp') --> ['s']. %will perhaps have to change it
modifier('http://purl.org/ontology/chord/doubleflat') --> ['b','b'].
modifier('http://purl.org/ontology/chord/doublesharp') --> ['s','s'].


degreelist(URI,[
		rdf(URI,'http://purl.org/ontology/chord/without_interval',Interval)
	,	rdf(Interval,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://purl.org/ontology/chord/ScaleInterval')
	|	Tail
	]) --> 
	{rdf_bnode(Interval)},
	['*'],
	degree(Interval,T1),
	[','],
	degreelist(URI,T2),
	{append(T1,T2,Tail)}.
degreelist(URI,[
		rdf(URI,'http://purl.org/ontology/chord/without_interval',Interval)
	,	rdf(Interval,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://purl.org/ontology/chord/ScaleInterval')
	|	Tail
	]) --> 
	['*'],
	{rdf_bnode(Interval)},
	degree(Interval,Tail).
degreelist(URI,[
		rdf(URI,'http://purl.org/ontology/chord/interval',Interval)
	,	rdf(Interval,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://purl.org/ontology/chord/ScaleInterval')
	|	Tail
	]) -->
	{rdf_bnode(Interval)},
	degree(Interval,T1),
	[','],
	degreelist(URI,T2),
	{append(T1,T2,Tail)}.
degreelist(URI,[
		rdf(URI,'http://purl.org/ontology/chord/interval',Interval)
	,	rdf(Interval,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://purl.org/ontology/chord/ScaleInterval')
	|	Tail
	]) -->
	{rdf_bnode(Interval)},
	degree(Interval,Tail).


degree(IntervalURI,[rdf(IntervalURI,'http://purl.org/ontology/chord/degree',literal(type('http://www.w3.org/2001/XMLSchema#int',Interval)))]) -->
	interval(Interval).
%No more than two modifiers - hardcoded
degree(IntervalURI,
	[
		rdf(IntervalURI,'http://purl.org/ontology/chord/modifier',ModifierURI)
	,	rdf(IntervalURI,'http://purl.org/ontology/chord/degree',literal(type('http://www.w3.org/2001/XMLSchema#int',Interval)))
	]) --> 
	modifier(ModifierURI),
	interval(Interval).


interval(N) --> 
	[N], 
	{member(N,['1','2','3','4','5','6','7','8','9','10','11','12'])}.

shorthand('http://purl.org/ontology/chord/maj') --> 
	['maj'].
shorthand('http://purl.org/ontology/chord/min') --> 
	['min'].
shorthand('http://purl.org/ontology/chord/dim') --> 
	['dim'].
shorthand('http://purl.org/ontology/chord/aug') -->
	['aug'].
shorthand('http://purl.org/ontology/chord/maj7') -->
	['maj7'].
shorthand('http://purl.org/ontology/chord/min7') -->
	['min7'].
shorthand('http://purl.org/ontology/chord/seventh') -->
	['7'].
shorthand('http://purl.org/ontology/chord/dim7') -->
	['dim7'].
shorthand('http://purl.org/ontology/chord/hdim7') -->
	['hdim7'].
shorthand('http://purl.org/ontology/chord/minmaj7') -->
	['minmaj7'].
shorthand('http://purl.org/ontology/chord/maj6') -->
	['maj6'].
shorthand('http://purl.org/ontology/chord/min6') -->
	['min6'].
shorthand('http://purl.org/ontology/chord/ninth') -->
	['9'].
shorthand('http://purl.org/ontology/chord/maj9') -->
	['maj9'].
shorthand('http://purl.org/ontology/chord/min9') -->
	['min9'].
shorthand('http://purl.org/ontology/chord/sus4') -->
	['sus4'].
shorthand('http://purl.org/ontology/chord/sus2') -->
	['sus2'].
	
%tokeniser 

%tokens - the order is actually important (longer first)

token(minmaj7).
token(maj9).
token(maj7).
token(maj6).
token(maj).
token(min9).
token(min7).
token(min6).
token(min).
token(dim7).
token(dim).
token(aug).
token('7').
token(hdim7).
token('9').
token(sus4).
token(sus2).

token('A').
token('B').
token('C').
token('D').
token('E').
token('F').
token('G').

token('10').
token('11').
token('12').
token('1').
token('2').
token('3').
token('4').
token('5').
token('6').
token('7').
token('8').
token('9').

%token('#').
token(s).
token(':').
token('b').
token('/').
token('(').
token(')').
token(',').
token('*').
token('N').


tokenise(Atom,Tokens) :-
	atom_chars(Atom,Chars),
	tokenise_l(Chars,Tokens),!.
tokenise_l([],[]) :- !.
tokenise_l(Chars,[Token|Tail]) :-
	grab_token(Chars,Token,CharRest),
	tokenise_l(CharRest,Tail).

grab_token([H|T1],Atom,CharRest) :-
	token(Token),atom_chars(Token,[H|T2]),
	grab_token2(T1,T2,H,Atom,CharRest).
grab_token2(Tail,[],Atom,Atom,Tail) :- !.
grab_token2([H|T1],[H|T2],At,Atom,CharRest) :-
	atom_concat(At,H,NewAt),
	grab_token2(T1,T2,NewAt,Atom,CharRest).



