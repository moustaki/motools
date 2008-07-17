:- module(literal_entailment,[rdf/3]).

:- use_module(library('semweb/rdf_db'),[rdf_bnode/1]).
:- use_module(library('semweb/rdf_litindex')).



rdf(S,'http://purl.org/ontology/swi#soundslike',O) :-
	\+var(S),
	S = literal(Literal),
	literal_to_spec(Literal,Spec),
	rdf_find_literals(Spec,List),
	member(Lit,List),
	rdf_db:rdf(O,_,literal(Lit)).
rdf(S,P,O) :-
	rdf_db:rdf(S,P,O).

literal_to_spec(Literal,Spec):-
	concat_atom(List,' ',Literal),
	literal_to_spec2(List,Spec).
literal_to_spec2([Head,Tail],and(sounds(Head),sounds(Tail))):- !.
literal_to_spec2([Head|Tail],and(sounds(Head),Tail2)) :-
	literal_to_spec2(Tail,Tail2).


/**
 * We now register the rdf/3 predicate to 
 * be used as an entailment module within the
 * SeRQL SWI Semantic Web server.
 */


                 /*******************************
                 *             REGISTER         *
                 *******************************/

:- multifile
        serql:entailment/2.

serql:entailment(lit, literal_entailment).

