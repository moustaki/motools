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




                 /*******************************
                 *             REGISTER         *
                 *******************************/

:- multifile
        serql:entailment/2.

serql:entailment(p2r, p2r_entailment).




