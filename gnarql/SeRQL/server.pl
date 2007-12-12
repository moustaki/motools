/*  This file is part of ClioPatria.

    Author:
    HTTP:	http://e-culture.multimedian.nl/
    GITWEB:	http://gollem.science.uva.nl/git/ClioPatria.git
    GIT:	git://gollem.science.uva.nl/home/git/ClioPatria.git
    GIT:	http://gollem.science.uva.nl/home/git/ClioPatria.git
    Copyright:  2007, E-Culture/MultimediaN

    ClioPatria is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.

    ClioPatria is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ClioPatria.  If not, see <http://www.gnu.org/licenses/>.
*/

:- module(server,
	  [ server/0,
	    restrict_server/0,		% Update security
	    daemon/0,
	    canonical_host/1		% -HostName
	  ]).

% First setup search paths
:- load_files(paths, [silent(true)]).
% Load PlDoc
:- load_files(pldoc, [silent(true)]).
% Namespaces are needed everywhere
:- load_files(namespaces, [ silent(true)]).

% Load these into module user, so we can use them from the toplevel
% for interactive exploration of the triples.

:- load_files([ user:library('semweb/rdf_db'),
		user:library('semweb/rdf_turtle')
	      ],
	      [ silent(true) ]).


% NOTE: namespaces (rdf_register_ns/2) are defined in namespaces.pl
% loaded in parms.pl, and then loaded again to overrule old declarations 
% in getty(t20getty)

:- load_files([ serql(load),
		serql(serql_log),
		serql(user_db),		% Deny actions
		library(lists),
		version,
		util(state),
		util(user_profile),
		util(interface_util),
		rdfbrowsing(load),
		util(rdf_util),
		util(fuzzy),
		search_keyword(http_search),
		api(http_tree),
		util(http_util),
		util(http_files),
		util(html_util),
		library('http/html_write'),
		library('http/http_dispatch'),
		library('http/http_authenticate'),
		library('semweb/rdf_persistency'),
		library('semweb/rdf_litindex'),
		library('semweb/rdf_http_plugin'),
		library('semweb/rdf_zlib_plugin'),
		library(socket),
		library(settings),
		%		  user:serql(debug),
		library('http/http_error'),
		% user:artchive_base(artchive),
		fbrowse(fbrowse),
		relsearch(relation_search),
		rdfbrowsing(browser),
		suggest(suggest),
		annotate(annotate),
		annotate(picturepoint),		  
		myart(myart),
		api(load),
		maintain(backtrace)
	      ],
	      [ silent(true),
		if(not_loaded)
	      ]).
:- load_files([ application(load)
	      ],
	      [ silent(true),
		if(not_loaded)
	      ]).


:- multifile
	mime:mime_extension/2.

mime:mime_extension(class, application/'octet-stream').
mime:mime_extension(kml, application/'vnd.google-earth.kml+xml').
mime:mime_extension(kmz, application/'vnd.google-earth.kmz').
mime:mime_extension(js, text/javascript).
mime:mime_extension(vbs, text/vbscript).
mime:mime_extension(ico, image/'x-ico').
mime:mime_extension(jar, application/'java-archive').
mime:mime_extension(swf, application/'x-shockwave-flash').
mime:mime_extension(xspf, application/'xspf+xml').
mime:mime_extension(mp3, audio/mpeg).
mime:mime_extension(svg,  image/'svg+xml').

%%	server
%
%	Start the Semantic Web based E-culture  server. Settings such as
%	the port to use are loaded from setting/2.
%	
%	Starting the server  loads  the   persistent  database  from the
%	directory =|SeRQL-store|=. To start from   scratch,  delete this
%	directory and load the initial state as described in README.

server :-
	init_state_options,
	
	restrict_server,
	serql_server([ base_ontologies([]),
		       after_load(server:(%attach_picture_point_trigger,
					  stem_literals))
		     ]),
	rdf_persistency(anonymous_user_settings, false),
	rdf_check_changed_sources(list),
	compile_iface_owl_class.
	

%%	restrict_server
%
%	Restrict some operations on the  server   for  all  users except
%	admin. We do not want someone to delete our work by accident!

restrict_server :-
	retractall(user_db:denied(_)),	% HACK
					% /servlets/unloadSource
	deny_all_users(write(_, unload(_))),
					% /servlets/uploadData
					% /servlets/uploadFile
					% /servlets/uploadURL
%	deny_all_users(write(_, load(_))),
	deny_all_users(write(_, remove_statements(-,_,_))),
	deny_all_users(write(_, remove_statements(_,-,_))).


%%	daemon
%
%	Start as a deamon.  See the script =daemon.sh=.

daemon :- 
	write_state([state=initializing]),
	rdf_set_literal_index_option([verbose(false)]),
	catch(server, E, server_failed(E)),
	write_state([state=running]),
	on_signal(hup,  _, stop_daemon),
	on_signal(term, _, stop_daemon),
	on_signal(int,  _, stop_daemon),
	on_signal(segv, _, default),
	on_signal(bus,  _, default),
	on_signal(fpe,  _, default),
	loop.

server_failed(E) :-
	print_message(error, E),
	write_state([state=error]),
	halt(1).

loop :-
	sleep(10000),
	loop.

%%	stop_daemon(+Signal)
%
%	We received Signal.  Add message to log-file and die.

stop_daemon(Signal) :-
	format(user_error, 'Stopping daemon on signal ~w ...~n', [Signal]),
	serql_log('~q.~n', [signal(Signal)]),
	write_state([state=stopped]),
	halt.

%%	canonical_host(-Host)
%	
%	Canonical name of the host in *lowercase*.

:- dynamic
	canonical_host_cache/1.

canonical_host(Host) :-
	canonical_host_cache(Host0), !,
	Host = Host0.
canonical_host(Host) :-
	(   getenv('HOST', Host0)	% allow redefining
	->  true
	;   gethostname(Host0)
	),
	downcase_atom(Host0, Host),
	assert(canonical_host_cache(Host)).

%%	write_state(+State) is det.
%
%	Write current state to a file.  Name of the file is in environment
%	variable =SERQL_STATE_FILE=.
%	
%	@param State	List of Name=Value pairs

write_state(State) :-
	getenv('SERQL_STATE_FILE', StateFile),
	StateFile \== none, !,
	open(StateFile, write, Out),
	forall(member(Name=Value, State),
	       format(Out, '~w: ~w~n', [Name, Value])),
	close(Out).
write_state(_).


		 /*******************************
		 *	     TRIPLE20		*
		 *******************************/

/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Add  default  Triple20  commandline  options.   --nobase  simply  starts
Triple20 without doing a scan for base ontologies.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - */

:- multifile
	triple20:option/1.

triple20:option('--nobase').
triple20:option('--nochecksaved').


		 /*******************************
		 *		REPLY		*
		 *******************************/

:- multifile
	serql_http:sidebar_menu/2.

:- http_handler('/', main_page, [priority(10)]).
:- http_handler('/favicon.ico',
		http_reply_file(www('img/favicon.ico'), []), []).
/*
serql_http:sidebar_menu(-, 'e-culture demo').
serql_http:sidebar_menu(Link, -) :- menu_link('/facet', '/facet', Link).
serql_http:sidebar_menu(Link, -) :- menu_link('/search', 'search', Link).
serql_http:sidebar_menu(Link, -) :- menu_link('/path', 'Relation Search', Link).
serql_http:sidebar_menu(Link, -) :- menu_link('/search/graph', 'Display search graphs', Link).
serql_http:sidebar_menu(Link, -) :- menu_link('/annotate', 'Annotate URL', Link).

serql_http:sidebar_menu(-, 'Deprecated').
serql_http:sidebar_menu(Link, -) :- menu_link('/search/old', 'Basic Search', Link).
serql_http:sidebar_menu(Link, -) :- menu_link('/search/advanced', 'Advanced Search', Link).
serql_http:sidebar_menu(Link, -) :- menu_link('/search/dev', 'Developer\'s Search', Link).	%'
serql_http:sidebar_menu(Link, -) :- menu_link('/facet/old', '/facet 0.1', Link).
serql_http:sidebar_menu(Link, -) :- menu_link('/localview?active=http%3a%2f%2fe-culture.multimedian.nl%2fns%2fgetty%2fulan%23associated_with', '/test localview', Link).

serql_http:sidebar_menu(-, 'Maintenance').
serql_http:sidebar_menu(Link, -) :- menu_link('/pldoc/', 'Search source', Link).
serql_http:sidebar_menu(Link, -) :- menu_link('/qa_index', 'RDF QA', Link).
serql_http:sidebar_menu(Link, -) :-
	mk_image_uri('MNlogoGifFormat.gif', Image),
	Link =
	a([target='_top' , href='http://e-culture.multimedian.nl/'],img([
           src=Image, 
	   class=logo, alt=logo, style='margin-top: 1em; border-style:none; width: 140px'])).
*/


%%	menu_link(+Location, +Label, -Link)
%
%	Create a link for the server main menu from Location and Label.

menu_link(Path, Label, Link) :-
	make_uri(FacetLink, Path, []), 
	Link = a([target='_top', href=FacetLink], Label).

%%	main_page(+Request)
%
%	Emit frameset for the E-culture demo.

main_page(_Request) :-
	make_uri(Sidebar,'/sidebar.html',[]),
	make_uri(Welcome,'/welcome.html',[]),
	phrase(html([ head(title('MultimediaN E-Culture Server')),
		      frameset([cols('200,*')],
			       [ frame([ src(Sidebar),
					 name(sidebar)
				       ]),
				 frame([ src(Welcome),
					 name(main)
				       ])
			       ])
		    ]), HTML),
	format('Content-type: text/html~n~n'),
	print_html(HTML).
