:- module(lastfm_friends,
		[ friends_rdf/2		% +User, -Triples
		]).

:- use_module(library('http/http_open')).
:- use_module(library('semweb/rdf_db')).

:- use_module(lastfm_namespaces).
:- use_module(lastfm_api_query).
:- use_module(lastfm_config).
:- use_module(lastfm_utils).

/** <module> Last.fm friends to RDF converter

This module converts the friends graph of a Last.fm user to RDF.

@author		Yves Raimond, 
			Thomas Gängler
@version 	2.0  
@copyright	Yves Raimond, Thomas Gängler; 2008 - 2010
*/

%%	lastfm_api_method(+LFM_API_METHOD)
%
%	Defines the method for fetching events.
 
lastfm_api_method('user.getFriends').

%%	lastfm_api_response_rootnode(+LFM_API_RESPONSE_ROOTNODE)
%
%	Defines the root node of the Last.fm API response (not 'lfm').

lastfm_api_response_rootnode('friends').

%%	friends_rdf(+User, -Triples)
%
%	Converts the Last.fm friends graph of a given user to RDF triples.

friends_rdf(User,[
		rdf(UserUri,rdf:type,foaf:'Person')
	,	rdf(UserUri,rdfs:label,literal(User))
	,	rdf(UserUri,foaf:holdsAccount,Account)
	,	rdf(Account,rdf:type,foaf:'OnlineAccount')
	,	rdf(Account,foaf:isPrimaryTopicOf,LFMUserPage)
	,	rdf(Account,foaf:accountServiceHomepage, LFMH)
	,	rdf(Account,foaf:accountName,literal(User))|Triples]) :-
	host(Host),
	lastfm_host(LFMH),
	lastfm_api_method(LFMM),
	lastfm_api_response_rootnode(LFMRRN),
	lastfm_api_query_rdf('method=~w&user=~w',[LFMM,User],LFMRRN,Xml),!,
	format(atom(LFMUserPage),'~wuser/~w',[LFMH,User]),
	format(atom(UserUri),'~w/lfm-user/~w',[Host,User]),
	findall(Triples,
		(member(element(user,_,Friend),Xml),friend_rdf(UserUri,Friend,Triples)),
		BT),
	flatten(BT,Triples),
	rdf_bnode(Account).

%%	friend_rdf(+UserURi, +Friend, -Triples)
%
%	Converts a Last.fm friend representation to RDF triples.

friend_rdf(UserUri,Friend,[
		rdf(UserUri,foaf:knows,FriendUri)
	,	rdf(FriendUri,rdf:type,foaf:'Person')
	,	rdf(FriendUri,foaf:holdsAccount,FriendAccount)
	,	rdf(FriendAccount,rdf:type,foaf:'OnlineAccount')
	,	rdf(FriendAccount,foaf:isPrimaryTopicOf,LFMFriendPage)
	,	rdf(FriendAccount,foaf:accountServiceHomepage,LFMH)
	,	rdf(FriendAccount,foaf:accountName,literal(FriendName))|Triples]) :-
	host(Host),
	lastfm_host(LFMH),
	member(element(name,_,[FriendName]),Friend),
	rdf_bnode(FriendAccount),
	format(atom(FriendUri),'~w/lfm-user/~w',[Host,FriendName]),
	friend_realname_info(Friend,FriendAccount,RealnameTriples),
	lastfm_images(Friend,FriendAccount,['small','medium','large','extralarge'],'Friend',['foaf','img'],FriendImagesTriples),
	append(RealnameTriples,FriendImagesTriples,Triples),
	member(element(url,_,[LFMFriendPage]),Friend).

%%	friend_realname_info(+Friend, ?FriendAccount, -Triples)
%
%	Looks for the real name of the friend into the Last.fm friend representation
	
friend_realname_info(Friend,FriendAccount,[rdf(FriendAccount,foaf:name,literal(FriendRealname))]) :-
	member(element(realname,_,[FriendRealname]),Friend),!.
    
friend_realname_info(Friend,FriendAccount,[]) :-
	member(element(realname,_,_),Friend),
	FriendAccount=FriendAccount.


