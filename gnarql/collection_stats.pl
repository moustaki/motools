:- module(collection_stats,[stats/1]).

:- use_module(library('semweb/rdf_db')).

% Naive approaches :
% (probly want eg. to check they're associated with files on disk rather than just discovered on the web)

:- rdf_meta num_by_type(-,r).
num_by_type(N, Type) :- findall((S,_,_,_),
						(rdf_db:rdf(S,rdf:type,Type,_), \+rdf_is_bnode(S)),
						Quads
						),
						list_to_set(Quads, QuadSet),
						length(QuadSet, N).


num_artists(NA) :- num_by_type(NA,mo:'MusicArtist').
num_albums(NB)  :- num_by_type(NB,mo:'Record').
num_tracks(NT)  :- num_by_type(NT,mo:'Track').


stats(X) :- num_artists(NA), num_albums(NB), num_tracks(NT),
			sformat(X, '~w artists, ~w albums, ~w tracks', [NA,NB,NT]).