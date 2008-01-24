:- module(jamendo,[
		artist/1
	,	artist_name/2
	,	artist_dispname/2
	,	artist_description/2
	,	artist_genre/2
	,	artist_country/2
	,	artist_geo/2
	,	artist_image/2
	,	artist_link/2
	,	artist_homepage/2
	,	album/1
	,	album_name/2
	,	album_description/2
	,	album_artist/2
	,	album_genre/2
	,	album_validationurl/2
	,	album_publicdate/2
	,	album_archiveset/2
	,	album_popularity/2
	,	album_releasedate/2
	,	album_link/2
	,	album_cover/4
	,	album_p2p/4
	,	album_tags/2
	,	album_tag/2
	,	track/1
	,	track_name/2
	,	track_album/2
	,	track_no/2
	,	track_lyrics/2
	,	track_lengths/2
	,	track_licenseurl/2
	,	track_link/2
	]).

/**
 * A SWI-Prolog module to access Jamendo XML dumps
 * Yves Raimond, C4DM, Queen Mary, University of London, 2007
 */



%:-import_from(jamendo_xml,parsed_dump/1).

/**
 * Jamendo artists
 */
artist(Id) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Artists',_,Artists),NestedElements),
        member(Artist,Artists),
        Artist=element(artist,ArtistAtt,_),
        get_attributes([id],ArtistAtt,[Id]).
artist_name(Id,Name) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Artists',_,Artists),NestedElements),
        member(Artist,Artists),
        Artist=element(artist,ArtistAtt,_),
        get_attributes([name,id],ArtistAtt,[Name,Id]),
	Name\=''.
artist_dispname(Id,DispName) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Artists',_,Artists),NestedElements),
        member(Artist,Artists),
        Artist=element(artist,ArtistAtt,ArtistNested),
	get_nested_elts([dispname],ArtistNested,[DispName]),
	get_attributes([id],ArtistAtt,[Id]),
	DispName\=''.
artist_genre(Id,Genre) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Artists',_,Artists),NestedElements),
        member(Artist,Artists),
        Artist=element(artist,ArtistAtt,ArtistNested),
        get_nested_elts([genre],ArtistNested,[Genre]),
        get_attributes([id],ArtistAtt,[Id]),
	Genre\=''.
artist_description(Id,Description) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Artists',_,Artists),NestedElements),
        member(Artist,Artists),
        Artist=element(artist,ArtistAtt,ArtistNested),
        get_nested_elts([description],ArtistNested,[Description]),
        get_attributes([id],ArtistAtt,[Id]),
	Description\=''.
artist_country(Id,Country) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Artists',_,Artists),NestedElements),
        member(Artist,Artists),
        Artist=element(artist,ArtistAtt,_),
        get_attributes([country,id],ArtistAtt,[Country,Id]),
	Country\=''.
artist_image(Id,Image) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Artists',_,Artists),NestedElements),
        member(Artist,Artists),
        Artist=element(artist,ArtistAtt,_),
        get_attributes([image,id],ArtistAtt,[Image,Id]),
	Image\=''.
artist_geo(Id,GeoString) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Artists',_,Artists),NestedElements),
        member(Artist,Artists),
        Artist=element(artist,ArtistAtt,_),
        get_attributes([geostr1,id],ArtistAtt,[GeoString,Id]),
	GeoString\=''.
artist_link(Id,Link) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Artists',_,Artists),NestedElements),
        member(Artist,Artists),
        Artist=element(artist,ArtistAtt,_),
        get_attributes([link,id],ArtistAtt,[Link,Id]),
	Link\=''.
artist_homepage(Id,HomePage) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Artists',_,Artists),NestedElements),
        member(Artist,Artists),
        Artist=element(artist,ArtistAtt,_),
        get_attributes([homepage,id],ArtistAtt,[HomePage,Id]),
	HomePage\=''.


/**
 * Jamendo albums
 */
album(Id) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Albums',_,Albums),NestedElements),
        member(Album,Albums),
        Album=element(album,AlbumAtt,_),
	get_attributes([id],AlbumAtt,[Id]).
album_artist(Id,ArtistId) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Albums',_,Albums),NestedElements),
        member(Album,Albums),
        Album=element(album,AlbumAtt,_),
        get_attributes([artistID,id],AlbumAtt,[ArtistId,Id]),
	ArtistId\=''.
album_name(Id,DispName) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Albums',_,Albums),NestedElements),
        member(Album,Albums),
        Album=element(album,AlbumAtt,AlbumNested),
	get_nested_elts([dispname],AlbumNested,[DispName]),
	get_attributes([id],AlbumAtt,[Id]),
	DispName\=''.
album_genre(Id,Genre) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Albums',_,Albums),NestedElements),
        member(Album,Albums),
        Album=element(album,AlbumAtt,AlbumNested),
        get_nested_elts([genre],AlbumNested,[Genre]),
        get_attributes([id],AlbumAtt,[Id]),
	Genre\=''.
album_description(Id,Description) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Albums',_,Albums),NestedElements),
        member(Album,Albums),
        Album=element(album,AlbumAtt,AlbumNested),
        get_nested_elts([description],AlbumNested,[Description]),
        get_attributes([id],AlbumAtt,[Id]),
	Description\=''.
album_validationurl(Id,ValidationURL) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Albums',_,Albums),NestedElements),
        member(Album,Albums),
        Album=element(album,AlbumAtt,_),
        get_attributes([validationURL,id],AlbumAtt,[ValidationURL,Id]),
	ValidationURL\=''.
album_publicdate(Id,PublicDate) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Albums',_,Albums),NestedElements),
        member(Album,Albums),
        Album=element(album,AlbumAtt,_),
        get_attributes([publicDate,id],AlbumAtt,[PublicDate,Id]),
	PublicDate\=''.
album_archiveset(Id,ArchiveSet) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Albums',_,Albums),NestedElements),
        member(Album,Albums),
        Album=element(album,AlbumAtt,_),
        get_attributes([archiveSet,id],AlbumAtt,[ArchiveSet,Id]),
	ArchiveSet\=''.
album_popularity(Id,Popularity) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Albums',_,Albums),NestedElements),
        member(Album,Albums),
        Album=element(album,AlbumAtt,_),
        get_attributes([popularity,id],AlbumAtt,[Popularity,Id]),
	Popularity\=''.
album_releasedate(Id,ReleaseDate) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Albums',_,Albums),NestedElements),
        member(Album,Albums),
        Album=element(album,AlbumAtt,_),
        get_attributes([releaseDate,id],AlbumAtt,[ReleaseDate,Id]),
	ReleaseDate\=''.
album_link(Id,Link) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Albums',_,Albums),NestedElements),
        member(Album,Albums),
        Album=element(album,AlbumAtt,_),
        get_attributes([link,id],AlbumAtt,[Link,Id]),
	Link\=''.
album_cover(Id,Res,No,Cover) :-
	parsed_dump([element(_,_,NestedElements)]),
	member(element('Albums',_,Albums),NestedElements),
	member(Album,Albums),
	Album=element(album,Att,AlbumAtt),
	member(id=Id,Att),
	member(element('Covers',_,Covers),AlbumAtt),
	member(element(cover,[res=Res,no=No],[Cover]),Covers).
album_p2p(Id,AudioEncoding,Network,Link) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Albums',_,Albums),NestedElements),
        member(Album,Albums),
        Album=element(album,Att,AlbumAtt),
        member(id=Id,Att),
	member(element('P2PLinks',_,P2PLinks),AlbumAtt),
	member(element(p2plink,LinkAtt,[Link]),P2PLinks),
	member(audioEncoding=AudioEncoding,LinkAtt),
	member(network=Network,LinkAtt).
album_tag(Id,Tag) :-
	album_tags(Id,Tags),
	concat_atom(TagList,' ',Tags),
	member(Tag,TagList).
album_tags(Id,Tags) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Albums',_,Albums),NestedElements),
        member(Album,Albums),
        Album=element(album,Att,AlbumNested),
        get_nested_elts([tags],AlbumNested,[Tags]),
	member(id=Id,Att),
	Tags\=''.

/**
 * Jamendo tracks
 */
track(Id) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Tracks',_,Tracks),NestedElements),
        member(Track,Tracks),
        Track=element(track,TrackAtt,_),
	get_attributes([id],TrackAtt,[Id]).
track_album(Id,AlbumId) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Tracks',_,Tracks),NestedElements),
        member(Track,Tracks),
        Track=element(track,TrackAtt,_),
        get_attributes([albumID,id],TrackAtt,[AlbumId,Id]),
	AlbumId\=''.
track_no(Id,TrackNo) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Tracks',_,Tracks),NestedElements),
        member(Track,Tracks),
        Track=element(track,TrackAtt,_),
        get_attributes([trackno,id],TrackAtt,[TrackNo,Id]),
	TrackNo\=''.
track_name(Id,Name) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Tracks',_,Tracks),NestedElements),
        member(Track,Tracks),
        Track=element(track,TrackAtt,TrackNested),
	get_attributes([id],TrackAtt,[Id]),
	get_nested_elts([dispname],TrackNested,[Name]),
	Name\=''.
track_lyrics(Id,Lyrics) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Tracks',_,Tracks),NestedElements),
        member(Track,Tracks),
        Track=element(track,TrackAtt,TrackNested),
        get_attributes([id],TrackAtt,[Id]),
        get_nested_elts([lyrics],TrackNested,[Lyrics]),
	Lyrics\=''.
track_lengths(Id,Lengths) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Tracks',_,Tracks),NestedElements),
        member(Track,Tracks),
        Track=element(track,TrackAtt,_),
        get_attributes([lengths,id],TrackAtt,[Lengths,Id]),
	Lengths\=''.
track_licenseurl(Id,LicenseURL) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Tracks',_,Tracks),NestedElements),
        member(Track,Tracks),
        Track=element(track,TrackAtt,_),
        get_attributes([licenseURL,id],TrackAtt,[LicenseURL,Id]),
	LicenseURL\=''.
track_link(Id,Link) :-
	parsed_dump([element(_,_,NestedElements)]),
        member(element('Tracks',_,Tracks),NestedElements),
        member(Track,Tracks),
        Track=element(track,TrackAtt,_),
        get_attributes([link,id],TrackAtt,[Link,Id]),
	Link\=''.

/**
 * XML parsing tools
 */
get_attributes([],_,[]).
get_attributes([AttName|T1],AttList,[Att|T2]) :-
	member(AttName=Att,AttList),
	get_attributes(T1,AttList,T2).

get_nested_elts([],_,[]).
get_nested_elts([EltName|T1],NestedElements,[EltText|T2]):-
	(member(element(EltName,_,[EltText]),NestedElements);EltText=''),
	get_nested_elts(T1,NestedElements,T2).
