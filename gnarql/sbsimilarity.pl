:- use_module(musicbrainz) . /* for mbz_url_to_id */
:- use_module(library('semweb/rdf_db')) .

:- rdf_register_ns(mo, 'http://purl.org/ontology/mo/') .


:- forall(
 			(bagof(Signal, rdf_db:rdf(A, rdf:type, 'http://purl.org/ontology/mo/Signal'), Signals),  % Use bagof to avoid db deadlock
			atom_concat('http://zitgist.com/music/signal/', _, A), % Check that it is a ZG URI
			mbz_url_to_id(A, MbzID),
			atom_concat('http://isophonics.net/music/signal/', MbzID, IPURI)),
			
			rdf_assert(A, owl:sameAs, IPURI) 
		  ) .
