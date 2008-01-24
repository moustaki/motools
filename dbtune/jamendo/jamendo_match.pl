:- module(jamendo_match,[]).

:- consult(library('semweb/rdf_db')).

:- use_module(match).

:- consult(jamendo_ns).


/**
 * Class mappings
 */
match:
	(jamendo:artist(Id))
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/artist/',Id]),rdf:type,mo:'MusicArtist')
	].

match:
	(jamendo:album(Id))
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/record/',Id]),rdf:type,mo:'Record')
	].


match:
	(jamendo:track(Id))
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/track/',Id]),rdf:type,mo:'Track')
	,	rdf(pattern(['http://dbtune.org/jamendo/signal/',Id]),mo:published_as,pattern(['http://dbtune.org/jamendo/track/',Id]))
	,	rdf(pattern(['http://dbtune.org/jamendo/signal/',Id]),rdf:type,mo:'Signal')
	,	rdf(pattern(['http://dbtune.org/jamendo/signal/',Id]),mo:time,pattern(['http://dbtune.org/jamendo/interval/',Id]))
	,	rdf(pattern(['http://dbtune.org/jamendo/interval/',Id]),rdf:type,time:'Interval')
	,	rdf(pattern(['http://dbtune.org/jamendo/interval/',Id]),tl:onTimeLine,pattern(['http://dbtune.org/jamendo/timeline/',Id]))
	,	rdf(pattern(['http://dbtune.org/jamendo/performance/',Id]),mo:recorded_as,pattern(['http://dbtune.org/jamendo/signal/',Id]))
	].

/**
 * Property mappings
 */

/**
 * Artists
 */
match:
	(jamendo:artist_dispname(Id,Name))
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/artist/',Id]),foaf:name,literal(type('http://www.w3.org/2001/XMLSchema#string',Name)))
	].

%match:
%	(jamendo:artist_dispname(Id,Name),jamendo_match:mbz_artist(Name,MbzId))
%		eq
%	[
%		rdf(pattern(['http://dbtune.org/jamendo/artist/',Id]),owl:sameAs,pattern(['http://zitgist.com/music/artist/',MbzId]))
%	].

match:
	(jamendo:artist_description(Id,Desc))
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/artist/',Id]),mo:biography,literal(type('http://www.w3.org/2001/XMLSchema#string',Desc)))
	].

match:
	(jamendo:artist_geo(Id,Geo),jamendo_match:geonames(Geo,URI)) 
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/artist/',Id]),foaf:based_near,URI)
	].

match:
	(jamendo:artist_homepage(Id,HomePage)) 
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/artist/',Id]),foaf:homepage,HomePage)
	].

match:
	(jamendo:artist_image(Id,Image))
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/artist/',Id]),foaf:img,Image)
	].

/**
 * Albums
 */
match:
	(jamendo:album_name(Id,Name))
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/record/',Id]),dc:title,literal(type('http://www.w3.org/2001/XMLSchema#string',Name)))
	,	rdf(pattern(['http://dbtune.org/jamendo/record/',Id]),mo:available_as,pattern(['http://www.jamendo.com/get/track/id/album/audio/play/',Id,'/?item_o=track_no_asc&aue=ogg2&n=all']))
	,	rdf(pattern(['http://www.jamendo.com/get/track/id/album/audio/play/',Id,'/?item_o=track_no_asc&aue=ogg2&n=all']),rdf:type,mo:'Playlist')
	,	rdf(pattern(['http://www.jamendo.com/get/track/id/album/audio/play/',Id,'/?item_o=track_no_asc&aue=ogg2&n=all']),dc:format,literal(m3u))
	,	rdf(pattern(['http://dbtune.org/jamendo/record/',Id]),mo:available_as,pattern(['http://www.jamendo.com/get/track/id/album/audio/xspf/',Id,'/?item_o=track_no_asc&aue=ogg2&n=all']))
	,	rdf(pattern(['http://www.jamendo.com/get/track/id/album/audio/xspf/',Id,'/?item_o=track_no_asc&aue=ogg2&n=all']),rdf:type,mo:'Playlist')
	,	rdf(pattern(['http://www.jamendo.com/get/track/id/album/audio/xspf/',Id,'/?item_o=track_no_asc&aue=ogg2&n=all']),dc:format,literal(xspf))
	].

match:
	(jamendo:album_description(Id,Desc))
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/record/',Id]),dc:description,literal(type('http://www.w3.org/2001/XMLSchema#string',Desc)))
	].

match:
	(jamendo:album_artist(Id,ArtistId))
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/record/',Id]),foaf:maker,pattern(['http://dbtune.org/jamendo/artist/',ArtistId]))
	,	rdf(pattern(['http://dbtune.org/jamendo/artist/',ArtistId]),foaf:made,pattern(['http://dbtune.org/jamendo/record/',Id]))
	].

match:
	(jamendo:album_releasedate(Id,Date))
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/record/',Id]),dc:date,literal(Date))
	].

match:
	(jamendo:album_cover(Id,_,_,Cover))
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/record/',Id]),mo:image,Cover)
	].
match:
	(jamendo:album_p2p(Id,ogg3,ed2k,Link))
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/record/',Id]),mo:available_as,Link)
	,	rdf(Link,rdf:type,mo:'ED2K')
	,	rdf(Link,dc:format,literal(ogg3))
	].
match:
        (jamendo:album_p2p(Id,mp32,ed2k,Link))
                eq
        [
                rdf(pattern(['http://dbtune.org/jamendo/record/',Id]),mo:available_as,Link)
        ,       rdf(Link,rdf:type,mo:'ED2K')
        ,       rdf(Link,dc:format,literal(mp32))
        ].
match:
        (jamendo:album_p2p(Id,ogg3,bittorrent,Link))
                eq
        [
                rdf(pattern(['http://dbtune.org/jamendo/record/',Id]),mo:available_as,Link)
        ,       rdf(Link,rdf:type,mo:'Torrent')
        ,       rdf(Link,dc:format,literal(ogg3))
        ].
match:
        (jamendo:album_p2p(Id,mp32,bittorrent,Link))
                eq
        [
                rdf(pattern(['http://dbtune.org/jamendo/record/',Id]),mo:available_as,Link)
        ,       rdf(Link,rdf:type,mo:'Torrent')
        ,       rdf(Link,dc:format,literal(mp32))
        ].

match:
	(jamendo:album_tag(_,Tag)) 
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/tag/',Tag]),tags:tagName,literal(type('http://www.w3.org/2001/XMLSchema#string',Tag)))
	,	rdf(pattern(['http://dbtune.org/jamendo/tag/',Tag]),rdf:type,tags:'Tag')
	].
match:
	(jamendo:album_tag(Id,Tag))
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/record/',Id]),tags:taggedWithTag,pattern(['http://dbtune.org/jamendo/tag/',Tag]))
	].

/**
 * Tracks
 */
match:
	(jamendo:track_album(Id,AlbumId))
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/record/',AlbumId]),mo:track,pattern(['http://dbtune.org/jamendo/track/',Id]))
	,	rdf(pattern(['http://dbtune.org/jamendo/track/',Id]),mo:available_as,pattern(['http://www.jamendo.com/get/track/id/track/audio/play/',Id]))
	,	rdf(pattern(['http://dbtune.org/jamendo/track/',Id]),mo:available_as,pattern(['http://www.jamendo.com/get/track/id/track/audio/xspf/',Id]))
	,	rdf(pattern(['http://www.jamendo.com/get/track/id/track/audio/play/',Id]),rdf:type,mo:'Playlist')
	,	rdf(pattern(['http://www.jamendo.com/get/track/id/track/audio/xspf/',Id]),rdf:type,mo:'Playlist')
	,	rdf(pattern(['http://www.jamendo.com/get/track/id/track/audio/play/',Id]),dc:format,literal(m3u))
	,	rdf(pattern(['http://www.jamendo.com/get/track/id/track/audio/xspf/',Id]),dc:format,literal(xspf))
	].

match:
	(jamendo:track_no(Id,No))
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/track/',Id]),mo:track_number,literal(type('http://www.w3.org/2001/XMLSchema#int',No)))
	].

match:
	(jamendo:track_name(Id,Name))
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/track/',Id]),dc:title,literal(type('http://www.w3.org/2001/XMLSchema#string',Name)))
	].

match:
	(jamendo:track_licenseurl(Id,License))
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/track/',Id]),mo:license,License)
	,	rdf(License,rdf:type,foaf:'Document')
	].
match:
	(jamendo:track_lyrics(Id,Lyrics))
		eq
	[
		rdf(pattern(['http://dbtune.org/jamendo/performance/',Id]),event:factor,pattern(['http://dbtune.org/jamendo/lyrics/',Id]))
	,	rdf(pattern(['http://dbtune.org/jamendo/lyrics/',Id]),rdf:type,mo:'Lyrics')
	,	rdf(pattern(['http://dbtune.org/jamendo/lyrics/',Id]),mo:text,literal(type('http://www.w3.org/2001/XMLSchema#string',Lyrics)))
	].



/**
 * Geo mapping
 */
:- use_module(library('http/http_open')).
:- use_module(library('semweb/rdf_http_plugin')).

geonames('Lithuanie (VL)','http://sws.geonames.org/597427/') :- !.
geonames(JamendoLiteral,URI) :-
	clean_literal(JamendoLiteral,Query),
	concat_atom(['http://ws.geonames.org/search?q=',Query,'&fclass=A','&type=rdf','&maxRows=1'],Url),
	rdf_db:rdf(URI,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://www.geonames.org/ontology#Feature',Url:_),!.
geonames(JamendoLiteral,URI) :-
	clean_literal(JamendoLiteral,Query),
	concat_atom(['http://ws.geonames.org/search?q=',Query,'&fclass=A','&type=rdf','&maxRows=1'],Url),
	rdf_load(Url),
	rdf_db:rdf(URI,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://www.geonames.org/ontology#Feature',Url:_),!.
geonames(JamendoLiteral,URI) :-
	first_word(JamendoLiteral,Query),
	concat_atom(['http://ws.geonames.org/search?q=',Query,'&fclass=A','&type=rdf','&maxRows=1'],Url),
	rdf_db:rdf(URI,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://www.geonames.org/ontology#Feature',Url:_),!.
geonames(JamendoLiteral,URI) :-
        first_word(JamendoLiteral,Query),
        concat_atom(['http://ws.geonames.org/search?q=',Query,'&fclass=A','&type=rdf','&maxRows=1'],Url),
	rdf_load(Url),
        rdf_db:rdf(URI,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://www.geonames.org/ontology#Feature',Url:_),!.

clean_literal(Literal,Cleaned) :-
	atom_chars(Literal,Chars),
	delete(Chars,'(',T1),
	delete(T1,')',T2),
	atom_chars(T3,T2),
	www_form_encode(T3,Cleaned).
first_word(Literal,Q) :-
	atom_chars(Literal,Chars),
	cut(Chars,' ',First),
	atom_chars(F,First),
	www_form_encode(F,Q).
	
cut([Elt|_],Elt,[]) :- !.
cut([H|T],Elt,[H|T2]) :-
	cut(T,Elt,T2).

/**
 * Mbz mapping
 */
:- use_module(musicbrainz).
threshold(90).
reviews('reviews.log').


space_to_plus(Name,Name2) :-
	atom_chars(Name,Chars),
	space_to_plus2(Chars,Chars2),
	atom_chars(Name2,Chars2).
space_to_plus2([],[]).
space_to_plus2([' '|T],['+'|T2]) :-
	!,space_to_plus2(T,T2).
space_to_plus2([H|T],[H|T2]) :-
	space_to_plus2(T,T2).

mbz_track(Name,Uri) :-
	space_to_plus(Name,Name2),
	mbz_track2(Name2,Uri).
mbz_track2(Name,Uri) :-
	findall(uri(Uri,Score),find_track_id(Name,Uri,Score),Results),
	\+ambiguous(Results,_),
	Results=[uri(Uri,_)|_].
mbz_track2(Name,_) :-
	findall(uri(Uri,Score),find_track_id(Name,Uri,Score),Results),
	ambiguous(Results,Reason),
	reviews(Reviews),
	open(Reviews,append,Stream,[]),
	(
			(Reason=uris(List,Score),
			format(atom(T),'\n - Ambiguous track URIs for string "~w"\nMatching results are (with score ~w) :\n',[Name,Score]),
			concat_atom(List,'\n',T2),
			atom_concat(T,T2,T3),
			write(Stream,T3)
			);(
			Reason=uri(A,B),
			format(atom(U),'\n - Not succeeded to find a good enough track result for string "~w"\nBest matching results is ~w with score ~w%',[Name,A,B]),
			write(Stream,U)
			);(
                        Reason=[],
                        format(atom(U),'\n\n - No results for ~w',[Name]),
                        write(Stream,U)
                        )
	),close(Stream),fail.

mbz_artist(Name,Uri) :-
        space_to_plus(Name,Name2),
        mbz_artist2(Name2,Uri).
mbz_artist2(Name,Uri) :-
        findall(uri(Uri,Score),find_artist_id(Name,Uri,Score),Results),
        \+ambiguous(Results,_),
        Results=[uri(Uri,_)|_].
mbz_artist2(Name,_) :-
        findall(uri(Uri,Score),find_artist_id(Name,Uri,Score),Results),
        ambiguous(Results,Reason),
        reviews(Reviews),
        open(Reviews,append,Stream,[]),
        (
                	(Reason=uris(List,Score),
                        format(atom(T),'\n\n - Ambiguous artist URIs for string "~w"\nMatching results are (with score ~w) :\n',[Name,Score]),
                        concat_atom(List,'\n',T2),
                        atom_concat(T,T2,T3),
                        write(Stream,T3)
                        );(
                        Reason=uri(A,B),
                        format(atom(U),'\n\n - Not succeeded to find a good enough artist result for string "~w"\nBest matching results is ~w with score ~w%',[Name,A,B]),
                        write(Stream,U)
                        );(
			Reason=[],
			format(atom(U),'\n\n - No results for ~w',[Name]),
			write(Stream,U)
			)
        ),close(Stream),fail.

mbz_release(Name,Uri) :-
        space_to_plus(Name,Name2),
        mbz_release2(Name2,Uri).
mbz_release2(Name,Uri) :-
        findall(uri(Uri,Score),find_release_id(Name,Uri,Score),Results),
        \+ambiguous(Results,_),
        Results=[uri(Uri,_)|_].
mbz_release2(Name,_) :-
        findall(uri(Uri,Score),find_release_id(Name,Uri,Score),Results),
        ambiguous(Results,Reason),
        reviews(Reviews),
        open(Reviews,append,Stream,[]),
        (
                	(Reason=uris(List,Score),
                        format(atom(T),'\n\n - Ambiguous release URIs for string "~w"\nMatching results are (with score ~w) :\n',[Name,Score]),
                        concat_atom(List,'\n',T2),
                        atom_concat(T,T2,T3),
                        write(Stream,T3)
                        );(
                        Reason=uri(A,B),
                        format(atom(U),'\n\n - Not succeeded to find a good enough release result for string "~w"\nBest matching results is ~w with score ~w%',[Name,A,B]),
                        write(Stream,U)
                        );(
                        Reason=[],
                        format(atom(U),'\n\n - No results for ~w',[Name]),
                        write(Stream,U)
                        )
        ),close(Stream),fail.

ambiguous([],[]). %no results
ambiguous([uri(Uri,Score)|_],uri(Uri,Score)) :- threshold(Thre),  Score < Thre, !. %the first result has a confidence lower than the threshold
ambiguous([uri(Uri1,Score),uri(Uri2,Score)|T1],uris([Uri1,Uri2|Uris],Score)) :- findall(Uri,member(uri(Uri,Score),T1),Uris), !. %the first two results have the same score



