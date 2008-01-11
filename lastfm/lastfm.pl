:- module(lastfm,[scrobble_rdf/2,host/1]).

:- use_module(library('http/http_open')).
:- use_module(library('semweb/rdf_db')).

:- consult(namespaces).
:- consult(config).


scrobble_rdf(User,RDF2) :-
	tracks_rdf(User,RDF),
	rdf_global_term(RDF,RDF2).


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
	[element(artist,[mbid=ID],[Name])],!,
	{
	rdf_bnode(Artist),
	format(atom(URI),'http://zitgist.com/music/artist/~w',[ID]),
	format(atom(ScrobbleDesc),'Listened to "~w"',[Name])
	},
	track_info(User,Track,ScrobbleDesc,Triples).
artist_info(User,Track,[rdf(Track,foaf:maker,Artist),rdf(Artist,rdf:type,mo:'MusicalArtist'),rdf(Artist,foaf:name,literal(Name))|Triples]) -->
        newline,
        [element(artist,_,[Name])],
        {
        rdf_bnode(Artist),
        format(atom(ScrobbleDesc),'Listened to "~w"',[Name])
        },
        track_info(User,Track,ScrobbleDesc,Triples).
track_info(User,Track,ScrobbleDesc,[rdf(Track,dc:title,literal(Title)),rdf(Track,rdf:type,mo:'Track'),rdf(Track,owl:sameAs,URI)|Triples]) -->
	newline,
	[element(name,_,[Title])],newline,
	[element(mbid,_,[ID])],!,
	{
	rdf_bnode(Track),
	format(atom(URI),'http://zitgist.com/music/track/~w',[ID]),
	format(atom(NewScrobbleDesc),'~w, track "~w"',[ScrobbleDesc,Title])
	},
	album_info(User,Track,NewScrobbleDesc,Triples).
track_info(User,Track,ScrobbleDesc,[rdf(Track,dc:title,literal(Title)),rdf(Track,rdfs:label,literal(Title)),rdf(Track,rdf:type,mo:'Track')|Triples]) -->
	newline,
	[element(name,_,[Title])],newline,
	[element(mbid,_,_)],
	{
	rdf_bnode(Track),
	format(atom(NewScrobbleDesc),'~w, track "~w"',[ScrobbleDesc,Title])
	},
	album_info(User,Track,NewScrobbleDesc,Triples).
album_info(User,Track,ScrobbleDesc,[rdf(Album,mo:track,Track),rdf(Album,rdf:type,mo:'Record'),rdf(Album,owl:sameAs,URI),rdf(Album,rdfs:label,literal(Title)),rdf(Album,foaf:name,literal(Title))|Triples]) -->
	newline,
	[element(album,[mbid=ID],[Title])],{ID\=''},!,
	{
	rdf_bnode(Album),
	format(atom(URI),'http://zitgist.com/music/record/~w',[ID]),
	format(atom(NewScrobbleDesc),'~w, record "~w"',[ScrobbleDesc,Title])
	},
	url_info(User,Track,NewScrobbleDesc,Triples).
album_info(User,Track,ScrobbleDesc,[rdf(Album,mo:track,Track),rdf(Album,rdf:type,mo:'Record'),rdf(Album,rdfs:label,literal(Title)),rdf(Album,foaf:name,literal(Title))|Triples]) -->
        newline,
	[element(album,_,[Title])],
        {
        rdf_bnode(Album),
	format(atom(NewScrobbleDesc),'~w, record "~w"',[ScrobbleDesc,Title])
        },
        url_info(User,Track,NewScrobbleDesc,Triples).
url_info(User,Track,ScrobbleDesc,[rdf(Track,foaf:primaryTopicOf,URL)|Triples]) -->
	newline,
	[element(url,[],[URL])],
	date_info(User,Track,ScrobbleDesc,Triples).
date_info(User,Track,ScrobbleDesc,[rdf(Evt,rdf:type,lfm:'ScrobbleEvent'),rdf(Evt,rdfs:label,literal(ScrobbleDesc)),rdf(Evt,lfm:track_played,Track),rdf(Evt,dc:date,literal(type('http://www.w3.org/2001/XMLSchema#dateTime',Date))),rdf(Evt,lfm:user,Uri)]) -->
	newline,
	[element(date,[uts=UTS],_)],
	{
	rdf_bnode(Evt),
	atom_to_term(UTS,Time,[]),
	stamp_date_time(Time,date(Year,Month,Day,Hour,Minute,Seconds,_,_,_),'UTC'),
	term_to_atom(Year,Y),term_to_atom(Month,Mo),term_to_atom(Day,D),term_to_atom(Hour,H),term_to_atom(Minute,Mi),term_to_atom(Seconds,S),
	((atom_chars(Mo,MoC),length(MoC,1))->atom_chars(Mo2,['0'|MoC]);Mo2=Mo),
	((atom_chars(D,DC),length(DC,1))->atom_chars(D2,['0'|DC]);D2=D),
	((atom_chars(H,HC),length(HC,1))->atom_chars(H2,['0'|HC]);H2=H),
	((atom_chars(Mi,MiC),length(MiC,1))->atom_chars(Mi2,['0'|MiC]);Mi2=Mi),
	((atom_chars(S,SC),length(SC,1))->atom_chars(S2,['0'|SC]);S2=S),
	format(atom(Date),'~w-~w-~wT~w:~w:~w',[Y,Mo2,D2,H2,Mi2,S2]),
	host(Host),
	format(atom(Uri),'~w/~w',[Host,User])
	%format(atom(Uri),'http://ws.audioscrobbler.com/1.0/user/~w',[User])
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



