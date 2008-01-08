:- module(lastfm,[]).

:- use_module(library('http/http_open')).
:- use_module(library('semweb/rdf_db')).


/**
 * Goals converting a Prolog representation
 * of XML last.fm feeds to Music Ontology RDF
 *
 * Caching within the local store, for now.
 */
tracks_rdf(User,Triples) :-
	recent_tracks_xml(User,Xml),
	Xml = [element(recenttracks,_,Xml2)],
	findall(Triples,
		(member(element(track,_,Track),Xml2),phrase(lastfm:artist_info(User,_,Triples),Track)),
		BT),
	flatten(BT,Triples).


artist_info(User,Track,[rdf(Track,foaf:maker,Artist),rdf(Artist,rdf:type,mo:'MusicalArtist'),rdf(Artist,foaf:name,literal(Name)),rdf(Artist,owl:sameAs,URI)|Triples]) -->
	newline,
	[element(artist,[mbid=ID],[Name])],
	{
	rdf_bnode(Artist),
	format(atom(URI),'http://zitgist.com/music/artist/~w',[ID])
	},
	track_info(User,Track,Triples).
track_info(User,Track,[rdf(Track,dc:title,literal(Title)),rdf(Track,rdf:type,mo:'Track'),rdf(Track,owl:sameAs,URI)|Triples]) -->
	newline,
	[element(name,_,[Title])],newline,
	[element(mbid,_,[ID])],!,
	{
	rdf_bnode(Track),
	format(atom(URI),'http://zitgist.com/music/track/~w',[ID])
	},
	album_info(User,Track,Triples).
track_info(User,Track,[rdf(Track,dc:title,literal(Title)),rdf(Track,rdf:type,mo:'Track')|Triples]) -->
	newline,
	[element(name,_,[Title])],newline,
	[element(mbid,_,_)],
	{
	rdf_bnode(Track)
	},
	album_info(User,Track,Triples).
album_info(User,Track,[rdf(Album,mo:track,Track),rdf(Album,rdf:type,mo:'Record'),rdf(Album,owl:sameAs,URI),rdf(Album,foaf:name,literal(Title))|Triples]) -->
	newline,
	[element(album,[mbid=ID],[Title])],!,
	{
	rdf_bnode(Album),
	format(atom(URI),'http://zitgist.com/music/record/~w',[ID])
	},
	url_info(User,Track,Triples).
album_info(User,Track,[rdf(Album,mo:track,Track),rdf(Album,rdf:type,mo:'Record'),rdf(Album,foaf:name,literal(Title))|Triples]) -->
        newline,
	[element(album,_,[Title])],
        {
        rdf_bnode(Album)
        },
        url_info(User,Track,Triples).
url_info(User,Track,[rdf(Track,foaf:primaryTopicOf,URL)|Triples]) -->
	newline,
	[element(url,[],[URL])],
	date_info(User,Track,Triples).
date_info(User,Track,[rdf(Evt,rdf:type,lfm:'BroadcastEvent'),rdf(Evt,lfm:track_played,Track),rdf(Evt,dc:date,literal(Date)),rdf(Evt,lfm:listener,Uri)]) -->
	newline,
	[element(date,[uts=UTS],_)],
	{
	atom_to_term(UTS,Time,[]),
	stamp_date_time(Time,date(Year,Month,Day,Hour,Minute,Seconds,_,_,_),'UTC'),
	term_to_atom(Year,Y),term_to_atom(Month,Mo),term_to_atom(Day,D),term_to_atom(Hour,H),term_to_atom(Minute,Mi),term_to_atom(Seconds,S),
	format(atom(Date),'~w-~w-~wT~w:~w:~w',[Y,Mo,D,H,Mi,S]),
	format(atom(Uri),'http://ws.audioscrobbler.com/1.0/user/~w',[User])
	},done.
done --> [_|_].
done --> [].
newline --> [T],{atom_concat('\n',_,T)},!.
newline --> [].


/**
 * Access to a Prolog representation of the XML last.fm feeds
 */
recent_tracks_xml(User,Xml) :-
	format(atom(Url),'http://ws.audioscrobbler.com/1.0/user/~w/recenttracks.xml',[User]),
	http_open(Url,Stream,[]),
	load_xml_file(Stream,Xml).



