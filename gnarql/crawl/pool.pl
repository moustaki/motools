:- module(pool,[create_crawlers_pool/1]).


:- use_module(library('semweb/rdf_db')).
:- consult('../namespaces').

% Crawler pool

create_crawlers_pool(N) :-
        forall(between(1,N,_),thread_create(crawler(jobs),_,[detached(true)])),
	message_queue_create(jobs).

crawler(Queue) :-
        repeat,
        thread_get_message(Queue,URI),%log(' - Received ~w\n',[URI]),
        (URI=stop -> (thread_exit(true));(
                uri_url(URI,URL),
                load(URL),fail)).

%load(URL) :-
%        rdf(URL,rdf:type,gnarql:'CrawledSource'),!.
load(URL) :-
        catch(
	(
		rdf_load(URL),xsd_time(Time),
		rdf_assert(URL,rdf:type,gnarql:'CrawledSource'),
		rdf_assert(URL,dc:date,literal(type('http://www.w3.org/2001/XMLSchema#dateTime',Time)))
	),_,
                (
                true
                )
        ).


uri_url(URI,URL) :-
        parse_url(URI,List),
        select(fragment(_),List,Rest),!,
        parse_url(URL,Rest).
uri_url(URI,URI).



xsd_time(Date) :-
        get_time(S),
        format_time(atom(Date),'%Y-%m-%dT%H:%M:%S',S).


