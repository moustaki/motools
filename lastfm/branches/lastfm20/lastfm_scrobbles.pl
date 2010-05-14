:- module(lastfm_scrobbles,
		[ tracks_rdf/2		% +User, -Triples
		]).

:- use_module(library('http/http_open')).
:- use_module(library('semweb/rdf_db')).

:- use_module(lastfm_namespaces).
:- use_module(lastfm_config).
:- use_module(lastfm_api_query).
:- use_module(lastfm_utils).

/** <module> Last.fm scrobbles to RDF converter

This module converts the scrobbles of a Last.fm user to RDF.

@author		Yves Raimond, 
			Thomas Gängler
@version 	2.0 
@copyright	Yves Raimond, Thomas Gängler; 2008 - 2010
*/
 
%%	lastfm_api_method(+LFM_API_METHOD)
%
% 	Defines the method for fetching scrobbles (artists, tracks, ...)
 
lastfm_api_method('user.getRecentTracks').
 
%%	lastfm_api_response_rootnode(+LFM_API_RESPONSE_ROOTNODE)
%
% 	Defines the root node of the Last.fm API response (not 'lfm').
 
lastfm_api_response_rootnode('recenttracks').	
 
%%	tracks_rdf(+User, -Triples)
%
% 	Converts the scrobbles of a given Last.fm user to RDF triples.
 
tracks_rdf(User,Triples) :-
	lastfm_api_method(LFMM),
	lastfm_api_response_rootnode(LFMRRN),
	lastfm_api_query_rdf('method=~w&user=~w',[LFMM,User],LFMRRN,Xml),
	findall(Triples,
		(member(element(track,_,Track),Xml),track_rdf(User,Track,Triples)),
		BT),
	flatten(BT,Triples),
	retractall(mbid(_,_)),
	retractall(scrobbledesc(_,_)).
	/*current_output(S),
	set_stream(S,encoding(utf8)),
	rdf_global_term(Triples,Triples4),
	rdf_write_xml(S,Triples4).*/
	%format(user_error,'Triples: ~w\n',Triples).
	
%%	track_rdf(+User, +Track, -Triples)
%
% 	Converts all track information of a scrobbling event to RDF triples.

track_rdf(User,Track,[
		rdf(EventUri,rdf:type,lfm:'ScrobbleEvent')
	,	rdf(EventUri,lfm:user,UserUri)
	,	rdf(EventUri,lfm:track_played,TrackUri)
	,	rdf(EventUri,rdfs:label,literal(ScrobbleDesc))|Triples]) :-
	track_mbid_info(Track,TrackUri,ScrobbleDesc,TrackMbidTriples),
	rdf_bnode(EventUri),
	date_info(Track,EventUri,DateTriples),
	append(DateTriples,TrackMbidTriples,Triples),
	create_local_uri(User, 'lfm-user', UserUri).
 
%%	track_mbid_info(+Track, +TrackUri, -ScrobbleDesc, -TrackTriples)
%
% 	Fetches the track title and MusicBrainz ID (mbid). Works when mbid is available.
% 	With duplicate check.
 
track_mbid_info(Track, TrackUri, ScrobbleDesc, TrackTriples) :-
    member(element(mbid,_,[ID]), Track), ID \= '', !,
    ((clause(mbid(ID,TrackUri), Z), Z = true)
    	->
    		(TrackTriples = [],
    		clause(scrobbledesc(ID,ScrobbleDesc), Y), Y = true)
    	;
    		(create_local_uri(ID, 'mbid', TrackUri),
    		track_info(Track, TrackUri, ScrobbleDesc, TrackInfoTriples),
    		set_mbid_uri(ID, TrackUri, ScrobbleDesc, 'track', TrackInfoTriples, TrackTriples))
	).
 
%%	track_mbid_info(+Track, +TrackUri, -ScrobbleDesc, -TrackTriples)
%
% 	Fetches the track title (without mbid).
% 	Without duplicate check.
 
track_mbid_info(Track, TrackUri, ScrobbleDesc, TrackInfoTriples) :-
	member(element(mbid,_,_), Track),
	rdf_bnode(TrackUri),
	track_info(Track, TrackUri, ScrobbleDesc, TrackInfoTriples).

%%	track_info(+Track, -TrackUri, -NewScrobbleDesc4, -Triples)
%
% 	Converts general track information to RDF triples.
   
track_info(Track, TrackUri, NewScrobbleDesc4, [	
		rdf(TrackUri, rdf:type, mo:'Track')
	, 	rdf(TrackUri, dc:title, literal(Title))
	,	rdf(TrackUri, foaf:isPrimaryTopicOf, URL) 
	,	rdf(URL, rdf:type, foaf:'Document') | Triples3]) :-
	artist_mbid_info(Track, TrackUri, ScrobbleDesc, ArtistTriples),
	write_scrobbledesc('Listened to', ScrobbleDesc, NewScrobbleDesc),
	member(element(name,_,[Title]), Track),
	format(atom(TitleDesc), ' track "~w"', Title),
	write_scrobbledesc(NewScrobbleDesc, TitleDesc, NewScrobbleDesc2),
	album_mbid_info(Track,TrackUri, NewScrobbleDesc3, AlbumTriples),
	append(AlbumTriples, ArtistTriples, Triples2),
	write_scrobbledesc(NewScrobbleDesc2, NewScrobbleDesc3, NewScrobbleDesc4),
	member(element(streamable,_,_), Track),
	member(element(url,[],[URL]), Track),
	lastfm_images(Track, TrackUri, ['small','medium','large','extralarge'], 'Track', ['mo','image'], TrackImagesTriples),
	append(TrackImagesTriples, Triples2, Triples3).

%%	artist_mbid_info(+Track, +TrackUri, -ScrobbleDesc, -ArtistTriples)
%
% 	Fetches the artist name and Musicbrainz ID (mbid). Works when mbid is available.
% 	With duplicate check.

artist_mbid_info(Track,TrackUri,ScrobbleDesc,ArtistTriples) :-
	member(element(artist,[mbid=ID],[Name]),Track),ID\='',!,
	((clause(mbid(ID,ArtistUri),Z),Z=true)
		->
    		(ArtistTriples = [rdf(TrackUri,foaf:maker,ArtistUri)],
    		clause(scrobbledesc(ID,ScrobbleDesc),Y),Y=true)
		;
			(create_local_uri(ID, 'mbid', ArtistUri),
			artist_info(Name,TrackUri,ArtistUri,ScrobbleDesc,ArtistInfoTriples),
			set_mbid_uri(ID, ArtistUri, ScrobbleDesc, 'artist', ArtistInfoTriples, ArtistTriples))
	).
 
%%	artist_mbid_info(+Track, +TrackUri, -ScrobbleDesc, -ArtistTriples)
%
% 	Fetches the artist name (without mbid).
% 	Without duplicate check.
 	
artist_mbid_info(Track, TrackUri, ScrobbleDesc, ArtistTriples) :-
	member(element(artist,_,[Name]), Track), !,
	rdf_bnode(ArtistUri),
	artist_info(Name, TrackUri, ArtistUri, ScrobbleDesc, ArtistTriples),
	ArtistUri=ArtistUri.
   
artist_mbid_info(Track,TrackUri,ScrobbleDesc,[]) :-
	Track=Track,
	TrackUri=TrackUri,
	ScrobbleDesc=''.

%%	artist_info(+Name, +TrackUri, -ArtistUri, -ScrobbleDesc, -Triples) 
%
%	Converts general artist information to RDF triples.
    
artist_info(Name, TrackUri, ArtistUri, ScrobbleDesc, [
		rdf(TrackUri, foaf:maker, ArtistUri)
	,   rdf(ArtistUri, rdf:type, mo:'MusicArtist')
	,	rdf(ArtistUri, foaf:homepage, Homepage)
	,	rdf(Homepage, rdf:type, foaf:'Document')
	,	rdf(ArtistUri, foaf:name, literal(Name))]) :-
	lastfm_host(LFMH),
	format(atom(Homepage), '~wmusic/~w', [LFMH, Name]),
	format(atom(ScrobbleDesc), ' "~w",', [Name]).
 
%%	album_mbid_info(+Track, +TrackUri, -ScrobbleDesc, -AlbumTriples) 
%
%	Fetches the album title and MusicBrainz ID (mbid). Works when mbid is available.
%	With duplicate check.
 
album_mbid_info(Track, TrackUri, ScrobbleDesc, AlbumTriples) :-
	member(element(album,[mbid=ID],[Title]), Track), ID \= '', !,
	((clause(mbid(ID,AlbumUri), Z), Z = true)
		->
			(AlbumTriples = [rdf(AlbumUri, mo:track, TrackUri)],
			clause(scrobbledesc(ID,ScrobbleDesc), Y), Y = true)
		;
			(create_local_uri(ID, 'mbid', AlbumUri),
			album_info(Title, TrackUri, AlbumUri, ScrobbleDesc, AlbumInfoTriples),
			set_mbid_uri(ID, AlbumUri, ScrobbleDesc, 'record', AlbumInfoTriples, AlbumTriples))
	).
 
%%	album_mbid_info(+Track, +TrackUri, -ScrobbleDesc, -AlbumTriples) 
%
%	Fetches the album title (without mbid).
%	Without duplicate check.
 
album_mbid_info(Track, TrackUri, ScrobbleDesc, AlbumTriples) :-
	member(element(album,_,[Title]), Track), !,
	rdf_bnode(AlbumUri),
	album_info(Title, TrackUri, AlbumUri, ScrobbleDesc, AlbumTriples),
	AlbumUri = AlbumUri.

album_mbid_info(Track,TrackUri,ScrobbleDesc,[]) :-
	member(element(album,_,[]),Track),
	TrackUri=TrackUri,
	ScrobbleDesc=''.

%%	album_info(+Title, +TrackUri, -ScrobbleDesc, -Triples)
%
%	Converts general album information to RDF triples.
	
album_info(Title,TrackUri,AlbumUri,ScrobbleDesc,[
		rdf(AlbumUri,mo:track,TrackUri)
	,	rdf(AlbumUri,rdf:type,mo:'Record')
	,	rdf(AlbumUri,rdfs:label,literal(Title))
	,	rdf(AlbumUri,foaf:name,literal(Title))]) :-
	format(atom(ScrobbleDesc),', record "~w"',Title).

%%	date_info(+Track, +EventUri, -Triples)
%
%	Converts the scrobbling date to RDF triples.
	
date_info(Track,EventUri,[rdf(EventUri,dc:date,literal(type(xmls:'dateTime', Date)))]) :-
	member(element(date,[uts=UTS],_),Track),!,
	uts_to_date(UTS,Date).
    
date_info(Track,EventUri,[]) :-
	Track=Track,
	EventUri=EventUri.

%%	write_scrobbledesc(+NewScrobbleDesc, +NewScrobbledesc2, -NewScrobbleDesc3)
%
%	Concats the scrobbling description of the scrobbling event.
	
write_scrobbledesc(NewScrobbleDesc,NewScrobbleDesc2,NewScrobbleDesc3) :-
	NewScrobbleDesc2\='',!,
	format(atom(NewScrobbleDesc3),'~w~w',[NewScrobbleDesc,NewScrobbleDesc2]).
	
write_scrobbledesc(NewScrobbleDesc,NewScrobbleDesc2,NewScrobbleDesc3) :-
	NewScrobbleDesc3=NewScrobbleDesc,
	NewScrobbleDesc2=NewScrobbleDesc2.

%%	set_mbid_uri(+MBID, +RdfNode, +ScrobbleDesc, +UriDesc, +Triples, -NewTriples)
%
% 	Converts the MBID of a track, artist or album to a dereferencable URI.
	
set_mbid_uri(MBID, RdfNode, ScrobbleDesc, UriDesc, Triples, [
		rdf(RdfNode, owl:sameAs, URI)
	,	rdf(RdfNode, mo:musicbrainz_guid, literal(MBID)) | Triples]) :-
	assertz(mbid(MBID, RdfNode)),
	assertz(scrobbledesc(MBID, ScrobbleDesc)),
	zitgist_host(ZGH),
	format(atom(URI), '~wmusic/~w/~w', [ZGH, UriDesc, MBID]).
