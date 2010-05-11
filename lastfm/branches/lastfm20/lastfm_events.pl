:- module(lastfm_events,
		[ events_rdf/2		% +User, -Triples
		]).

:- use_module(library('http/http_open')).
:- use_module(library('semweb/rdf_db')).

:- use_module(lastfm_namespaces).
:- use_module(lastfm_config).
:- use_module(lastfm_api_query).
:- use_module(lastfm_utils).

%:- dynamic cache/1.

/** <module> Last.fm events to RDF converter

This module converts the a Last.fm events graph of a Last.fm user to RDF.

@author		Yves Raimond, 
			Thomas Gängler
@version 	2.0
@copyright	Yves Raimond, Thomas Gängler; 2008 - 2010 
*/

%%	lastfm_api_method(+LFM_API_METHOD)
%  
%	Defines the method for fetching events.
%
% 	@tbd 	Currently it fetches the events, which the user will attend
%			a better solution is the recommended events method, which needs user authentification

%lastfm_api_method('user.getRecommendedEvents').
lastfm_api_method('user.getEvents').

%%	lastfm_api_response_rootnode(+LFM_API_RESPONSE_ROOTNODE)
%
%	Defines the root node of the Last.fm API response (not 'lfm').

lastfm_api_response_rootnode('events').

%%	events_rdf(+User, -Triples)
%
%	Converts a Last.fm events graph of a given user to RDF triples.

events_rdf(User,Triples) :-
	lastfm_api_method(LFMM),
	lastfm_api_response_rootnode(LFMRRN),
	%recommended_events_rdf(LFMM,LFMRRN,Xml),
	lastfm_api_query_rdf('method=~w&user=~w',[LFMM,User],LFMRRN,Xml),
	create_local_uri(User, 'lfm-user', UserUri),
	findall(Triples,
		(member(element(event,_,Event),Xml),event_rdf(UserUri,Event,Triples)),
		T),
	flatten(T,Triples).
	/*current_output(S),
	set_stream(S,encoding(utf8)),
	rdf_global_term(Triples,Triples4),
	rdf_write_xml(S,Triples4).*/
	%format(user_error,'Triples events: ~w\n', Triples).

%%	recommended_events_rdf(+LFMM, +LFMRRN, -Xml)
%
%	Fetches the Last.fm recommended events graph of a Last.fm user.
%
% 	@param 	LFMM	The Last.fm API method to fetch the recommended events
% 	@param 	LFMRRN	The Last.fm API response rootnode
%
% 	@tbd 	Currently not used, because of the interactive authentication process

recommended_events_rdf(LFMM,LFMRRN,Xml) :-
	%lastfm_api_sessionkey(SessionKey),
	lastfm_auth(SessionKey), 
	crypt_api_method_signature('method~wsk~w',[LFMM,SessionKey],ApiSignatureEncrypted),
	lastfm_api_query_rdf('method=~w&api_sig=~w&sk=~w',[LFMM,ApiSignatureEncrypted,SessionKey],LFMRRN,Xml).

%%	event_rdf(+UserUri, +Event, -Triples)
%
%	Converts a Last.fm events graph of a given user to RDF triples.

event_rdf(UserUri, Event, [
	%	rdf(UserUri, lfm:recommendation, EventUri)
	%	for "a user attends an event"
		rdf(UserUri, mo:listened, EventUri)
	,	rdf(EventUri, dc:title, literal(Title))
	,	rdf(EventUri, rdf:type, mo:'Performance')
	,   rdf(EventUri, lfm:event_id, literal(EventID))
	,	rdf(EventUri, foaf:isPrimaryTopicOf, LastFmEventUrl)
	,	Triples7]) :-
	member(element(id,_,[EventID]), Event),
	member(element(title,_,[Title]), Event),
	create_local_uri(EventID, 'lfm-event', EventUri),
	artists_info(Event, EventUri, ArtistTriples),
	venue_info(Event, EventUri, VenueTriples),
	append(VenueTriples, ArtistTriples, Triples2),
	date_info(Event, EventUri, DateTriples),
	append(DateTriples, Triples2, Triples3),
	description_info(Event, EventUri, DescriptionTriples),
	append(DescriptionTriples, Triples3, Triples4),
	lastfm_images(Event, EventUri, ['small','medium','large','extralarge'], 'Event', ['mo','image'], EventImagesTriples),
	append(EventImagesTriples, Triples4, Triples5),
	member(element(attendance,_,_), Event),
	member(element(reviews,_,_), Event),
	member(element(tag,_,_), Event),
	member(element(url,_,[LastFmEventUrl]), Event),
	website_info(Event, EventUri, WebsiteTriples),
	append(WebsiteTriples, Triples5, Triples6),
	member(element(tickets,_,_), Event),
	member(element(cancelled,_,_), Event),
	event_tags(Event, EventUri, EventTagsTriples),
	append(EventTagsTriples, Triples6, Triples7).

%%	artists_info(+Event, +EventUri, -Triples)
%
%	Converts all artists of a Last.fm event to RDF triples (incl. the headliner of the event).

artists_info(Event,EventUri,[
		rdf(EventUri,mo:headliner,HeadlinerUri)
	,	rdf(HeadlinerUri,rdf:type,mo:'MusicArtist')
	,	rdf(HeadlinerUri,foaf:name,literal(Headliner))
	,	ArtistTriples]) :-
	member(element(artists,_,Artists),Event),
	member(element(headliner,_,[Headliner]),Artists),!,
	rdf_bnode(HeadlinerUri),
	findall(Rdf,
		(member(element(artist,_,[Artist]),Artists),artist_info(Artist,Headliner,EventUri,Rdf)),
		BT),!,
	flatten(BT,ArtistTriples).

artists_info(Event,EventUri,[]) :-
	Event=Event,
	EventUri=EventUri.

%%	artist_info(+Artist, +Headliner, +EventUri, -Triples)
%
%	Converts an artist of a Last.fm event to RDF triples.

artist_info(Artist,Headliner,EventUri,[
		rdf(EventUri,mo:performer,ArtistUri)
	,	rdf(ArtistUri,rdf:type,mo:'MusicArtist')
	,	rdf(ArtistUri,foaf:name,literal(Artist))]) :-
	Artist\=Headliner,!,
	rdf_bnode(ArtistUri).

%%	venue_info(+Event, +EventUri, -Triples)
%
%	Converts the venue of a Last.fm event to RDF triples.
%	With duplicate check over Last.fm venue identifier.

venue_info(Event, EventUri, VenueTriples) :-	
	member(element(venue,_, Venue), Event),
	member(element(id,_,[VenueID]), Venue),
	((clause(vid(VenueID, OrganizationUri), Z), Z = true)
		->
			(VenueTriples = [rdf(EventUri, event:agent, OrganizationUri)])
		;
			(member(element(name,_,[VenueName]), Venue),
			create_local_uri(VenueID, 'lfm-venue', OrganizationUri),
			member(element(location,_,Location), Venue),
			location_info(Location, OrganizationUri, LocationTriples),
			geo_info(Location, OrganizationUri, GeoTriples),
			append(GeoTriples, LocationTriples, Triples2),
			member(element(url,_,[LastFmVenueUrl]), Venue),
			venue_website(Venue, OrganizationUri, VenueWebsiteTriples),
			append(VenueWebsiteTriples, Triples2, Triples3),
			venue_phonenumber(Venue, OrganizationUri, VenuePhonenumberTriples),
			append(VenuePhonenumberTriples, Triples3, Triples4),
			lastfm_images(Venue, OrganizationUri, ['small','medium','large','extralarge','mega'], 'Venue', ['foaf','depiction'], VenueImagesTriples),
			append(VenueImagesTriples, Triples4, Triples5),
			VenueTriples = [
		 			rdf(EventUri, event:agent, OrganizationUri)
				,	rdf(OrganizationUri, rdf:type, foaf:'Organisation')
				,	rdf(OrganizationUri, foaf:'name', literal(VenueName))
				,	rdf(OrganizationUri, lfm:venue_id, literal(VenueID))
				,	rdf(OrganizationUri, foaf:isPrimaryTopicOf, LastFmVenueUrl)
				,	Triples5],
			assertz(vid(VenueID, OrganizationUri)))
	).

%%	location_info(+Location, +PlaceUri, -Triples)
%
%	Converts the location of a venue to RDF triples.

location_info(Location, OrganizationUri, [ 
		rdf(AddressUri, v:locality, literal(City))
	,	rdf(AddressUri, v:'country-name', literal(Country))
	,	rdf(AddressUri, v:'street-address', literal(Street))
	,	rdf(AddressUri, v:'postal-code', literal(PostalCode)) | Triples]) :-	
	member(element(city,_,[City]), Location),
	member(element(country,_,[Country]), Location),
	member(element(street,_,[Street]), Location),
	member(element(postalcode,_,[PostalCode]), Location),!,
	location_main_info(OrganizationUri, AddressUri, Triples).

location_info(Location, OrganizationUri, [ 
		rdf(AddressUri, v:locality, literal(City))
	,	rdf(AddressUri, v:'country-name', literal(Country))
	,	rdf(AddressUri, v:'postal-code', literal(PostalCode)) | Triples]) :-	
	member(element(city,_,[City]), Location),
	member(element(country,_,[Country]), Location),
	member(element(street,_,_), Location),
	member(element(postalcode,_,[PostalCode]), Location),!,	
	location_main_info(OrganizationUri, AddressUri, Triples).

location_info(Location, OrganizationUri, [ 
		rdf(AddressUri, v:locality, literal(City))
	,	rdf(AddressUri, v:'country-name', literal(Country)) | Triples]) :-	
	member(element(city,_,[City]),Location),!,
	member(element(country,_,[Country]),Location),!,
	location_main_info(OrganizationUri, AddressUri, Triples). 
	
location_info(Location, OrganizationUri, []) :-
	Location = Location,
	OrganizationUri = OrganizationUri.

%%	location_main_info(+OrganizationUri, -AddressUri, -Triples)
%
%	Creates the address node and links it.
	
location_main_info(OrganizationUri, AddressUri, [
		rdf(OrganizationUri, ov:'businessCard', BusinessCardUri)
	,	rdf(BusinessCardUri, rdf:type, v:'VCard')
	,	rdf(BusinessCardUri, v:adr, AddressUri)
	,	rdf(AddressUri, rdf:type, v:'Address')]) :-
    rdf_bnode(BusinessCardUri),
    rdf_bnode(AddressUri).

%%	geo_info(+Location, +PlaceUri, -Triples)
%
%	Converts the spatial information of a location to RDF triples.

geo_info(Location, OrganizationUri, [
	    rdf(OrganizationUri, wgs:'location', PlaceUri)
	,	rdf(PlaceUri, rdf:type, wgs:'SpatialThing')
	,	rdf(PlaceUri, wgs:long, literal(type(xmls:'float', Lat)))
	,	rdf(PlaceUri, wgs:lat, literal(type(xmls:'float', Long)))]) :-	
	member(element('geo:point' ,_, GeoPoint), Location),!,
	member(element('geo:lat' ,_, [Lat]), GeoPoint),
	member(element('geo:long' ,_, [Long]), GeoPoint),
	rdf_bnode(PlaceUri).

geo_info(Location,OrganizationUri,[]) :-
	Location = Location,
	OrganizationUri = OrganizationUri.

%%	venue_website(+Venue, +PlaceUri, -Triples)
%
%	Converts the venue website to RDF triples.

venue_website(Venue,PlaceUri,[rdf(PlaceUri,foaf:homepage,VenueWebsite)]) :-	
	member(element(website,_,[VenueWebsite]),Venue),!.

venue_website(Venue,PlaceUri,[]) :-	
	member(element(website,_,_),Venue),
	PlaceUri=PlaceUri.

%%	venue_phonenumber(+Venue, +PlaceUri, -Triples)
%
%	Converts the venue phonenumber to RDF triples.

venue_phonenumber(Venue,PlaceUri,[rdf(PlaceUri,foaf:phone,literal(PhoneNumber))]) :-	
	member(element(phonenumber,_,[PhoneNumber]),Venue),!.

venue_phonenumber(Venue,PlaceUri,[]) :-
	member(element(phonenumber,_,_),Venue),
	PlaceUri=PlaceUri.

%%	date_info(+Event, +EventUri, -Triples)
%
%	Converts the date information of an event to RDF triples
%
%	@tbd	format dates to xmls:dateTime

date_info(Event,EventUri,[ 
		rdf(EventUri,event:time,TimeUri)
	,	rdf(TimeUri,rdf:type,tl:'Interval')
	,	rdf(TimeUri,tl:start,literal(Start))
	,	rdf(TimeUri,tl:end,literal(End))]) :-	
	member(element(startDate,_,[Start]),Event),
	member(element(endDate,_,[End]),Event),!,
	rdf_bnode(TimeUri).
	
date_info(Event,EventUri,[ 
		rdf(EventUri,event:time,TimeUri)
	,	rdf(TimeUri,rdf:type,tl:'Instant')
	,	rdf(TimeUri,tl:start,literal(Start))]) :-	
	member(element(startDate,_,[Start]),Event),
	rdf_bnode(TimeUri).

%%	description_info(+Event, +EvenUri, -Triples)
%
%	Converts the description of an event to RDF triples.

description_info(Event,EventUri,[rdf(EventUri,dc:description,literal(Desc))]) :-	
	member(element(description,_,[Desc]),Event),!.

description_info(Event,EventUri,[]) :-	
	member(element(description,_,_),Event),
	EventUri=EventUri.

%%	website_info(+Event, +EventUri, -Triples)
%
%	Converts the website of an event to RDF triples.

website_info(Event,EventUri,[rdf(EventUri,foaf:homepage,Page)]) :-	
	member(element(website,_,[Page]),Event),!.

website_info(Event,EventUri,[]) :-	
	member(element(website,_,_),Event),
	EventUri=EventUri.

%%	event_tags(+Event, +EventUri, -Triples)
%
%	Converts the tags of an event to RDF triples.

event_tags(Event,EventUri,Triples) :-	
	member(element(tags,_,Tags),Event),
	findall(Rdf,
		(member(element(tag,_,[Tag]),Tags),tag_info(Tag,EventUri,Rdf)),
		BT),!,
	flatten(BT,Triples).
	
event_tags(Event,EventUri,[]) :-
	Event=Event,
	EventUri=EventUri.

%%	tag_info(+Tag, +EventUri, -Triples)
%
%	Converts a tag of an to RDF triples.

tag_info(Tag,EventUri,[
		rdf(EventUri,tags:taggedWithTag,TagUri)
	,	rdf(TagUri,rdf:type,tags:'Tag')
	,	rdf(TagUri,tags:tagName,literal(Tag))]) :-
	rdf_bnode(TagUri).

