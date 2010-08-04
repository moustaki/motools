:- module(lastfm_api_query,
		[ lastfm_api_query_rdf/4,			% +QueryParamsTemplate, +QueryParams, +RootNode, -Xml
		  crypt_api_method_signature/3,		% +SignatureTemplate, +SignatureTemplateList, -ApiSignatureEncrypted
		  lastfm_auth/1						% -SessionKey
		]).

:- use_module(library('http/http_open')).
:- use_module(library('semweb/rdf_db')).
:- use_module(library('www_browser')).

:- use_module(lastfm_namespaces).
:- use_module(lastfm_config).
:- use_module(log).

/** <module> Last.fm API query

This module is for Last.fm API query related stuff.

@author		Thomas Gängler
@version	1.0 
@copyright	Thomas Gängler; 2010
*/

%%	lastfm_api_authtoken_method(+LFM_API_AUTHTOKEN_METHOD)
%
%	Defines the method for fetching a Last.fm token.

lastfm_api_authtoken_method('auth.getToken').

%%	lastfm_api_authsession_method(+LFM_API_AUTHTOKEN_METHOD)
%
%	Defines the method for fetching a Last.fm session key.

lastfm_api_authsession_method('auth.getSession').
 
%%	lastfm_api_query_rdf(+QueryParamsTemplate, +QueryParams, +RootNode, -Xml)
%
%	Initializes the Last.fm API query and checks the response.
 
lastfm_api_query_rdf(QueryParamsTemplate,QueryParams,RootNode,Xml) :-
	format(atom(QueryMethods),QueryParamsTemplate,QueryParams),
	query_lastfm_api(QueryMethods,Xml1),
	member(element(lfm,_,Xml2),Xml1),
	member(element(RootNode,_,Xml),Xml2).
	
%%	query_lastfm_api(+QueryParams, -Xml)
%
%	Access to a Prolog representation of the XML last.fm feeds.
%	Returns 400 if it is a bad request and stops.
 
query_lastfm_api(QueryParams,Xml) :-
	lastfm_api_key(LFMK),
	lastfm_api_host(LFMH),
	format(atom(Url),'~w?~w&api_key=~w',[LFMH,QueryParams,LFMK]),
	log:log('Last.fm API query URL: ~w',[Url]),
	http_open(Url,Stream,[]),
	load_xml_file(Stream,Xml),close(Stream).

%%	lastfm_auth(-SessionKey)
%
%	Requests a Last.fm session key.
%
% 	@tbd 	Wait for user interaction during the authentification (2nd step), e.g. generate a continue button

lastfm_auth(SessionKey) :-
	lastfm_api_key(LFMK),
    
	% step 1: fetch auth token
	lastfm_api_authtoken_method(LFMAT),
	crypt_api_method_signature('method~w',[LFMAT],ApiSignatureEncrypted),
	lastfm_api_query_rdf('method=~w&api_sig=~w',[LFMAT,ApiSignatureEncrypted],token,[Token]),
	
	%step 2: authorize auth token
	lastfm_auth_token(LFMK,Token),
	
	%step 3: fetch session key
	lastfm_api_authsession_method(LFMAS),
	crypt_api_method_signature('method~wtoken~w',[LFMAS,Token],ApiSignatureEncrypted2),
	lastfm_api_query_rdf('method=~w&token=~w&api_sig=~w',[LFMAS,Token,ApiSignatureEncrypted2],session,Session),
	member(element(key,_,[SessionKey]),Session).

%%	crypt_api_method_signature(+SignatureTemplate, +SignatureTemplateList, -ApiSignatureEncrypted)
%
%	Encrypts the API signature.
	
crypt_api_method_signature(SignatureTemplate,SignatureTemplateList,ApiSignatureEncrypted) :-
	lastfm_api_key(LFMK),
	lastfm_api_secret(LFMS),
	append([LFMK],SignatureTemplateList,STL2),
	append(STL2,[LFMS],STL3),
	concat('api_key~w',SignatureTemplate,ST2),
	concat(ST2,'~w',ST3),
	format(atom(ApiSignature),ST3,STL3),
	rdf_atom_md5(ApiSignature,1,ApiSignatureEncrypted).

%%	lastfm_auth_token(+LFMK, +Token)
%
%	Opens a webbrowser for user confirmation during the authentification process.
%
%	@tbd 	interrupt authentification process during the conformation
	
lastfm_auth_token(LFMK,Token) :-
	lastfm_host(LFMH),
	format(atom(Url),'~wapi/auth/?api_key=~w&token=~w',[LFMH,LFMK,Token]),
	www_open_url(Url).

