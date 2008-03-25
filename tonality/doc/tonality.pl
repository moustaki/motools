:- use_module('../../mo/ontospec/onto_spec').
:- use_module(library('semweb/rdf_db')).
:- use_module(library('semweb/rdf_turtle')).

:- rdf_load('../rdf/tonality.rdf').

:- rdf_db:rdf_register_ns(tuning,'http://purl.org/ontology/tuning/').
:- rdf_db:rdf_register_ns(to,'http://purl.org/ontology/tonality/').

author_name('David Pastor Escuredo').
author_foaf('David Pastor Escuredo').
page_title('Tonality Ontology').

output('tonality.html').

:-  output(Output),
	open(Output,write,Otp),
	header(Header),
	write(Otp,Header),
	open('intro.htm',read,Introduction),
	copy_stream_data(Introduction, Otp),
	open('../doc/glance.htm',read,GlanceIntro),
	copy_stream_data(GlanceIntro, Otp),
	glance_html_desc(Glance),
	write(Otp,Glance),
	open('../doc/spec.htm',read,SpecIntro),
	copy_stream_data(SpecIntro, Otp),
	write(Otp,'<h2 id="terms_classes">Classes</h2>'),
	classes_html_desc(Classes),
	write(Otp,Classes),
	write(Otp,'<h2 id="terms_props">Properties</h2>'),
	props_html_desc(Props),
	write(Otp,Props),
	write(Otp,'<h2 id="terms_inds">Individuals</h2>'),
	inds_html_desc(Inds),
	write(Otp,Inds),
	deprecs_html_desc(Deprecs),
	write(Otp,Deprecs),
	close(Otp),
	rdf_db:rdf_retractall(_,_,_).

:- halt.
