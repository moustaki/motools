:- module(crowl,[init/0,crawl_track/0,crawl_type/1,kill/0,crawl_forall/2]).

:- use_module(library('semweb/rdf_db')).
:- use_module('rdf_http_plugin').


init :-
	crawlers(N),
	create_crawlers_pool(N).
kill :-
	crawlers(N),
	stop_crawlers(N),sleep(1),
	message_queue_destroy(jobs).

crawl_forall(Goal,URI) :-
	forall(Goal,thread_send_message(jobs,URI)).

crawl_zg :-
	forall(
		( (rdf_db:rdf_subject(A) ; (rdf_db:rdf(_,_,A,_),atomic(A))),
		  atom_concat('http://zitgist.com/',_,A)
		),
		thread_send_message(jobs,A)
		).

crawl_track :-
	crawl_type('http://purl.org/ontology/mo/Track').
crawl_record :-
	crawl_type('http://purl.org/ontology/mo/Record').
crawl_artist :-
	crawl_type('http://purl.org/ontology/mo/Artist').
crawl_type(Type) :-
	forall((rdf_db:rdf(A,rdf:type,Type),atom_concat('http://zitgist.com/',_,A)),thread_send_message(jobs,A)).


/**
 * Crawler pool
 */

:- consult(config).

create_crawlers_pool(N) :-
	message_queue_create(jobs),
	forall(between(1,N,_),thread_create(crawler(jobs),_,[detached(true)])).

crawler(Queue) :-
	repeat,
	thread_get_message(Queue,URI),format(' - Received ~w\n',[URI]),
	(URI=stop -> (format(' - Exiting...\n'),thread_exit(true));(
		uri_url(URI,URL),
		load(URL),fail)).

load(URL) :-
	catch((rdf_load(URL), format(' - Loaded ~w\n',[URL])),_,
		(
		format(' - Failed to load ~w\n',[URL])%,
		%assert(failed(URL))
		)
	).

/**
 * Dismiss crawlers
 */
stop_crawlers(N) :-
	forall(between(1,N,_),thread_send_message(jobs,stop)).


uri_url(URI,URL) :-
        parse_url(URI,List),
	select(fragment(_),List,Rest),!,
	parse_url(URL,Rest). 
uri_url(URI,URI).
