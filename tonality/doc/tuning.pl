:- use_module('/home/david/onto_spec').
:- use_module(library('semweb/rdf_db')).
:- use_module(library('semweb/rdf_turtle')).

:- rdf_load('tuning.rdf').

author_name('David Pastor Escuredo').
author_foaf('David Pastor Escuredo').
page_title('Tuning Otology').

glance(G):-
	glance_html_desc(G).

class(C):-
	classes_html_desc(C).

prop(P):-
	props_html_desc(P).

:-gen('tuning.html').
