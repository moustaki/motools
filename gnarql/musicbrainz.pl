/**
 * Simple interface to MBZ web service
 * Yves Raimond, C4DM, Queen Mary, University of London
 */

:- module(musicbrainz,[
		find_artist_id/3
	,	find_release_id/3
	,	find_track_id/3
	,	mbz_url_to_id/2
	]).

:- use_module(library('http/http_open')).

webservice('http://musicbrainz.org/ws/1/').

/**
 * Find artist's MBZ Id (and associated confidence)
 * given a name
 */
find_artist_id(Name,Id,Score) :-
        webservice(NS),
        www_form_encode(Name,NameWWW),
        format(atom(ToGet),'~wartist/?type=xml&name=~w',[NS,NameWWW]),
        http_open(ToGet,Stream,[]),
        new_sgml_parser(Parser,[]),
        sgml_parse(Parser,[source(Stream),document(Document)]),close(Stream),
        parse_mbz_results(Document,Id,Score).

/**
 * Find release MBZ Id given its title
 */
find_release_id(Name,Id,Score) :-
        webservice(NS),
        www_form_encode(Name,NameWWW),
        format(atom(ToGet),'~wrelease/?type=xml&title=~w',[NS,NameWWW]),
        http_open(ToGet,Stream,[]),
        new_sgml_parser(Parser,[]),
        sgml_parse(Parser,[source(Stream),document(Document)]),close(Stream),
        parse_mbz_results(Document,Id,Score).

/**
 * Find track MBZ Id given its title
 */
find_track_id(Name,Id,Score) :-
	webservice(NS),
	www_form_encode(Name,NameWWW),
	format(atom(ToGet),'~wtrack/?type=xml&title=~w',[NS,NameWWW]),
	http_open(ToGet,Stream,[]),
	new_sgml_parser(Parser,[]),
	sgml_parse(Parser,[source(Stream),document(Document)]),close(Stream),
	parse_mbz_results(Document,Id,Score).

/**
 * Parses XML results
 * Only parses out results with an associated score
 */
parse_mbz_results(Document,Id,Score) :- 
	member(element(metadata,_,[element(_,_,RList)]),Document), 
	member(element(_,RAtt,_),RList),
	member(id=Id,RAtt),
	member('ext:score'=ScoreAt,RAtt),
	atom_to_term(ScoreAt,Score,[]).


/**
 * A small tool to parse MBZ URLs and get back 
 * the MBZ ID
 */
mbz_url_to_id(MbzURL,ID) :-
	atom_chars(MbzURL,Chars),
	reverse(Chars,CharsR),
	split_at_first_slash(CharsR,SplitR),
	reverse(SplitR,Split),
	atom_chars(ID,Split).

split_at_first_slash(['/'|_],[]) :-!.
split_at_first_slash([H|T1],[H|T2]) :-
	split_at_first_slash(T1,T2).

