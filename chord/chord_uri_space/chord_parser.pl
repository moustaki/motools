:- module(chord_parser,[chord/3]).

/**
 * A SWI DCG for parsing chord textual representation
 * as defined in Harte, 2005 (ISMIR proceedings)
 *
 * Yves Raimond, C4DM, Queen Mary, University of London
 */

:- use_module(library('semweb/rdf_db')).

chord(
	[
		rdf(ID,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://purl.org/ontology/chord/Chord')
	,	rdf(ID,'http://purl.org/ontology/chord/root',NoteURI)
	,	rdf(ID,'http://purl.org/ontology/chord/shorthand',ShorthandURI)
	|	Tail
	]
	) --> 
	{rdf_bnode(ID)},
	{writeln(coucou)},
	note(NoteURI,T1), 
	[':'],
	shorthand(ShorthandURI),
	optdegreelist(ID,T2),
	optdegree(ID,T3),
	!,
	{flatten([T1,T2,T3],Tail)}.
chord(
	[
		rdf(ID,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://purl.org/ontology/chord/Chord')
	,	rdf(ID,'http://purl.org/ontology/chord/root',NoteURI)
	|	Tail
	]
	) -->
	{rdf_bnode(ID)},
	note(NoteURI,T1),
	[':'],
	['('],
	degreelist(ID,T2),
	[')'],
	optdegree(ID,T3),!,
	{flatten([T1,T2,T3],Tail)}.
chord(
	[
		rdf(ID,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://purl.org/ontology/chord/Chord')
	,	rdf(ID,'http://purl.org/ontology/chord/root',NoteURI)
	|	Tail
	]
	) -->
	{rdf_bnode(ID)},
	note(NoteURI,T1),
	optdegree(ID,T2),!,
	{append(T1,T2,Tail)}.
chord([]) --> [].
	

note(NoteURI,[
		rdf(NoteURI,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://purl.org/ontology/chord/Note')
	,	rdf(NoteURI,'http://purl.org/ontology/chord/modifier',Modifier)
	,	rdf(NoteURI,'http://purl.org/ontology/chord/natural',NoteURI)	
	]) -->
	natural(NoteURI),
	modifier(Modifier),!.
note(NoteURI,[]) -->
        natural(NoteURI).

optdegreelist(ID,Triples) -->
	['('],degreelist(ID,Triples),[')'],!.
optdegreelist(_,[]) --> [].

optdegree(ID,Triples) -->
	['/'],degree(ID,Triples),!.
optdegree(_,[]) --> [].

natural('http://purl.org/ontology/chord/note/A') --> ['A'].
natural('http://purl.org/ontology/chord/note/B') --> ['B'].
natural('http://purl.org/ontology/chord/note/C') --> ['C'].
natural('http://purl.org/ontology/chord/note/D') --> ['D'].
natural('http://purl.org/ontology/chord/note/E') --> ['E'].
natural('http://purl.org/ontology/chord/note/F') --> ['F'].
natural('http://purl.org/ontology/chord/note/G') --> ['G'].

modifier('http://purl.org/ontology/chord/note/flat') --> ['b'].
modifier('http://purl.org/ontology/chord/note/sharp') --> ['#']. %will perhaps have to change it
modifier('http://purl.org/ontology/chord/doubleflat') --> ['b','b'].
modifier('http://purl.org/ontology/chord/doublesharp') --> ['#','#'].


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
		rdf(URI,'http://purl.org/ontology/chord/with_interval',Interval)
	,	rdf(Interval,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://purl.org/ontology/chord/ScaleInterval')
	|	Tail
	]) -->
	{rdf_bnode(Interval)},
	degree(Interval,T1),
	[','],
	degreelist(URI,T2),
	{append(T1,T2,Tail)}.
degreelist(URI,[
		rdf(URI,'http://purl.org/ontology/chord/with_interval',Interval)
	,	rdf(Interval,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://purl.org/ontology/chord/ScaleInterval')
	|	Tail
	]) -->
	{rdf_bnode(Interval)},
	degree(Interval,Tail).


degree(IntervalURI,[rdf(IntervalURI,'http://purl.org/ontology/chord/degree',literal(type(Interval,'http://www.w3.org/2001/XMLSchema#int')))]) -->
	interval(Interval).
%No more than two modifiers - hardcoded
degree(IntervalURI,
	[
		rdf(IntervalURI,'http://purl.org/ontology/chord/modifier',ModifierURI)
	,	rdf(IntervalURI,'http://purl.org/ontology/chord/degree',literal(type(Interval,'http://www.w3.org/2001/XMLSchema#int')))
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


