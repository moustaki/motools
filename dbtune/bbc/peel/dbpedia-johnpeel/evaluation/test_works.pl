:- module(test,[test/0]).

:- use_module(library('semweb/rdf_db')).
:- use_module(library('semweb/rdf_http_plugin')).
:- use_module(library('semweb/rdf_persistency')).
:- use_module(sparql_client).

a('all_works.xml').
eq('../dbpedia-johnpeel-works.rdf').
n(60).

sparql_a('PREFIX mo: <http://purl.org/ontology/mo/> PREFIX event: <http://purl.org/NET/c4dm/event.owl#>
	SELECT ?work ?aname WHERE {<~w> rdfs:label ?work. ?p event:usesWork <~w>. ?p2 event:hasSubEvent ?p; mo:performer ?artist. ?artist rdfs:label ?aname}'). 

:- rdf_attach_db(db2,[]).

test :-
	n(N),
	eq(File),rdf_load(File),
	forall(between(1,N,_),(
		pick(AUri),
		format(user_output,'Picking ~w\n',[AUri]),!,
		((rdf(AUri,owl:sameAs,BUri),!,rdf_load(BUri),!,display(AUri,BUri));(not_in(AUri)))
	)).
	

display(AUri,BUri) :-
	sparql_a(QueryP),
	open('answers.pl',append,S),
	format(atom(Q),QueryP,[AUri,AUri]),
	writeln(Q),
	forall(sparql_query(Q,row(literal(type(_,LW)),literal(type(_,LA))),[host('dbtune.org'),port(3030),path('/sparql/')]),format(user_output,'A is described by: ~w by ~w\n',[LW,LA])),
	forall(rdf(BUri,_,literal(lang(en,LB))),format(user_output,'B is described by: ~w\n',[LB])),
	writeln('Correct mapping? y. or n.'),
	read(Ans),
	(Ans = y -> (format(atom(Atom),'pl_ok(''~w'',''~w'').\n',[AUri,BUri]),write(S,Atom)); 
		(writeln('Why? (''answer''.)'),read(Why),format(atom(Atom2),'pl_fail(''~w'',''~w'',''~w'').\n',[AUri,BUri,Why]),write(S,Atom2))),
	close(S).

not_in(AUri) :-
	sparql_a(QueryP),
	open('answers.pl',append,S),
	format(atom(Q),QueryP,[AUri,AUri]),
	writeln(Q),
	forall(sparql_query(Q,row(literal(type(_,LW)),literal(type(_,LA))),[host('dbtune.org'),port(3030),path('/sparql/')]),format(user_output,'A is described by: ~w by ~w\n',[LW,LA])),
	writeln('Not in Wikipedia? n. or y.'),
	read(Ans),
	(Ans = n -> (format(atom(Atom),'pnl_ok(''~w'').\n',[AUri]),write(S,Atom));
		(writeln('Why? (''answer''.)'),read(Why),format(atom(Atom2),'pnl_fail(''~w'',''~w'').\n',[AUri,Why]),write(S,Atom2))),
	close(S).
	

pick(Uri) :-
	a(Test),
	format(atom(Command),'./random.sh ~w',[Test]),
	open(pipe(Command),read,S),
	get_until_nl(S,Uri),close(S).
	
get_until_nl(S,At) :-
        get_until_nl(S,'',At).
get_until_nl(S,Old,At) :-
        get_char(S,C),
        (C\='\n'->(
                atom_concat(Old,C,New),
                get_until_nl(S,New,At)
                );Old=At).



