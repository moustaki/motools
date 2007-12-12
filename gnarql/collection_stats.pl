:- module(collection_stats,[stats/1]).

:- use_module(library('semweb/rdf_db')).


num_artists(NA) :- findall((S,_,_,_),
						(rdf_db:rdf(S,rdf:type,mo:'MusicArtist',_), \+rdf_is_bnode(S)),
						Quads
						),
						list_to_set(Quads, QuadSet),
				length(QuadSet, NA).

stats(X) :- num_artists(NA), atom_concat(NA,' known artists', X).
