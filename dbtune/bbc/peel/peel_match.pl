:- module(peel_match,[]).

:- consult(library('semweb/rdf_db')).

:- use_module('p2r/match').

:- consult(peel_ns).
:- use_module(peel).

match:
	(peel:artist(Id,Name,_,Picture))
		eq
	[
		rdf(pattern(['http://dbtune.org/bbc/peel/artist/',Id]),rdf:type,mo:'MusicArtist')
	,	rdf(pattern(['http://dbtune.org/bbc/peel/artist/',Id]),foaf:name,literal(type('http://www.w3.org/2001/XMLSchema#string',Name)))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/artist/',Id]),foaf:img,pattern(['http://bbc.co.uk/music/',Picture])) %ooops i don't think it is there:-) 
	,	rdf(pattern(['http://dbtune.org/bbc/peel/artist/',Id]),rdfs:label,literal(type('http://www.w3.org/2001/XMLSchema#string',Name)))
	].

match:
	(peel:artist(Id,_,Biography,_),Biography\='',Biography\='\\N\r')
		eq
	[
		rdf(pattern(['http://dbtune.org/bbc/peel/artist/',Id]),mo:biography,literal(type('http://www.w3.org/2001/XMLSchema#string',Biography)))
	].

match:
	(peel:session(SessionId,_,_,_,ProducerT,_,_,_),ProducerT\='',peel_match:encode(ProducerT,Producer))
		eq
	[
		rdf(pattern(['http://dbtune.org/bbc/peel/producer/',Producer]),rdf:type,foaf:'Person')
	,	rdf(pattern(['http://dbtune.org/bbc/peel/producer/',Producer]),foaf:name,literal(type('http://www.w3.org/2001/XMLSchema#string',ProducerT)))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/producer/',Producer]),rdfs:label,literal(type('http://www.w3.org/2001/XMLSchema#string',ProducerT)))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/recording/',SessionId]),mo:producer,pattern(['http://dbtune.org/bbc/peel/producer/',Producer]))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/producer/',Producer]),mo:produced,pattern(['http://dbtune.org/bbc/peel/recording/',SessionId]))
	].
match:
        (peel:session(SessionId,_,_,_,_,EngineerT,_,_),EngineerT\='',peel_match:encode(EngineerT,Engineer))
                eq
        [
                rdf(pattern(['http://dbtune.org/bbc/peel/engineer/',Engineer]),rdf:type,foaf:'Person')
        ,       rdf(pattern(['http://dbtune.org/bbc/peel/engineer/',Engineer]),foaf:name,literal(type('http://www.w3.org/2001/XMLSchema#string',EngineerT)))
        ,       rdf(pattern(['http://dbtune.org/bbc/peel/engineer/',Engineer]),rdfs:label,literal(type('http://www.w3.org/2001/XMLSchema#string',EngineerT)))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/recording/',SessionId]),mo:engineer,pattern(['http://dbtune.org/bbc/peel/engineer/',Engineer]))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/engineer/',Engineer]),mo:engineered,pattern(['http://dbtune.org/bbc/peel/recording/',SessionId]))
        ].
match:
        (peel:session(SessionId,_,_,_,_,_,EngineerT,_),EngineerT\='',peel_match:encode(EngineerT,Engineer))
                eq
        [
                rdf(pattern(['http://dbtune.org/bbc/peel/engineer/',Engineer]),rdf:type,foaf:'Person')
        ,       rdf(pattern(['http://dbtune.org/bbc/peel/engineer/',Engineer]),foaf:name,literal(type('http://www.w3.org/2001/XMLSchema#string',EngineerT)))
        ,       rdf(pattern(['http://dbtune.org/bbc/peel/engineer/',Engineer]),rdfs:label,literal(type('http://www.w3.org/2001/XMLSchema#string',EngineerT)))
	,       rdf(pattern(['http://dbtune.org/bbc/peel/recording/',SessionId]),mo:engineer,pattern(['http://dbtune.org/bbc/peel/engineer/',Engineer]))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/engineer/',Engineer]),mo:engineered,pattern(['http://dbtune.org/bbc/peel/recording/',SessionId]))
        ].


match:
	(peel:session(SessionId,ArtistID,_,_,_,_,_,Studio))
		eq
	[
		rdf(pattern(['http://dbtune.org/bbc/peel/session/',SessionId]),rdf:type,mo:'Performance')
	,	rdf(pattern(['http://dbtune.org/bbc/peel/session/',SessionId]),rdfs:label,literal(type('http://www.w3.org/2001/XMLSchema#string',pattern(['Performance ',SessionId,' in ',Studio]))))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/session/',SessionId]),mo:performer,pattern(['http://dbtune.org/bbc/peel/artist/',ArtistID]))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/artist/',ArtistID]),mo:performed,pattern(['http://dbtune.org/bbc/peel/session/',SessionId]))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/session/',SessionId]),event:place,literal(Studio)) %to link
	,	rdf(pattern(['http://dbtune.org/bbc/peel/session/',SessionId]),mo:producesSound,pattern(['http://dbtune.org/bbc/peel/sound/',SessionId]))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/sound/',SessionId]),rdf:type,mo:'Sound')
	,	rdf(pattern(['http://dbtune.org/bbc/peel/recording/',SessionId]),rdf:type,mo:'Recording')
	,	rdf(pattern(['http://dbtune.org/bbc/peel/recording/',SessionId]),rdfs:label,literal(type('http://www.w3.org/2001/XMLSchema#string',pattern(['Recording ',SessionId,' in ',Studio]))))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/recording/',SessionId]),mo:usesSound,pattern(['http://dbtune.org/bbc/peel/sound/',SessionId]))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/recording/',SessionId]),event:place,literal(Studio)) %to link
	,	rdf(pattern(['http://dbtune.org/bbc/peel/signal/',SessionId]),rdf:type,mo:'Signal')
	,	rdf(pattern(['http://dbtune.org/bbc/peel/signal/',SessionId]),rdfs:label,literal(type('http://www.w3.org/2001/XMLSchema#string',pattern(['Signal ',SessionId]))))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/recording/',SessionId]),mo:producesSignal,pattern(['http://dbtune.org/bbc/peel/signal/',SessionId]))
	].


match:
	(peel:session(SessionId,_,TransmissionDate,_,_,_,_,_))
		eq
	[
		rdf(pattern(['http://dbtune.org/bbc/peel/transmission/',SessionId]),event:time,literal(type('http://www.w3.org/2001/XMLSchema#date',TransmissionDate)))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/transmission/',SessionId]),rdf:type,mo:'Transmission')
	,	rdf(pattern(['http://dbtune.org/bbc/peel/transmission/',SessionId]),rdfs:label,literal(type('http://www.w3.org/2001/XMLSchema#string',pattern(['Transmission of session ',SessionId,' on the ',TransmissionDate]))))
	].


match:
	(peel:session_band_member(_,SessionId,PerformerT,Instrument),peel_match:encode(PerformerT,Performer)) 
		eq
	[
		rdf(pattern(['http://dbtune.org/bbc/peel/session/',SessionId]),event:hasSubEvent,pattern(['http://dbtune.org/bbc/peel/perf_ins/',Performer]))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/perf_ins/',Performer]),mo:performer,pattern(['http://dbtune.org/bbc/peel/artist/',Performer]))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/artist/',Performer]),mo:performed,pattern(['http://dbtune.org/bbc/peel/perf_ins/',Performer]))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/perf_ins/',Performer]),rdf:type,mo:'Performance')
	,	rdf(pattern(['http://dbtune.org/bbc/peel/artist/',Performer]),foaf:name,literal(type('http://www.w3.org/2001/XMLSchema#string',PerformerT)))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/artist/',Performer]),rdf:type,foaf:'Person')
	,	rdf(pattern(['http://dbtune.org/bbc/peel/perf_ins/',Performer]),mo:instrument,literal(Instrument)) % to link
	].


match: 
	(peel:session_track(TrackID,SessionID,TrackTitle,_))
		eq
	[
		rdf(pattern(['http://dbtune.org/bbc/peel/session/',SessionID]),event:hasSubEvent,pattern(['http://dbtune.org/bbc/peel/perf_work/',TrackID]))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/perf_work/',TrackID]),event:usesWork,pattern(['http://dbtune.org/bbc/peel/work/',TrackID]))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/perf_work/',TrackID]),rdf:type,mo:'Performance')
	,	rdf(pattern(['http://dbtune.org/bbc/peel/work/',TrackID]),dc:title,literal(type('http://www.w3.org/2001/XMLSchema#string',TrackTitle)))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/work/',TrackID]),rdf:type,mo:'MusicalWork')
	,	rdf(pattern(['http://dbtune.org/bbc/peel/work/',TrackID]),rdfs:label,literal(type('http://www.w3.org/2001/XMLSchema#string',TrackTitle)))
	].


match:
	(peel:session_track(TrackID,_,TrackTitle,File),File\='')
		eq
	[
		rdf(pattern(['http://dbtune.org/bbc/peel/perf_work/',TrackID]),mo:recordedAs,pattern(['http://dbtune.org/bbc/peel/signal/',TrackID]))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/signal/',TrackID]),mo:publishedAs,pattern(['http://dbtune.org/bbc/peel/track/',TrackID]))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/signal/',TrackID]),rdf:type,mo:'Signal')
	,	rdf(pattern(['http://dbtune.org/bbc/peel/signal/',TrackID]),rdfs:label,literal(type('http://www.w3.org/2001/XMLSchema#string',pattern([TrackTitle,' signal']))))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/track/',TrackID]),rdf:type,mo:'Track')
	,	rdf(pattern(['http://dbtune.org/bbc/peel/track/',TrackID]),rdfs:label,literal(type('http://www.w3.org/2001/XMLSchema#string',TrackTitle)))
	,       rdf(pattern(['http://dbtune.org/bbc/peel/track/',TrackID]),dc:title,literal(type('http://www.w3.org/2001/XMLSchema#string',TrackTitle)))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/track/',TrackID]),mo:availableAs,pattern(['http://bbc.co.uk/music/',File])) %ooops
	,	rdf(pattern(['http://bbc.co.uk/music/',File]),rdf:type,mo:'Stream')
	].

match:
	(peel:festive_50s(ArtistID,Year,ChartPosition,TrackTitleT,Folder,_,File),peel_match:encode(TrackTitleT,TrackTitle))
		eq
	[
		rdf(pattern(['http://dbtune.org/bbc/peel/track/',ArtistID,'/',TrackTitle]),rdf:type,mo:'Track')
	,	rdf(pattern(['http://dbtune.org/bbc/peel/track/',ArtistID,'/',TrackTitle]),dc:created,literal(type('http://www.w3.org/2001/XMLSchema#date',Year)))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/track/',ArtistID,'/',TrackTitle]),mo:chart_position,literal(type('http://www.w3.org/2001/XMLSchema#int',ChartPosition)))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/track/',ArtistID,'/',TrackTitle]),mo:availableAs,pattern(['http://bbc.co.uk/music/',Folder,'/',File])) % oops
	,	rdf(pattern(['http://dbtune.org/bbc/peel/track/',ArtistID,'/',TrackTitle]),dc:title,literal(type('http://www.w3.org/2001/XMLSchema#string',TrackTitleT)))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/track/',ArtistID,'/',TrackTitle]),rdfs:label,literal(type('http://www.w3.org/2001/XMLSchema#string',TrackTitleT)))
	].

match:
	(peel:festive_50s(ArtistID,_,_,TrackTitleT,_,ISRC,_),ISRC\='noisrc',peel_match:encode(TrackTitleT,TrackTitle))
		eq
	[
		 rdf(pattern(['http://dbtune.org/bbc/peel/signal/',ArtistID,'/',TrackTitle]),mo:publishedAs,pattern(['http://dbtune.org/bbc/peel/track/',ArtistID,'/',TrackTitle]))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/signal/',ArtistID,'/',TrackTitle]),rdf:type,mo:'Signal')
	,	rdf(pattern(['http://dbtune.org/bbc/peel/signal/',ArtistID,'/',TrackTitle]),rdfs:label,literal(type('http://www.w3.org/2001/XMLSchema#string',pattern([TrackTitleT,' signal']))))
	,	 rdf(pattern(['http://dbtune.org/bbc/peel/signal/',ArtistID,'/',TrackTitle]),mo:isrc,literal(ISRC))
	].

%link festive_50s with the rest of the session information, if it is possible
match:
	(peel:festive_50s(ArtistID,_,_,TrackTitleT,_,_,_),peel:session_track(TID,SID,TrackTitleT,_),peel:session(SID,ArtistID,_,_,_,_,_,_),peel_match:encode(TrackTitleT,TrackTitle))
		eq
	[
		rdf(pattern(['http://dbtune.org/bbc/peel/track/',ArtistID,'/',TrackTitle]),owl:sameAs,pattern(['http://dbtune.org/bbc/peel/track/',TID]))
	,	rdf(pattern(['http://dbtune.org/bbc/peel/signal/',ArtistID,'/',TrackTitle]),owl:sameAs,pattern(['http://dbtune.org/bbc/peel/signal/',TID]))
	].

encode(A,B) :-
	url:www_form_encode(A,AA),
	rdf_db:rdf_atom_md5(AA,1,B).


