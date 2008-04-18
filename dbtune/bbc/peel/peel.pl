:- module(peel,[
		artist/4
	,	festive_50s/7
	,	session/8
	,	session_band_member/4
	,	session_track/4
	]).


:- use_module('../pldata/artists').
:- use_module('../pldata/sessions').
:- use_module('../pldata/sessionslineup').
:- use_module('../pldata/sessiontracks').
:- use_module('../pldata/festive50').


artist(Id,Name,Biography,Picture) :-
	artists:csv([Id,Name,Picture,Biography]).

festive_50s(ArtistID,Year,ChartPosition,TrackTitle,Folder,ISRC,File) :-
	festive50:csv([ArtistID,Year,ChartPosition,TrackTitle,Folder,ISRC,File]).

session(SessionId,ArtistID,TransmissionDate,RecordDate,Producer,Engineer1,Engineer2,Studio) :-
	sessions:csv([ArtistID,SessionId,TransmissionDate,RecordDate,Producer,Engineer1,Engineer2,Studio]).

session_band_member(ArtistID,SessionID,Performer,Instrument) :-
	sessionslineup:csv([ArtistID,SessionID,Performer,Instrument]).

session_track(TrackID,SessionID,TrackTitle,File) :-
	sessiontracks:csv([TrackID,SessionID,TrackTitle,File]).


