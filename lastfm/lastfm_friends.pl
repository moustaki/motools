:- module(lastfm_friends,[friends_rdf/2]).

:- use_module(library('http/http_open')).
:- use_module(library('semweb/rdf_db')).

:- use_module(namespaces).
:- use_module(config).

friends_rdf(User,[rdf(URI,rdf:type,foaf:'Person'),rdf(URI,rdfs:label,literal(User)),rdf(URI,foaf:holdsAccount,Account),rdf(Account,rdf:type,foaf:'OnlineAccount'),rdf(Account,foaf:isPrimaryTopicOf,Page),rdf(Account,foaf:accountServiceHomepage,'http://www.last.fm/'),rdf(Account,foaf:accountName,literal(User))|Triples]) :-
	friends_xml(User,[element(friends,_,Friends)]),!,
	findall(Rdf,friend_rdf(Friends,User,Rdf),T),
	flatten(T,Triples),%rdf_global_term(TT,Triples),
	rdf_bnode(Account),
	host(Host),
	format(atom(URI),'~w/~w',[Host,User]),
	format(atom(Page),'http://www.last.fm/user/~w',[User]).


friend_rdf(Friends,User1,[rdf(URI1,foaf:knows,URI2),rdf(URI2,foaf:img,Image),rdf(URI2,foaf:holdsAccount,Account),rdf(Account,rdf:type,foaf:'OnlineAccount'),rdf(Account,foaf:primaryTopicOf,Page),rdf(Account,foaf:accountServiceHomepage,'http://www.last.fm/'),rdf(Account,foaf:accountName,literal(User2))]) :-
	friend(Friends,User2,Page,Image),
	rdf_bnode(Account),
	host(Host),
	format(atom(URI1),'~w/~w',[Host,User1]),
	format(atom(URI2),'~w/~w',[Host,User2]).
friend(Friends,User2,Page,Image) :-
	%friends_xml(User1,[element(friends,_,Friends)]),
	member(element(user,[username=User2],Info),Friends),
	info(Info,Page,Image).


info(Info,Page,Image) :-
	member(element(url,_,[Page]),Info),
	member(element(image,_,[Image]),Info).
	



friends_xml(User,Xml) :-
	format(atom(URL),'http://ws.audioscrobbler.com/1.0/user/~w/friends.xml',[User]),
	http_open(URL,Stream,[]),
	load_xml_file(Stream,Xml),
	close(Stream).


