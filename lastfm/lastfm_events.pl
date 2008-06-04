:- module(lastfm_events,[events_rdf/2]).

:- use_module(library('http/http_open')).
:- use_module(library('semweb/rdf_db')).

:- use_module(namespaces).
:- use_module(config).

:- dynamic cache/1.

events_rdf(User,Triples) :-
	events_xml(User,Xml),
	member(element(rss,_,Rss),Xml),!,
	member(element(channel,_,Channel),Rss),
	host(Host),
	format(atom(UserUri),'~w/~w',[Host,User]),
	findall(Rdf,(member(element(item,_,EventItem),Channel),event_rdf(EventItem,UserUri,Rdf)),T),
	flatten(T,Triples).
	

event_rdf(Event,UserUri,[
		rdf(EventUri,dc:title,literal(Title))
	,	rdf(EventUri,rdf:type,mo:'Performance')
	,	rdf(UserUri,lfm:recommendation,EventUri)
	,	rdf(EventUri,foaf:homepage,literal(Page))
	,	rdf(EventUri,dc:description,literal(Desc))
	,	rdf(EventUri,rdf:type,event:'Event')
	,	rdf(EventUri,event:time,TimeUri)
	,	rdf(EventUri,event:place,PlaceUri)
	,	rdf(PlaceUri,rdf:type,wgs:'Point')
	,	rdf(PlaceUri,dc:title,literal(Address))
	,	rdf(PlaceUri,foaf:homepage,LocationURI)
	,	rdf(PlaceUri,wgs:long,literal(Lat))
	,	rdf(PlaceUri,wgs:lat,literal(Long))
	,	rdf(PlaceUri,georss:point,literal(LatLong))
	,	rdf(TimeUri,rdf:type,tl:'Interval')
	,	rdf(TimeUri,tl:start,literal(type('http://www.w3.org/2001/XMLSchema#dateTime',Start)))
	,	rdf(TimeUri,tl:end,literal(type('http://www.w3.org/2001/XMLSchema#dateTime',End)))
	,	rdf(EventUri,lfm:publication_date,literal(type('http://www.w3.org/2001/XMLSchema#dateTime',PubDate)))
	]) :-
	member(element(title,_,[Title]),Event),
	member(element(link,_,[Page]),Event),
	member(element(description,_,[Desc]),Event),
	member(element(pubDate,_,[PubDate]),Event),
	member(element('xcal:dtstart',_,[Start]),Event),
	member(element('xcal:dtend',_,[End]),Event),
	member(element('xcal:location',_,[LocationURI]),Event),
	rdf_bnode(EventUri),rdf_bnode(TimeUri),rdf_bnode(PlaceUri),
	parse_desc(Desc,Place),
	Place\='',
	format(user_error,'Geocoding ~w\n',Place),
	google_geo(Place,Address,Lat,Long),
	format(user_error,'Found ~w,~w\n',[Long,Lat]),
	format(atom(LatLong),'~w ~w',[Lat,Long]).
	%host(Host),
	%atom_concat('http://www.last.fm/event/',EventId,Page),
	%concat_atom([Host,'/','event','/',EventId],Id).
	


events_xml(User,Xml) :-
	format(atom(URL),'http://ws.audioscrobbler.com/1.0/user/~w/eventsysrecs.rss',[User]),
	http_open(URL,Stream,[]),
	load_xml_file(Stream,Xml),
	close(Stream).

parse_desc(Desc,Location) :-
	concat_atom([_,T|_],'Location: ',Desc),
	concat_atom([Location|_],'\n',T),!.
parse_desc(_,'').

api_key('ABQIAAAAu0AMQcAkvqfViJpEeSH_-hT2yXp_ZAY8_ufC3CFXhHIE1NvwkxQ0_Z6CDgX2Q08wvAh1aYjckybfeA').
google_geo(Literal,Address,Lat,Long) :-
	cache(google_geo(Literal,Address,Lat,Long)),!.
google_geo(Literal,Address,Lat,Long) :-
	api_key(Key),www_form_encode(Literal,LE),
	format(atom(URL),'http://maps.google.com/maps/geo?q=~w&output=kml&key=~w',[LE,Key]),
	http_open(URL,Stream,[]),
	load_xml_file(Stream,Xml),
	member(element(kml,_,Kml),Xml),
	close(Stream),
	member(element('Response',_,Response),Kml),
	member(element('Placemark',_,Placemark),Response),
	member(element('address',_,[Address]),Placemark),
	member(element('Point',_,Point),Placemark),
	member(element('coordinates',_,[Coord]),Point),
	concat_atom([Long,Lat,_Alt],',',Coord),
	assert(cache(google_geo(Literal,Address,Lat,Long))).
	


