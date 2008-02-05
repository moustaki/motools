:- module(p2r_entailment,[compile/0
	]).

:- use_module(library('semweb/rdf_db'),
              [ rdf_global_id/2,
	        rdf_global_term/2,
                rdf_reachable/3,
                rdf_has/3,
                rdf_subject/1,
                rdf_equal/2,
		rdf_global_term/2,
		rdf_atom_md5/3
	      ]).

:- use_module(match).


term_expansion((rdf(S0, P0, O0) :- Body),
               (rdf(S,  P,  O)  :- Body)) :-
        rdf_global_id(S0, S),
        rdf_global_id(P0, P),
        rdf_global_id(O0, O).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


compile :-
	forall(match:eq(Pred,Triples),(
		forall(member(rdf(A,B,C),Triples),(
			goal(A,S,GA),goal(B,P,GB),goal(C,O,GC),
			optimise(rdf(S,P,O),GA,GB,GC,Pred,OptimisedGoal),
			rdf_global_term(':-'(rdf(S,P,O),(writeln(rdf(S,P,O)),OptimisedGoal)),GlobalClause),
			assert(GlobalClause),
			format(user_error,' - Asserting rule: rdf(~w,~w,~w) :- ~w, ~w, ~w, ~w.\n',[S,P,O,Pred,GA,GB,GC])
		))
	)).



goal(A,Node,matches(List,Node)) :- \+var(A),A=pattern(List),!.
goal(N,N,true).
	

optimise(rdf(S,P,O),GoalS,GoalP,GoalO,Pred,(
		(atomic(S)->GoalS;true),
		(atomic(P)->GoalP;true),
		(atomic(O)->GoalO;true),
		Pred,
		(atomic(S)->true;GoalS),
		(atomic(P)->true;GoalP),
		(atomic(O)->true;GoalO)
	)).
	

matches(Atom,Atom) :- \+is_list(Atom),!.
matches(Pattern,Atom) :-
	ground(Pattern),!,
	concat_atom(Pattern,Atom).
matches([],'') :- !.
matches([H|T],Atom) :-
	ground(H),
	atom_concat(H,Rest,Atom),
	matches(T,Rest).
matches([H|T],Atom) :-
	var(H),
	atom_concat(H,Rest,Atom),
	matches(T,Rest).

%rdf(Subject,Predicate,Object) :-
%	rdf_global_id(Subject,SubjectX),rdf_global_id(Predicate,PredicateX),rdf_global_id(Object,ObjectX),
%	match:eq(Pred,Triples),
%        expand_t(Triples,TriplesX),
%	member_m(rdf(SubjectX,PredicateX,ObjectX),TriplesX,rdf(SM,_,OM)),
%	Pred,
%	(
%		(SM=pattern(ListA),concat_atom(ListA,SubjectX));
%		(atomic(SM),SubjectX=SM)
%		),
%	(
%		(OM=pattern(ListB),concat_atom(ListB,ObjectX));
%		(OM=literal(pattern(ListB)),concat_atom(ListB,ObjectXX),ObjectX=literal(ObjectXX));
%		(OM=literal(type(Type,pattern(ListB))),concat_atom(ListB,ObjectXX),ObjectX=literal(type(Type,ObjectXX)));
%		((atomic(OM);(OM=literal(P),P\=pattern(_),P\=type(_,_));(OM=literal(type(_,P)),P\=pattern(_))),ObjectX=OM)
%		).

%member_m(_,[],_) :- fail.
%member_m(rdf(S,P,O),[rdf(SM,PM,OM)|_],rdf(SM,PM,OM)) :-
%	pattern_match(SM,S),pattern_match(PM,P),pattern_match(OM,O).
%member_m(rdf(S,P,O),[_|T],rdf(SM,PM,OM)) :-
%	member_m(rdf(S,P,O),T,rdf(SM,PM,OM)).

pattern_match(P,A) :- var(A),\+var(P), P=literal(type(_,Pattern)), pattern(Pattern),!.
pattern_match(P,A) :- var(A), \+var(P), P=literal(Pattern),pattern(Pattern),!.
pattern_match(P,A) :- var(A), pattern(P),!.
pattern_match(P,A) :- atomic(A),pattern(P),!, pattern_match_p(P,A).
pattern_match(P,A) :- atomic(A),\+var(P), P=literal(Pattern),pattern(Pattern),!, pattern_match_lit(P,A).
pattern_match(P,A) :- atomic(A),\+var(P), P=literal(type(_,Pattern)),pattern(Pattern),!, pattern_match_lit(P,A).
pattern_match(A,A).
pattern_match_p(pattern([]),'').
pattern_match_p(pattern([H|T]),Atom) :- atomic(Atom),
	atom_concat(H,Atomtail,Atom),
	pattern_match(pattern(T),Atomtail).
pattern_match_lit(literal(pattern(Pattern)),literal(Atom)) :- pattern_match_p(pattern(Pattern),Atom).
pattern_match_lit(literal(type(Type,pattern(Pattern))),literal(type(Type,Atom))) :- pattern_match_p(pattern(Pattern),Atom).
%
%expand_t([],[]).
%expand_t([rdf(A,B,C)|T],[rdf(AX,BX,CX)|TX]) :-
%	rdf_global_id(A,AX),rdf_global_id(B,BX),rdf_global_id(C,CX),
%	expand_t(T,TX).
%
pattern(Pattern) :- \+var(Pattern),Pattern=pattern(_).


                 /*******************************
                 *             REGISTER         *
                 *******************************/

:- multifile
        serql:entailment/2.

serql:entailment(p2r, p2r_entailment).




