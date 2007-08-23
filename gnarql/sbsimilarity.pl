:- module(sbsimilarity,[sbsimilarity/0]).

:- use_module(musicbrainz) . /* for mbz_url_to_id */
:- use_module(library('semweb/rdf_db')) .

:- use_module(namespaces).

sbsimilarity :- findall(Signal, rdf_db:rdf(Signal, rdf:type, 'http://purl.org/ontology/mo/Signal'), Signals), 
   forall(
      ( member(Signal,Signals),
        atom_concat('http://zitgist.com/music/signal/',_,Signal),
	mbz_url_to_id(Signal, MbzID),
	atom_concat('http://isophonics.net/music/signal/', MbzID, IPURI)
      ),
      rdf_assert(A, owl:sameAs, IPURI)
      ).
