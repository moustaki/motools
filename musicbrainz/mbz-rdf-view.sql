/*
create text index on ZITGIST.MO.artist ("name") with key id;
create text index on ZITGIST.MO.artistalias ("name") with key id;
create text index on ZITGIST.MO.album ("name") with key id;
create text index on ZITGIST.MO.track ("name") with key id;
vt_batch_update (fix_identifier_case ('ZITGIST.MO.artist'), 'ON', NULL);
vt_batch_update (fix_identifier_case ('ZITGIST.MO.artistalias'), 'ON', NULL);
vt_batch_update (fix_identifier_case ('ZITGIST.MO.album'), 'ON', NULL);
vt_batch_update (fix_identifier_case ('ZITGIST.MO.track'), 'ON', NULL);
VT_INC_INDEX_DB_MO_artist ();
VT_INC_INDEX_DB_MO_artistalias ();
VT_INC_INDEX_DB_MO_album ();
VT_INC_INDEX_DB_MO_track ();
*/

--#
--# Making sure that the graphs and views are deleting to clean Virtuoso from the old definitions
--##############

sparql
drop quad storage virtrdf:MBZROOT.
;

--sparql drop graph virtrdf:MBZ;

sparql
drop graph map virtrdf:MBZ.
;

sparql
prefix mbz: <http://musibrainz.org/schemas/mbz#>
drop literal class mbz:duration.
;

sparql
prefix mbz: <http://musibrainz.org/schemas/mbz#>
drop literal class mbz:created.
drop literal class mbz:official_iri.
drop literal class mbz:bootleg_iri.
drop literal class mbz:promotion_iri.
drop literal class mbz:album_iri.
drop literal class mbz:single_iri.
drop literal class mbz:ep_iri.
drop literal class mbz:compilation_iri.
drop literal class mbz:soundtrack_iri.
drop literal class mbz:spokenword_iri.
drop literal class mbz:interview_iri.
drop literal class mbz:audiobook_iri.
drop literal class mbz:live_iri.
drop literal class mbz:remix_iri.
;

--#
--#The following SPARQL query will fix an issue Virtuoso has with its JSO system. Perform this query for now, the issue should be fixed in a future release
--#########
sparql define input:storage ""
delete from graph (iri(bif:JSO_SYS_GRAPH NIL)) { ?s virtrdf:version ?o }
where { graph `iri(bif:JSO_SYS_GRAPH NIL)` {?s virtrdf:version ?o}};
SPARQL_RELOAD_QM_GRAPH();
--#########




--#
--# Creation of IRIs classes.
--#########
sparql

prefix mbz: <http://musibrainz.org/schemas/mbz#>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix dc: <http://purl.org/dc/elements/1.1/>
prefix bio: <http://vocab.org/bio/0.1/#>
prefix rel: <http://vocab.org/relationship/#>
prefix mo: <http://purl.org/ontology/mo/>
prefix timeline: <http://purl.org/NET/c4dm/timeline.owl#>
prefix event: <http://purl.org/NET/c4dm/event.owl#>
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix sim: <http://purl.org/ontology/sim/>

create iri class mbz:artist_iri  "http://zitgist.com/music/artist/%U" (in gid varchar not null) option (bijection) .
create iri class mbz:artist_birth_event_iri  "http://zitgist.com/music/artist/birth/%U" (in gid varchar not null) option (bijection) .
create iri class mbz:artist_death_event_iri  "http://zitgist.com/music/artist/death/%U" (in gid varchar not null) option (bijection) .
create iri class mbz:sim_link_iri  "http://zitgist.com/music/artist/simlink/%U" (in gid varchar not null) option (bijection) .

#create iri class mbz:band_iri  "http://zitgist.com/music/band/%U" (in gid varchar not null) option (bijection) .
#create iri class mbz:band_birth_event_iri  "http://zitgist.com/music/band/birth/%U" (in gid varchar not null) option (bijection) .
#create iri class mbz:band_death_event_iri  "http://zitgist.com/music/band/death/%U" (in gid varchar not null) option (bijection) .

create iri class mbz:record_iri  "http://zitgist.com/music/record/%U" (in gid varchar not null) option (bijection) .
create iri class mbz:performance_iri  "http://zitgist.com/music/performance/%U" (in gid varchar not null) option (bijection) .
create iri class mbz:composition_iri  "http://zitgist.com/music/composition/%U" (in gid varchar not null) option (bijection) .
create iri class mbz:musicalwork_iri  "http://zitgist.com/music/musicalwork/%U" (in gid varchar not null) option (bijection) .
create iri class mbz:sound_iri  "http://zitgist.com/music/sound/%U" (in gid varchar not null) option (bijection) .
create iri class mbz:recording_iri  "http://zitgist.com/music/recording/%U" (in gid varchar not null) option (bijection) .
create iri class mbz:signal_iri  "http://zitgist.com/music/signal/%U" (in gid varchar not null) option (bijection) .

create iri class mbz:track_iri  "http://zitgist.com/music/track/%U" (in gid varchar not null) option (bijection) .

create iri class mbz:image_iri  "http://ec1.images-amazon.com/images/P/%U.01.MZZZZZZZ.jpg" (in image varchar not null) option (bijection) .

create iri class mbz:amazon_asin_iri  "http://amazon.com/exec/obidos/ASIN/%U/searchcom07-20" (in gid varchar not null) option (bijection) .


create literal class mbz:created using
   function ZITGIST.MO.RECORD_CREATION_DATE (in datestring varchar) returns varchar,
   function ZITGIST.MO.RECORD_CREATION_DATE_INVERSE (in datestring varchar) returns varchar .

create iri class mbz:official_iri using
   function ZITGIST.MO.RECORD_ATTRIBUTE_OFFICIAL (in attributes varchar) returns varchar
   option (returns 'http://purl.org/ontology/mo/official') .

create iri class mbz:promotion_iri using
   function ZITGIST.MO.RECORD_ATTRIBUTE_PROMOTION (in attributes varchar) returns varchar
   option (returns 'http://purl.org/ontology/mo/promotion') .

create iri class mbz:bootleg_iri using
   function ZITGIST.MO.RECORD_ATTRIBUTE_BOOTLEG (in attributes varchar) returns varchar
   option (returns 'http://purl.org/ontology/mo/bootleg') .

create iri class mbz:album_iri using
   function ZITGIST.MO.RECORD_ATTRIBUTE_ALBUM (in attributes varchar) returns varchar
   option (returns 'http://purl.org/ontology/mo/album') .

create iri class mbz:single_iri using
   function ZITGIST.MO.RECORD_ATTRIBUTE_SINGLE (in attributes varchar) returns varchar
   option (returns 'http://purl.org/ontology/mo/single') .

create iri class mbz:ep_iri using
   function ZITGIST.MO.RECORD_ATTRIBUTE_EP (in attributes varchar) returns varchar
   option (returns 'http://purl.org/ontology/mo/ep') .

create iri class mbz:compilation_iri using
   function ZITGIST.MO.RECORD_ATTRIBUTE_COMPILATION (in attributes varchar) returns varchar
   option (returns 'http://purl.org/ontology/mo/compilation') .

create iri class mbz:soundtrack_iri using
   function ZITGIST.MO.RECORD_ATTRIBUTE_SOUNDTRACK (in attributes varchar) returns varchar
   option (returns 'http://purl.org/ontology/mo/soundtrack') .

create iri class mbz:spokenword_iri using
   function ZITGIST.MO.RECORD_ATTRIBUTE_SPOKENWORD (in attributes varchar) returns varchar
   option (returns 'http://purl.org/ontology/mo/spokenword') .

create iri class mbz:interview_iri using
   function ZITGIST.MO.RECORD_ATTRIBUTE_INTERVIEW (in attributes varchar) returns varchar
   option (returns 'http://purl.org/ontology/mo/interview') .

create iri class mbz:audiobook_iri using
   function ZITGIST.MO.RECORD_ATTRIBUTE_AUDIOBOOK (in attributes varchar) returns varchar
   option (returns 'http://purl.org/ontology/mo/audiobook') .

create iri class mbz:live_iri using
   function ZITGIST.MO.RECORD_ATTRIBUTE_LIVE (in attributes varchar) returns varchar
   option (returns 'http://purl.org/ontology/mo/live') .

create iri class mbz:remix_iri using
   function ZITGIST.MO.RECORD_ATTRIBUTE_REMIX (in attributes varchar) returns varchar
   option (returns 'http://purl.org/ontology/mo/remix') .

create iri class mbz:duration_iri  "http://zitgist.com/music/track/duration/%U" (in gid varchar not null) .

create literal class mbz:duration using
   function ZITGIST.MO.TRACK_DURATION (in duration integer) returns varchar ,
   function ZITGIST.MO.TRACK_DURATION_INVERSE (in durationXSD varchar) returns integer .

create iri class mbz:geoname_country_iri  "http://www.geonames.org/countries/#%U" (in country varchar not null) .

create iri class mbz:url_iri  "%s" (in url varchar not null) .
create iri class mbz:mbz_release_url_iri  "http://musicbrainz.org/release/%s.html" (in mbz_gid varchar not null) .
create iri class mbz:mbz_track_url_iri  "http://musicbrainz.org/track/%s.html" (in mbz_gid varchar not null) .
create iri class mbz:mbz_artist_url_iri  "http://musicbrainz.org/artist/%s.html" (in mbz_gid varchar not null) .
;


--#
--# List of functions used to compute some IRI classes.
--# These function have been developed to handle some weird user cases of the Musicbrainz data model
--# (like the Attritube column of the album table, etc).
--#########


create function ZITGIST.MO.TRACK_DURATION_INVERSE(in durationXSD varchar)
{
   return null;
};

create function ZITGIST.MO.TRACK_DURATION(in duration integer)
{
   declare minutes, seconds, milliseconds integer;

   minutes := ((duration / 1000) / 60);

   if(minutes >= 1)
   {
       minutes := cast(minutes as integer);
   }
   else
   {
       minutes := 0;
   }

   seconds := (duration / 1000) - (minutes * 60);

   if(seconds >= 1)
   {
       seconds := cast(seconds as integer);
   }

   milliseconds := duration - (seconds * 1000) - (minutes * 60000);

   return sprintf('PT%dM%dS', minutes, seconds);
}
;


create function ZITGIST.MO.RECORD_CREATION_DATE(in datestring varchar)
{
   return sprintf('%sT00:00:00Z', datestring);
};

create function ZITGIST.MO.RECORD_CREATION_DATE_INVERSE(in datestring varchar)
{
   declare pos integer;
   pos := locate('T00:00:00Z', datestring) - 1;
   return substring(datestring, 1, pos);
};


create function ZITGIST.MO.RECORD_ATTRIBUTE(in attribute integer, in attributes varchar)
{
   declare attributes_array any;

   attributes_array := split_and_decode(ltrim(rtrim(attributes, '}'), '{'), 0, '\0\0,');

   foreach(int attr in attributes_array) do
   {
       attr := cast(attr as integer);
       if(attr = attribute)
       {
           if(attr = 100) return 'http://purl.org/ontology/mo/official';
           if(attr = 101) return 'http://purl.org/ontology/mo/promotion';
           if(attr = 102) return 'http://purl.org/ontology/mo/bootleg';
           if(attr = 1)   return 'http://purl.org/ontology/mo/album';
           if(attr = 2)   return 'http://purl.org/ontology/mo/single';
           if(attr = 3)   return 'http://purl.org/ontology/mo/ep';
           if(attr = 4)   return 'http://purl.org/ontology/mo/compilation';
           if(attr = 5)   return 'http://purl.org/ontology/mo/soundtrack';
           if(attr = 6)   return 'http://purl.org/ontology/mo/spokenword';
           if(attr = 7)   return 'http://purl.org/ontology/mo/interview';
           if(attr = 8)   return 'http://purl.org/ontology/mo/audiobook';
           if(attr = 9)   return 'http://purl.org/ontology/mo/live';
           if(attr = 10)  return 'http://purl.org/ontology/mo/remix';
       }
   }
   return null;
}
;

create function ZITGIST.MO.RECORD_ATTRIBUTE_OFFICIAL(in attributes varchar)
{    return ZITGIST.MO.RECORD_ATTRIBUTE(100, attributes); }
;
create function ZITGIST.MO.RECORD_ATTRIBUTE_PROMOTION(in attributes varchar)
{    return ZITGIST.MO.RECORD_ATTRIBUTE(101, attributes);}
;
create function ZITGIST.MO.RECORD_ATTRIBUTE_BOOTLEG(in attributes varchar)
{    return ZITGIST.MO.RECORD_ATTRIBUTE(102, attributes);}
;
create function ZITGIST.MO.RECORD_ATTRIBUTE_ALBUM(in attributes varchar)
{    return ZITGIST.MO.RECORD_ATTRIBUTE(1, attributes);}
;
create function ZITGIST.MO.RECORD_ATTRIBUTE_SINGLE(in attributes varchar)
{    return ZITGIST.MO.RECORD_ATTRIBUTE(2, attributes);}
;
create function ZITGIST.MO.RECORD_ATTRIBUTE_EP(in attributes varchar)
{    return ZITGIST.MO.RECORD_ATTRIBUTE(3, attributes);}
;
create function ZITGIST.MO.RECORD_ATTRIBUTE_COMPILATION(in attributes varchar)
{    return ZITGIST.MO.RECORD_ATTRIBUTE(4, attributes);}
;
create function ZITGIST.MO.RECORD_ATTRIBUTE_SOUNDTRACK(in attributes varchar)
{    return ZITGIST.MO.RECORD_ATTRIBUTE(5, attributes);}
;
create function ZITGIST.MO.RECORD_ATTRIBUTE_SPOKENWORD(in attributes varchar)
{    return ZITGIST.MO.RECORD_ATTRIBUTE(6, attributes);}
;
create function ZITGIST.MO.RECORD_ATTRIBUTE_INTERVIEW(in attributes varchar)
{    return ZITGIST.MO.RECORD_ATTRIBUTE(7, attributes);}
;
create function ZITGIST.MO.RECORD_ATTRIBUTE_AUDIOBOOK(in attributes varchar)
{    return ZITGIST.MO.RECORD_ATTRIBUTE(8, attributes);}
;
create function ZITGIST.MO.RECORD_ATTRIBUTE_LIVE(in attributes varchar)
{    return ZITGIST.MO.RECORD_ATTRIBUTE(9, attributes);}
;
create function ZITGIST.MO.RECORD_ATTRIBUTE_REMIX(in attributes varchar)
{    return ZITGIST.MO.RECORD_ATTRIBUTE(10, attributes);}
;

--#
--# Definition of the quad map patterns.
--# This what creates the RDF triples from the musicbrainz relational database schema.
--###########



sparql
prefix mbz: <http://musibrainz.org/schemas/mbz#>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix dc: <http://purl.org/dc/elements/1.1/>
prefix dcterms: <http://purl.org/dc/terms/>
prefix bio: <http://vocab.org/bio/0.1/#>
prefix rel: <http://vocab.org/relationship/#>
prefix mo: <http://purl.org/ontology/mo/>
prefix timeline: <http://purl.org/NET/c4dm/timeline.owl#>
prefix event: <http://purl.org/NET/c4dm/event.owl#>
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix sim: <http://purl.org/ontology/sim/>

create quad storage virtrdf:MBZROOT

#
# Defitions of the source tables from the mbz relational database and their joints.
#########

from ZITGIST.MO.track as track text literal name
from ZITGIST.MO.artist as track_artist
from ZITGIST.MO.puid as track_puid
from ZITGIST.MO.track as track_track
from ZITGIST.MO.url as track_url

from ZITGIST.MO.artist as track_artist_creator where (^{track.}^.artist = ^{track_artist_creator.}^.id)

from ZITGIST.MO.albumjoin as track_albumjoin where (^{track.}^.id = ^{track_albumjoin.}^.track)

from ZITGIST.MO.l_artist_track as l_artist_track2 where (^{track.}^.id = ^{l_artist_track2.}^.link1)
                                                     where (^{track_artist.}^.id = ^{l_artist_track2.}^.link0)


from ZITGIST.MO.puidjoin as puidjoin where (^{track.}^.id = ^{puidjoin.}^.track)
                                        where (^{puidjoin.}^.puid = ^{track_puid.}^.id)


from ZITGIST.MO.l_track_track as l_track_track where (^{track.}^.id = ^{l_track_track.}^.link0)
                                                  where (^{track_track.}^.id = ^{l_track_track.}^.link1)


from ZITGIST.MO.l_track_url as l_track_url where (^{track.}^.id = ^{l_track_url.}^.link0)
                                              where (^{track_url.}^.id = ^{l_track_url.}^.link1)



from ZITGIST.MO.album as album text literal name
from ZITGIST.MO.artist as album_artist
from ZITGIST.MO.album as album_album
from ZITGIST.MO.url as album_url
from ZITGIST.MO.country as album_release_country
from ZITGIST.MO.track as album_albumjoin_track

from ZITGIST.MO.artist as album_artist_creator where (^{album.}^.artist = ^{album_artist_creator.}^.id)

from ZITGIST.MO.album_amazon_asin as album_amazon_asin where (^{album.}^.id = ^{album_amazon_asin.}^.album)


from ZITGIST.MO.albumjoin as album_albumjoin where (^{album.}^.id = ^{album_albumjoin.}^.album)
                                                where (^{album_albumjoin.}^.track = ^{album_albumjoin_track.}^.id)


from ZITGIST.MO.l_album_artist as l_album_artist2 where (^{album.}^.id = ^{l_album_artist2.}^.link0)
                                                     where (^{album_artist.}^.id = ^{l_album_artist2.}^.link1)


from ZITGIST.MO.l_album_album as l_album_album where (^{album.}^.id = ^{l_album_album.}^.link0)
                                                  where (^{album_album.}^.id = ^{l_album_album.}^.link1)


from ZITGIST.MO.l_album_url as l_album_url where (^{album.}^.id = ^{l_album_url.}^.link0)
                                              where (^{album_url.}^.id = ^{l_album_url.}^.link1)


from ZITGIST.MO.release as album_release where (^{album.}^.id = ^{album_release.}^.album)
                                            where (^{album_release.}^.country = ^{album_release_country.}^.id)





from ZITGIST.MO.artist as sim_band
from ZITGIST.MO.artist as sim_artist
from ZITGIST.MO.url as band_url
from ZITGIST.MO.artist as band_member
from ZITGIST.MO.album as band_album
from ZITGIST.MO.track as band_track
from ZITGIST.MO.artist as band text literal name where (^{band.}^.type = 2)
#from ZITGIST.MO.artist as artist text literal name where (^{artist.}^.type <> 2)
from ZITGIST.MO.artist as artist text literal name where (__or (neq(^{artist.}^.type, 2), isnull (^{artist.}^.type)))
from ZITGIST.MO.artist as artist_untyped text literal name where (^{artist_untyped.}^.type <> 2)
                                                     where (^{artist.}^.gid = ^{artist_untyped.}^.gid)



from ZITGIST.MO.album as band_album_creatorOf where (^{band_album_creatorOf.}^.artist = ^{band.}^.id)
from ZITGIST.MO.track as band_track_creatorOf where (^{band_track_creatorOf.}^.artist = ^{band.}^.id)

from ZITGIST.MO.artistalias as bandalias text literal name where (^{band.}^.id = ^{bandalias.}^."ref")

from ZITGIST.MO.l_artist_artist as band_l_artist_artist where (^{band_member.}^.id = ^{band_l_artist_artist.}^.link0)
                                                           where (^{band.}^.id = ^{band_l_artist_artist.}^.link1)
                                                           where (^{band_l_artist_artist.}^.link_type = 2)


from ZITGIST.MO.artist_relation as band_relation
where (^{artist.}^.id = ^{band_relation.}^.artist)
where (^{band.}^.id = ^{band_relation.}^.artist)
where (^{sim_band.}^.id = ^{band_relation.}^."ref")

from ZITGIST.MO.artist_relation as artist_relation
where (^{artist.}^.id = ^{artist_relation.}^.artist)
where (^{band.}^.id = ^{artist_relation.}^.artist)
where (^{sim_artist.}^.id = ^{artist_relation.}^."ref")



from ZITGIST.MO.l_artist_url as l_artist_url3 where (^{band.}^.id = ^{l_artist_url3.}^.link0)
                                                 where (^{band_url.}^.id = ^{l_artist_url3.}^.link1)


from ZITGIST.MO.l_album_artist as l_album_artist3 where (^{band.}^.id = ^{l_album_artist3.}^.link1)
                                                     where (^{band_album.}^.id = ^{l_album_artist3.}^.link0)


from ZITGIST.MO.l_artist_track as l_artist_track3 where (^{band.}^.id = ^{l_artist_track3.}^.link0)
                                                     where (^{band_track.}^.id = ^{l_artist_track3.}^.link1)

from ZITGIST.MO.url as artist_url
from ZITGIST.MO.artist as artist_artist
from ZITGIST.MO.track as artist_track
from ZITGIST.MO.album as artist_album

from ZITGIST.MO.album as artist_album_creatorOf where (^{artist_album_creatorOf.}^.artist = ^{artist.}^.id)
from ZITGIST.MO.track as artist_track_creatorOf where (^{artist_track_creatorOf.}^.artist = ^{artist.}^.id)

from ZITGIST.MO.artistalias as artistalias text literal name where (^{artist.}^.id = ^{artistalias.}^."ref")
from ZITGIST.MO.l_artist_url as l_artist_url where (^{artist.}^.id = ^{l_artist_url.}^.link0)
                                                where (^{artist_url.}^.id = ^{l_artist_url.}^.link1)

from ZITGIST.MO.l_artist_artist as l_artist_artist where (^{artist.}^.id = ^{l_artist_artist.}^.link0)
                                                      where (^{artist_artist.}^.id = ^{l_artist_artist.}^.link1)

from ZITGIST.MO.l_artist_track as l_artist_track where (^{artist.}^.id = ^{l_artist_track.}^.link0)
                                                    where (^{artist_track.}^.id = ^{l_artist_track.}^.link1)
from ZITGIST.MO.l_album_artist as l_album_artist where (^{artist.}^.id = ^{l_album_artist.}^.link1)
                                                    where (^{artist_album.}^.id = ^{l_album_artist.}^.link0)

{
 create virtrdf:MBZ as graph iri ("http://musicbrainz.org/") option (exclusive)
   {

       # Track Composition Event
       mbz:composition_iri (track.gid)
           a mo:Composition as mbz:track_is_composition;
           dc:title track.name as mbz:title_of_track;
           mo:composer mbz:artist_iri (track_artist_creator.gid) as mbz:creator_composer_of_track;
           mo:composer mbz:artist_iri (track_artist.gid) where (^{l_artist_track2.}^.link_type = 14) option (using l_artist_track2) as mbz:composer14_of_track;
           mo:produced_work mbz:musicalwork_iri (track.gid) as mbz:track_produced_work.

       # Track Musical Work
       mbz:musicalwork_iri (track.gid)
           a mo:MusicalWork as mbz:track_is_mw;
           dc:title track.name as mbz:name_of_mw;

           mo:composed_in mbz:composition_iri(track.gid) as mbz:mw_is_composed_in_of;
           mo:performed_in mbz:performance_iri(track.gid) as mbz:mw_performed_in.

       # Track Performance Event
       mbz:performance_iri (track.gid)
           a mo:Performance;
           dc:title track.name;
           mo:performer mbz:artist_iri (track_artist_creator.gid);
           mo:performer mbz:artist_iri (track_artist.gid) where (^{l_artist_track2.}^.link_type = 2) option (using l_artist_track2);
           mo:conductor mbz:artist_iri (track_artist.gid) where (^{l_artist_track2.}^.link_type = 9) option (using l_artist_track2);

           mo:performance_of mbz:musicalwork_iri (track.gid);
           mo:produced_sound mbz:sound_iri (track.gid);

           mo:recorded_as mbz:signal_iri(track.gid).

       # Track Sound
       mbz:sound_iri (track.gid)
           a mo:Sound;
           dc:title track.name;
           mo:recorded_in mbz:recording_iri (track.gid).

       # Track Recording Event
       mbz:recording_iri (track.gid)
           a mo:Recording;
           dc:title track.name;
           mo:recording_of mbz:sound_iri (track.gid);
           mo:produced_signal mbz:signal_iri (track.gid).

       # Track Signal (Musical Expression)
       mbz:signal_iri (track.gid)
           a mo:Signal;
           dc:title track.name;

           mo:remixer mbz:artist_iri (track_artist.gid) where (^{l_artist_track2.}^.link_type = 11) option (using l_artist_track2);
           mo:sampler mbz:artist_iri (track_artist.gid) where (^{l_artist_track2.}^.link_type = 12) option (using l_artist_track2);
           mo:djmixed mbz:artist_iri (track_artist.gid) where (^{l_artist_track2.}^.link_type = 40) option (using l_artist_track2);

           mo:djmix_of mbz:track_iri (track_track.gid) where (^{l_track_track.}^.link_type = 13) option (using l_track_track);
           mo:remix_of mbz:track_iri (track_track.gid) where (^{l_track_track.}^.link_type = 6) option (using l_track_track);
           mo:remix_of mbz:track_iri (track_track.gid) where (^{l_track_track.}^.link_type = 11) option (using l_track_track);
           mo:mashup_of mbz:track_iri (track_track.gid) where (^{l_track_track.}^.link_type = 8) option (using l_track_track);
           mo:mashup_of mbz:track_iri (track_track.gid) where (^{l_track_track.}^.link_type = 4) option (using l_track_track);
           mo:remaster_of mbz:track_iri (track_track.gid) where (^{l_track_track.}^.link_type = 3) option (using l_track_track);
           mo:compilation_of mbz:track_iri (track_track.gid) where (^{l_track_track.}^.link_type = 10) option (using l_track_track);
           mo:compilation_of mbz:track_iri (track_track.gid) where (^{l_track_track.}^.link_type = 12) option (using l_track_track);
           mo:medley_of mbz:record_iri (track_track.gid) where (^{l_track_track.}^.link_type = 14) option (using l_track_track);

           mo:published_as mbz:track_iri (track.gid);
           mo:time mbz:duration_iri(track.gid);
           mo:puid track_puid.puid option (using puidjoin).

       # Track duration
       mbz:duration_iri(track.gid)
           a timeline:Interval;
           timeline:durationXSD mbz:duration(track.length).


       mbz:track_iri(track.gid)
           a mo:Track;
           dc:title track.name;

           mo:track_number track_albumjoin.sequence;


#           dc:creator mbz:artist_iri (track_artist_creator.gid);
#           dc:creator mbz:artist_iri (track_artist.gid) where (^{l_artist_track2.}^.link_type = 14) option (using l_artist_track2);

           foaf:maker mbz:artist_iri (track_artist_creator.gid);
           foaf:maker mbz:artist_iri (track_artist.gid) where (^{l_artist_track2.}^.link_type = 14) option (using l_artist_track2);
                       mo:compiler mbz:artist_iri (track_artist.gid) where (^{l_artist_track2.}^.link_type = 39) option (using l_artist_track2);
           mo:producer mbz:artist_iri (track_artist.gid) where (^{l_artist_track2.}^.link_type = 18) option (using l_artist_track2);
           mo:publisher mbz:artist_iri (track_artist.gid) where (^{l_artist_track2.}^.link_type = 35) option (using l_artist_track2);
           mo:engineer mbz:artist_iri (track_artist.gid) where (^{l_artist_track2.}^.link_type = 19) option (using l_artist_track2);


           mo:licence mbz:url_iri(track_url.url) where (^{l_track_url.}^.link_type = 21) option (using l_track_url);
           mo:paiddownload mbz:url_iri(track_url.url) where (^{l_track_url.}^.link_type = 16) option (using l_track_url);
           mo:freedownload mbz:url_iri(track_url.url) where (^{l_track_url.}^.link_type = 17) option (using l_track_url);
           mo:olga mbz:url_iri(track_url.url) where (^{l_track_url.}^.link_type = 19) option (using l_track_url);

           mo:musicbrainz mbz:mbz_track_url_iri(track.gid);

           mo:duration track.length.

       # Record Composition Event
       mbz:composition_iri (album.gid)
           a mo:Composition;
           dc:title album.name;

           mo:composer mbz:artist_iri (album_artist_creator.gid);
           mo:composer mbz:artist_iri (album_artist.gid) where (^{l_album_artist2.}^.link_type = 14) option (using l_album_artist2);

           mo:produced_work mbz:musicalwork_iri (album.gid).

       # Record Musical Work
       mbz:musicalwork_iri (album.gid)
           a mo:MusicalWork;
           dc:title album.name;

           mo:composed_in mbz:composition_iri(album.gid);
           mo:performed_in mbz:performance_iri(album.gid).


       # Record Performance Event
       mbz:performance_iri (album.gid)
           a mo:Performance;
           dc:title album.name;
           mo:performer mbz:artist_iri (album_artist_creator.gid);
           mo:performer mbz:artist_iri (album_artist.gid) where (^{l_album_artist2.}^.link_type = 2) option (using l_album_artist2);
           mo:conductor mbz:artist_iri (album_artist.gid) where (^{l_album_artist2.}^.link_type = 9) option (using l_album_artist2);

           mo:performance_of mbz:musicalwork_iri (album.gid);
           mo:produced_sound mbz:sound_iri (album.gid);

           mo:recorded_as mbz:record_iri(album.gid).


       # Record Sound
       mbz:sound_iri (album.gid)
           a mo:Sound;
           dc:title album.name;

           mo:recorded_in mbz:recording_iri (album.gid).

       # Record Recording Event
       mbz:recording_iri (album.gid)
           a mo:Recording;
           dc:title album.name;

           mo:recording_of mbz:sound_iri (album.gid);
           mo:produced_signal mbz:signal_iri (album.gid).

       # Record Signal (Musical Expression)
       mbz:signal_iri (album.gid)
           a mo:Signal;
           dc:title album.name;

           mo:djmix_of mbz:record_iri (album_album.gid) where (^{l_album_album.}^.link_type = 9) option (using l_album_album);
           mo:remix_of mbz:record_iri (album_album.gid) where (^{l_album_album.}^.link_type = 7) option (using l_album_album);
           mo:remix_of mbz:record_iri (album_album.gid) where (^{l_album_album.}^.link_type = 4) option (using l_album_album);
           mo:mashup_of mbz:record_iri (album_album.gid) where (^{l_album_album.}^.link_type = 5) option (using l_album_album);
           mo:remaster_of mbz:record_iri (album_album.gid) where (^{l_album_album.}^.link_type = 3) option (using l_album_album);
           mo:tribute_to mbz:artist_iri (album_artist.gid) where (^{l_album_artist2.}^.link_type = 44) option (using l_album_artist2);

           mo:remixer mbz:artist_iri (album_artist.gid) where (^{l_album_artist2.}^.link_type = 11) option (using l_album_artist2);
           mo:djmixed mbz:artist_iri (album_artist.gid) where (^{l_album_artist2.}^.link_type = 38) option (using l_album_artist2);
           mo:sampler mbz:artist_iri (album_artist.gid) where (^{l_album_artist2.}^.link_type = 12) option (using l_album_artist2);

           mo:published_as mbz:record_iri (album.gid).


       # Record (Musical Manifestation)
       mbz:record_iri (album.gid)
           a mo:Record;
           dc:title album.name;

           dc:date mbz:created(album_release.releasedate);
           mo:image mbz:image_iri(album_amazon_asin.asin);

           #Empty for now.
           mo:compilation_of mbz:record_iri (album_album.gid) where (^{l_album_album.}^.link_type = 8) option (using l_album_album);
           mo:release_status mbz:official_iri(album.attributes);
           mo:release_status mbz:promotion_iri(album.attributes);
           mo:release_status mbz:bootleg_iri(album.attributes);

           mo:release_type mbz:album_iri(album.attributes);
           mo:release_type mbz:single_iri(album.attributes);
           mo:release_type mbz:ep_iri(album.attributes);
           mo:release_type mbz:compilation_iri(album.attributes);
           mo:release_type mbz:soundtrack_iri(album.attributes);
           mo:release_type mbz:spokenword_iri(album.attributes);
           mo:release_type mbz:interview_iri(album.attributes);
           mo:release_type mbz:audiobook_iri(album.attributes);
           mo:release_type mbz:live_iri(album.attributes);
           mo:release_type mbz:remix_iri(album.attributes);


#           dc:creator mbz:artist_iri (album_artist_creator.gid);
#           dc:creator mbz:artist_iri (album_artist.gid) where (^{l_album_artist2.}^.link_type = 14) option (using l_album_artist2);

           foaf:maker mbz:artist_iri (album_artist_creator.gid);
           foaf:maker mbz:artist_iri (album_artist.gid) where (^{l_album_artist2.}^.link_type = 14) option (using l_album_artist2);

           mo:compiler mbz:artist_iri (album_artist.gid) where (^{l_album_artist2.}^.link_type = 41) option (using l_album_artist2);
           mo:producer mbz:artist_iri (album_artist.gid) where (^{l_album_artist2.}^.link_type = 18) option (using l_album_artist2);
           mo:publisher mbz:artist_iri (album_artist.gid) where (^{l_album_artist2.}^.link_type = 35) option (using l_album_artist2);
           mo:engineer mbz:artist_iri (album_artist.gid) where (^{l_album_artist2.}^.link_type = 19) option (using l_album_artist2);


           mo:musicbrainz mbz:mbz_release_url_iri(album.gid);

           mo:musicmoz mbz:url_iri(album_url.url) where (^{l_album_url.}^.link_type = 25) option (using l_album_url);
           mo:discogs mbz:url_iri(album_url.url) where (^{l_album_url.}^.link_type = 24) option (using l_album_url);
           mo:wikipedia mbz:url_iri(album_url.url) where (^{l_album_url.}^.link_type = 23) option (using l_album_url);
           mo:discography mbz:url_iri(album_url.url) where (^{l_album_url.}^.link_type = 1) option (using l_album_url);
           mo:freedownload mbz:url_iri(album_url.url) where (^{l_album_url.}^.link_type = 21) option (using l_album_url);
           mo:discography mbz:url_iri(album_url.url) where (^{l_album_url.}^.link_type = 16) option (using l_album_url);
           mo:mailorder mbz:url_iri(album_url.url) where (^{l_album_url.}^.link_type = 19) option (using l_album_url);
           mo:imdb mbz:url_iri(album_url.url) where (^{l_album_url.}^.link_type = 27) option (using l_album_url);
           mo:paiddownload mbz:url_iri(album_url.url) where (^{l_album_url.}^.link_type = 20) option (using l_album_url);
           mo:licence mbz:url_iri(album_url.url) where (^{l_album_url.}^.link_type = 32) option (using l_album_url);
           mo:review mbz:url_iri(album_url.url) where (^{l_album_url.}^.link_type = 17) option (using l_album_url);


           mo:amazon_asin mbz:amazon_asin_iri(album_amazon_asin.asin);

           mo:track mbz:track_iri (album_albumjoin_track.gid) option (using album_albumjoin).

      # Music Group (Band)
#       mbz:band_iri(band.gid)
       mbz:artist_iri(band.gid)
           a mo:MusicArtist;
           a mo:MusicGroup;
           a foaf:Group;
           foaf:name band.name;
           foaf:nick bandalias.name;

#           bio:event mbz:band_birth_event_iri(band.gid);
#           bio:event mbz:band_death_event_iri(band.gid);
           bio:event mbz:artist_birth_event_iri(band.gid);
           bio:event mbz:artist_death_event_iri(band.gid);

#           mo:similar_to mbz:band_iri(sim_band.gid) option (using band_relation);
           mo:similar_to mbz:artist_iri(sim_band.gid) option (using band_relation);
           mo:similar_to mbz:artist_iri(sim_artist.gid) option (using artist_relation);
#            sim:link mbz:sim_link_iri(sim_band.gid)  option (using band_relation);
#            sim:link mbz:sim_link_iri(sim_artist.gid)  option (using artist_relation);

           foaf:member mbz:artist_iri(band_member.gid) option (using band_l_artist_artist);

           # l_artist_url
           mo:myspace mbz:url_iri(band_url.url) where (^{l_artist_url3.}^.link_type = 19) option (using l_artist_url3);
           mo:musicmoz mbz:url_iri(band_url.url) where (^{l_artist_url3.}^.link_type = 12) option (using l_artist_url3);
           mo:discogs mbz:url_iri(band_url.url) where (^{l_artist_url3.}^.link_type = 11) option (using l_artist_url3);
           mo:wikipedia mbz:url_iri(band_url.url) where (^{l_artist_url3.}^.link_type = 10) option (using l_artist_url3);
           mo:discography mbz:url_iri(band_url.url) where (^{l_artist_url3.}^.link_type = 1) option (using l_artist_url3);
           mo:freedownload mbz:url_iri(band_url.url) where (^{l_artist_url3.}^.link_type = 8) option (using l_artist_url3);
           mo:fanpage mbz:url_iri(band_url.url) where (^{l_artist_url3.}^.link_type = 3) option (using l_artist_url3);
           mo:biography mbz:url_iri(band_url.url) where (^{l_artist_url3.}^.link_type = 4) option (using l_artist_url3);
           mo:discography mbz:url_iri(band_url.url) where (^{l_artist_url3.}^.link_type = 5) option (using l_artist_url3);
           mo:mailorder mbz:url_iri(band_url.url) where (^{l_artist_url3.}^.link_type = 15) option (using l_artist_url3);
           mo:imdb mbz:url_iri(band_url.url) where (^{l_artist_url3.}^.link_type = 17) option (using l_artist_url3);
           mo:paiddownload mbz:url_iri(band_url.url) where (^{l_artist_url3.}^.link_type = 7) option (using l_artist_url3);
           foaf:depiction mbz:url_iri(band_url.url) where (^{l_artist_url3.}^.link_type = 14) option (using l_artist_url3);
           foaf:homepage mbz:url_iri(band_url.url) where (^{l_artist_url3.}^.link_type = 2) option (using l_artist_url3);

           mo:musicbrainz mbz:mbz_artist_url_iri(band.gid);


           # l_album_artist
#           mo:composed mbz:composition_iri (band_album.gid) where (^{l_album_artist3.}^.link_type = 14) option (using l_album_artist3);
           mo:performed mbz:performance_iri (band_album.gid) where (^{l_album_artist3.}^.link_type = 14) option (using l_album_artist3);
           mo:performed mbz:performance_iri (band_album.gid) where (^{l_album_artist3.}^.link_type = 2) option (using l_album_artist3);
           mo:conducted mbz:performance_iri (band_album.gid) where (^{l_album_artist3.}^.link_type = 9) option (using l_album_artist3);
           mo:compiled mbz:record_iri (band_album.gid) where (^{l_album_artist3.}^.link_type = 41) option (using l_album_artist3);
           mo:djmixed mbz:record_iri (band_album.gid) where (^{l_album_artist3.}^.link_type = 38) option (using l_album_artist3);
           mo:remixed mbz:record_iri (band_album.gid) where (^{l_album_artist3.}^.link_type = 11) option (using l_album_artist3);
           mo:sampled mbz:record_iri (band_album.gid) where (^{l_album_artist3.}^.link_type = 12) option (using l_album_artist3);
           mo:produced mbz:record_iri (band_album.gid) where (^{l_album_artist3.}^.link_type = 18) option (using l_album_artist3);
           mo:published mbz:record_iri (band_album.gid) where (^{l_album_artist3.}^.link_type = 35) option (using l_album_artist3);
           mo:engineered mbz:record_iri (band_album.gid) where (^{l_album_artist3.}^.link_type = 19) option (using l_album_artist3);

#    #      mo:creatorOfRecord mbz:record_iri(band_album_creatorOf.gid);
           foaf:made mbz:record_iri(band_album_creatorOf.gid);

           # l_artist_track
#           mo:composed mbz:composition_iri (band_track.gid) where (^{l_artist_track3.}^.link_type = 14) option (using l_artist_track3);
           mo:performed mbz:performance_iri (band_track.gid) where (^{l_artist_track3.}^.link_type = 14) option (using l_artist_track3);
           mo:performed mbz:performance_iri (band_track.gid) where (^{l_artist_track3.}^.link_type = 2) option (using l_artist_track3);
           mo:conducted mbz:performance_iri (band_track.gid) where (^{l_artist_track3.}^.link_type = 9) option (using l_artist_track3);
           mo:compiled mbz:record_iri (band_track.gid) where (^{l_artist_track3.}^.link_type = 39) option (using l_artist_track3);
           mo:djmixed mbz:track_iri (band_track.gid) where (^{l_artist_track3.}^.link_type = 40) option (using l_artist_track3);
           mo:remixed mbz:track_iri (band_track.gid) where (^{l_artist_track3.}^.link_type = 11) option (using l_artist_track3);
           mo:sampled mbz:track_iri (band_track.gid) where (^{l_artist_track3.}^.link_type = 12) option (using l_artist_track3);
           mo:produced mbz:track_iri (band_track.gid) where (^{l_artist_track3.}^.link_type = 18) option (using l_artist_track3);
           mo:published mbz:track_iri (band_track.gid) where (^{l_artist_track3.}^.link_type = 35) option (using l_artist_track3);
           mo:engineered mbz:track_iri (band_track.gid) where (^{l_artist_track3.}^.link_type = 19) option (using l_artist_track3).

#    #      mo:creatorOfTrack mbz:track_iri(band_track_creatorOf.gid).




       # Music Group (Band)'s Birth Event
#       mbz:band_birth_event_iri(band.gid)
       mbz:artist_birth_event_iri(band.gid)
           a bio:Birth;
           bio:date band.begindate.

       # Music Group (Band)'s Death Event
#       mbz:band_death_event_iri(band.gid)
       mbz:artist_death_event_iri(band.gid)
           a bio:Death;
           bio:date band.enddate.

       # Similarity link
       #mbz:sim_link_iri(sim_band.gid)
       #    sim:relation mo:similar_to;
       #    sim:level band_relation.weight;
       #    sim:to sim_band.gid.


       # Music Artist
       mbz:artist_iri (artist.gid)

           # artist
           a mo:MusicArtist;
           a mo:SoloMusicArtist where (^{artist_untyped.}^.gid is not null) option (using artist_untyped);
           a foaf:Person where (^{artist_untyped.}^.gid is not null) option (using artist_untyped);
           foaf:name artist.name;
           foaf:nick artistalias.name;
           bio:event mbz:artist_birth_event_iri(artist.gid);
           bio:event mbz:artist_death_event_iri(artist.gid);

           mo:member_of mbz:artist_iri(artist_artist.gid) where (^{l_artist_artist.}^.link_type = 2) option (using l_artist_artist);

           # l_artist_artist
           rel:siblingOf mbz:artist_iri(artist_artist.gid) where (^{l_artist_artist.}^.link_type = 7) option (using l_artist_artist);
           rel:friendOf mbz:artist_iri(artist_artist.gid) where (^{l_artist_artist.}^.link_type = 5) option (using l_artist_artist);
           rel:parentOf mbz:artist_iri(artist_artist.gid) where (^{l_artist_artist.}^.link_type = 6) option (using l_artist_artist);
           rel:collaborated_with mbz:artist_iri(artist_artist.gid) where (^{l_artist_artist.}^.link_type = 11) option (using l_artist_artist);
           rel:engagedTo mbz:artist_iri(artist_artist.gid) where (^{l_artist_artist.}^.link_type = 9) option (using l_artist_artist);
           rel:spouseOf mbz:artist_iri(artist_artist.gid) where (^{l_artist_artist.}^.link_type = 8) option (using l_artist_artist);
           mo:supporting_musician mbz:artist_iri(artist_artist.gid) where (^{l_artist_artist.}^.link_type = 13) option (using l_artist_artist);
           mo:supporting_musician mbz:artist_iri(artist_artist.gid) where (^{l_artist_artist.}^.link_type = 14) option (using l_artist_artist);
           mo:supporting_musician mbz:artist_iri(artist_artist.gid) where (^{l_artist_artist.}^.link_type = 15) option (using l_artist_artist);

           mo:similar_to mbz:artist_iri(sim_artist.gid) option (using artist_relation);
#           mo:similar_to mbz:band_iri(sim_band.gid) option (using band_relation);
           mo:similar_to mbz:artist_iri(sim_band.gid) option (using band_relation);

#            sim:link mbz:sim_link_iri(sim_band.gid)  option (using band_relation);
#            sim:link mbz:sim_link_iri(sim_artist.gid)  option (using artist_relation);


           # l_artist_url
           mo:myspace mbz:url_iri(artist_url.url) where (^{l_artist_url.}^.link_type = 19) option (using l_artist_url);
           mo:musicmoz mbz:url_iri(artist_url.url) where (^{l_artist_url.}^.link_type = 12) option (using l_artist_url);
           mo:discogs mbz:url_iri(artist_url.url) where (^{l_artist_url.}^.link_type = 11) option (using l_artist_url);
           mo:wikipedia mbz:url_iri(artist_url.url) where (^{l_artist_url.}^.link_type = 10) option (using l_artist_url);
           mo:discography mbz:url_iri(artist_url.url) where (^{l_artist_url.}^.link_type = 1) option (using l_artist_url);
           mo:freedownload mbz:url_iri(artist_url.url) where (^{l_artist_url.}^.link_type = 8) option (using l_artist_url);
           mo:fanpage mbz:url_iri(artist_url.url) where (^{l_artist_url.}^.link_type = 3) option (using l_artist_url);
           mo:biography mbz:url_iri(artist_url.url) where (^{l_artist_url.}^.link_type = 4) option (using l_artist_url);
           mo:discography mbz:url_iri(artist_url.url) where (^{l_artist_url.}^.link_type = 5) option (using l_artist_url);
           mo:mailorder mbz:url_iri(artist_url.url) where (^{l_artist_url.}^.link_type = 15) option (using l_artist_url);
           mo:imdb mbz:url_iri(artist_url.url) where (^{l_artist_url.}^.link_type = 17) option (using l_artist_url);
           mo:paiddownload mbz:url_iri(artist_url.url) where (^{l_artist_url.}^.link_type = 7) option (using l_artist_url);
           foaf:depiction mbz:url_iri(artist_url.url) where (^{l_artist_url.}^.link_type = 14) option (using l_artist_url);
           foaf:homepage mbz:url_iri(artist_url.url) where (^{l_artist_url.}^.link_type = 2) option (using l_artist_url);

           mo:musicbrainz mbz:mbz_artist_url_iri(artist.gid);


           # l_album_artist
#            mo:composed mbz:composition_iri (artist_album.gid) where (^{l_album_artist.}^.link_type = 14) option (using l_album_artist);
           mo:performed mbz:performance_iri (artist_album.gid) where (^{l_album_artist.}^.link_type = 14) option (using l_album_artist);
           mo:performed mbz:performance_iri (artist_album.gid) where (^{l_album_artist.}^.link_type = 2) option (using l_album_artist);
           mo:conducted mbz:performance_iri (artist_album.gid) where (^{l_album_artist.}^.link_type = 9) option (using l_album_artist);
           mo:compiled mbz:record_iri (artist_album.gid) where (^{l_album_artist.}^.link_type = 41) option (using l_album_artist);
           mo:djmixed mbz:record_iri (artist_album.gid) where (^{l_album_artist.}^.link_type = 38) option (using l_album_artist);
           mo:remixed mbz:record_iri (artist_album.gid) where (^{l_album_artist.}^.link_type = 11) option (using l_album_artist);
           mo:sampled mbz:record_iri (artist_album.gid) where (^{l_album_artist.}^.link_type = 12) option (using l_album_artist);
           mo:produced mbz:record_iri (artist_album.gid) where (^{l_album_artist.}^.link_type = 18) option (using l_album_artist);
           mo:published mbz:record_iri (artist_album.gid) where (^{l_album_artist.}^.link_type = 35) option (using l_album_artist);
           mo:engineered mbz:record_iri (artist_album.gid) where (^{l_album_artist.}^.link_type = 19) option (using l_album_artist);

    #      mo:creatorOfRecord mbz:record_iri(artist_album_creatorOf.gid);
           foaf:made mbz:record_iri(artist_album_creatorOf.gid);


           # l_artist_track
#            mo:composed mbz:composition_iri (artist_track.gid) where (^{l_artist_track.}^.link_type = 14) option (using l_artist_track);
           mo:performed mbz:performance_iri (artist_track.gid) where (^{l_artist_track.}^.link_type = 14) option (using l_artist_track);
           mo:performed mbz:performance_iri (artist_track.gid) where (^{l_artist_track.}^.link_type = 2) option (using l_artist_track);
           mo:conducted mbz:performance_iri (artist_track.gid) where (^{l_artist_track.}^.link_type = 9) option (using l_artist_track);
           mo:compiled mbz:track_iri (artist_track.gid) where (^{l_artist_track.}^.link_type = 39) option (using l_artist_track);
           mo:djmixed mbz:track_iri (artist_track.gid) where (^{l_artist_track.}^.link_type = 40) option (using l_artist_track);
           mo:remixed mbz:track_iri (artist_track.gid) where (^{l_artist_track.}^.link_type = 11) option (using l_artist_track);
           mo:sampled mbz:track_iri (artist_track.gid) where (^{l_artist_track.}^.link_type = 12) option (using l_artist_track);
           mo:produced mbz:track_iri (artist_track.gid) where (^{l_artist_track.}^.link_type = 18) option (using l_artist_track);
           mo:published mbz:track_iri (artist_track.gid) where (^{l_artist_track.}^.link_type = 35) option (using l_artist_track);
           mo:engineered mbz:track_iri (artist_track.gid) where (^{l_artist_track.}^.link_type = 19) option (using l_artist_track).

    #       mo:creatorOfTrack mbz:track_iri(artist_track_creatorOf.gid).


       # Music Artist''s Birth Event
       mbz:artist_birth_event_iri(artist.gid)
           a bio:Birth;
           bio:date artist.begindate.

       # Music Artist''s Death Event
       mbz:artist_death_event_iri(artist.gid)
           a bio:Death;
           bio:date artist.enddate.

       # Similarity link
       #mbz:sim_link_iri(sim_artist.gid)
       #    sim:relation mo:similar_to;
       #    sim:level artist_relation.weight;
       #    sim:to sim_artist.gid.

       }
 }
;


grant execute on ZITGIST.MO.RECORD_CREATION_DATE to "SPARQL";
grant execute on ZITGIST.MO.RECORD_CREATION_DATE_INVERSE to "SPARQL";
grant execute on ZITGIST.MO.RECORD_ATTRIBUTE_OFFICIAL to "SPARQL";
grant execute on ZITGIST.MO.RECORD_ATTRIBUTE_PROMOTION to "SPARQL";
grant execute on ZITGIST.MO.RECORD_ATTRIBUTE_BOOTLEG to "SPARQL";
grant execute on ZITGIST.MO.RECORD_ATTRIBUTE_ALBUM to "SPARQL";
grant execute on ZITGIST.MO.RECORD_ATTRIBUTE_SINGLE to "SPARQL";
grant execute on ZITGIST.MO.RECORD_ATTRIBUTE_EP to "SPARQL";
grant execute on ZITGIST.MO.RECORD_ATTRIBUTE_COMPILATION to "SPARQL";
grant execute on ZITGIST.MO.RECORD_ATTRIBUTE_SOUNDTRACK to "SPARQL";
grant execute on ZITGIST.MO.RECORD_ATTRIBUTE_SPOKENWORD to "SPARQL";
grant execute on ZITGIST.MO.RECORD_ATTRIBUTE_INTERVIEW to "SPARQL";
grant execute on ZITGIST.MO.RECORD_ATTRIBUTE_AUDIOBOOK to "SPARQL";
grant execute on ZITGIST.MO.RECORD_ATTRIBUTE_LIVE to "SPARQL";
grant execute on ZITGIST.MO.RECORD_ATTRIBUTE_REMIX to "SPARQL";
grant execute on ZITGIST.MO.TRACK_DURATION to "SPARQL";
grant execute on ZITGIST.MO.TRACK_DURATION_INVERSE to "SPARQL";
grant select on ZITGIST.MO.album to "SPARQL";
grant select on ZITGIST.MO.album_amazon_asin to "SPARQL";
grant select on ZITGIST.MO.album_name_WORDS to "SPARQL";
grant select on ZITGIST.MO.albumjoin to "SPARQL";
grant select on ZITGIST.MO.albummeta to "SPARQL";
grant select on ZITGIST.MO.artist to "SPARQL";
grant select on ZITGIST.MO.artist_name_WORDS to "SPARQL";
grant select on ZITGIST.MO.artist_relation to "SPARQL";
grant select on ZITGIST.MO.artistalias to "SPARQL";
grant select on ZITGIST.MO.artistalias_name_WORDS to "SPARQL";
grant select on ZITGIST.MO.country to "SPARQL";
grant select on ZITGIST.MO.l_album_album to "SPARQL";
grant select on ZITGIST.MO.l_album_artist to "SPARQL";
grant select on ZITGIST.MO.l_album_url to "SPARQL";
grant select on ZITGIST.MO.l_artist_artist to "SPARQL";
grant select on ZITGIST.MO.l_artist_track to "SPARQL";
grant select on ZITGIST.MO.l_artist_url to "SPARQL";
grant select on ZITGIST.MO.l_track_track to "SPARQL";
grant select on ZITGIST.MO.l_track_url to "SPARQL";
grant select on ZITGIST.MO."language" to "SPARQL";
grant select on ZITGIST.MO.puid to "SPARQL";
grant select on ZITGIST.MO.puidjoin to "SPARQL";
grant select on ZITGIST.MO.release to "SPARQL";
grant select on ZITGIST.MO.track to "SPARQL";
grant select on ZITGIST.MO.track_name_WORDS to "SPARQL";
grant select on ZITGIST.MO.url to "SPARQL";
