:- module(lastfm_utils,
	[ lastfm_images/6,		% +Source, +RdfNode, +Extents, +LabelPart, +ImageProperty, -Triples
	  uts_to_date/2			% +UTS, -Date
	]).

:- use_module(library('semweb/rdf_db')).

:- use_module(lastfm_namespaces).

/** <module> Last.fm utils

This module is for general transformation processes from Last.fm source information (to RDF).

@author		Thomas Gängler
@version	1.0 
@copyright	Thomas Gängler; 2010
*/

%%	lastfm_images(+Source, +RdfNode, +Extents, +LabelPart, +ImageProperty, -Triples)
%
% 	Converts Last.fm image information to RDF triples.
	
lastfm_images(Source,RdfNode,[Extent|Extents],LabelPart,ImageProperty,Triples) :-
	lastfm_image(Source,RdfNode,Extent,LabelPart,ImageProperty,ImageTriples),
	lastfm_images(Source,RdfNode,Extents,LabelPart,ImageProperty,Triples2),
	append(ImageTriples,Triples2,Triples).
    
lastfm_images(Source,RdfNode,[],LabelPart,ImageProperty,[]) :-
	Source=Source,
	RdfNode=RdfNode,
	LabelPart=LabelPart,
	ImageProperty=ImageProperty.

%% 	lastfm_image(+Source, +RdfNode, +Extent, +LabelPart, +ImageProperty, -Triples)
%
% 	Converts information from one Last.fm image to RDF triples.
	
lastfm_image(Source,RdfNode,Extent,LabelPart,ImageProperty,[
		rdf(RdfNode,NS:Property,ImageUri)
	,	rdf(ImageUri,rdf:type,foaf:'Image')
	,	rdf(ImageUri,rdf:about,literal(Image))
	,	rdf(ImageUri,terms:extent,literal(Extent))
	,	rdf(ImageUri,rdfs:label,literal(ImageLabel))]) :-	
	member(element(image,[size=Extent],[Image]),Source),!,
	format(atom(ImageLabel),'Last FM ~w Image: (~w)',[LabelPart,Extent]),
	ImageProperty=[NS,Property],
	rdf_bnode(ImageUri).
	
lastfm_image(Source,RdfNode,Extent,LabelPart,ImageProperty,[]) :-	
	member(element(image,[size=Extent],_),Source),
	LabelPart=LabelPart,
	RdfNode=RdfNode,
	ImageProperty=ImageProperty.

%%	uts_to_date(+UTS, -Date)
%
% 	Converts a UTS date information to xmls:dateTime conform date format.
	
uts_to_date(UTS,Date) :-
    atom_to_term(UTS,Time,[]),
	stamp_date_time(Time,date(Year,Month,Day,Hour,Minute,Seconds,_,_,_),'UTC'),
	term_to_atom(Year,Y),term_to_atom(Month,Mo),term_to_atom(Day,D),term_to_atom(Hour,H),term_to_atom(Minute,Mi),term_to_atom(Seconds,S),
	((atom_chars(Mo,MoC),length(MoC,1))->atom_chars(Mo2,['0'|MoC]);Mo2=Mo),
	((atom_chars(D,DC),length(DC,1))->atom_chars(D2,['0'|DC]);D2=D),
	((atom_chars(H,HC),length(HC,1))->atom_chars(H2,['0'|HC]);H2=H),
	((atom_chars(Mi,MiC),length(MiC,1))->atom_chars(Mi2,['0'|MiC]);Mi2=Mi),
	((atom_chars(S,SC),length(SC,1))->atom_chars(S2,['0'|SC]);S2=S),
	format(atom(Date),'~w-~w-~wT~w:~w:~wZ',[Y,Mo2,D2,H2,Mi2,S2]).
