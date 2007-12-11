:- module(bbc,[bbc/0]).

:- use_module(musicbrainz) . /* for mbz_url_to_id */
:- use_module(library('semweb/rdf_db')) .

:- use_module(namespaces).

:- assert(isArtistType('http://purl.org/ontology/mo/MusicArtist')).
:- assert(isArtistType('http://purl.org/ontology/mo/SoloMusicArtist')).

bbc :- findall(Artist, (rdf_db:rdf(Artist, rdf:type, X), isArtistType(X)), Artists), 
   forall(
      ( member(Artist,Artists),
        atom_concat('http://zitgist.com/music/artist/',_,Artist),
		mbz_url_to_id(Artist, MbzID),
		atom_concat(MbzID,'.rdf#person', End), % I'm sure there's a better way to do this ? I can't get [MbzID, '.rdf#person'] to work in place of End in the line below...
		atom_concat('http://bbc-hackday.dyndns.org:2825/music/artists/', End, BBCURI)
      ),
      rdf_assert(Artist, owl:sameAs, BBCURI)
      ).
