<xsl:transform 
    xmlns:xsl  ="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:rdf  ="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:owl  ="http://www.w3.org/2002/07/owl#"
    xmlns:rdfs ="http://www.w3.org/2000/02/rdfschema#"
    xmlns:mo   ="http://purl.org/ontology/mo/"
    xmlns:dc   ="http://purl.org/dc/elements/1.1/"
    xmlns:event="http://purl.org/NET/c4dm/event.owl#"
    xmlns:foaf ="http://xmlns.com/foaf/0.1/"
    xmlns:geo  ="http://www.geonames.org/ontology#"
    xmlns:wgs  ="http://www.w3.org/2003/01/geo/wgs84_pos#"
    xmlns:tags ="http://www.holygoat.co.uk/owl/redwood/0.1/tags/"
    xmlns ="http://dbtune.org/echonest/" 
    >

<xsl:output method="xml" indent="yes" encoding="utf-8"/>

<xsl:template match="JamendoData">
<rdf:RDF>

<xsl:for-each select="Artists/artist">
<mo:MusicArtist rdf:about="http://dbtune.org/jamendo/artist/{id/text()}" foaf:name="{name/text()}">
    <xsl:if test="string(image)">
    <foaf:img rdf:resource="{image/text()}"/>
    </xsl:if>
    <xsl:if test="string(mbgid)">
    <owl:sameAs rdf:resource="http://dbtune.org/musicbrainz/resource/artist/{mbgid/text()}"/>
    <owl:sameAs rdf:resource="http://www.bbc.co.uk/music/artists/{mbgid/text()}#artist"/>
    <mo:musicbrainz rdf:resource="http://musicbrainz.org/artist/{mbgid/text()}"/>
    </xsl:if>
    <foaf:homepage rdf:resource="{url/text()}"/>
    <xsl:if test="location">
    <foaf:based_near>
      <geo:Feature geo:name="{location/city/text()}" wgs:lat="{location/latitude/text()}" wgs:long="{location/longitude/text()}">
        <xsl:if test="location/country">
        <geo:inCountry>
            <geo:Country rdf:about="http://www.geonames.org/countries/#{location/country/text()}" rdfs:label="{location/country/text()}" />
        </geo:inCountry>
        </xsl:if>
        <xsl:if test="location/state">
        <geo:inState>
            <geo:State rdfs:label="{location/state/text()}"/>
        </geo:inState>
        </xsl:if>
      </geo:Feature>
    </foaf:based_near>
    </xsl:if>
<xsl:for-each select="Albums/album">
<foaf:made>
<mo:Record rdf:about="http://dbtune.org/jamendo/record/{id/text()}" dc:title="{name/text()}" dc:date="{releasedata/text()}">
    <foaf:homepage rdf:resource="{url/text()}" />
    <xsl:if test="string(mbgid)">
    <owl:sameAs rdf:resource="http://dbtune.org/musicbrainz/resource/record/{mbgid/text()}"/>
    <mo:musicbrainz rdf:resource="http://musicbrainz.org/release/{mbgid/text()}"/>
    <mo:available_as rdf:resource="http://api.jamendo.com/get2/bittorrent/file/plain/?album_id={id/text()}&amp;type=archive&amp;class=mp32" />
    <mo:available_as rdf:resource="http://api.jamendo.com/get2/bittorrent/file/plain/?album_id={id/text()}&amp;type=archive&amp;class=ogg3" />
    </xsl:if>
    <!-- <mo:license rdf:resource="{license_artwork/text()}"/> -->
    <xsl:for-each select="Tracks/track">
    <mo:track>
        <mo:Track rdf:about="http://dbtune.org/jamendo/track/{id/text()}" dc:title="name/text()" mo:track_number="{numalbum/text()}">
            <xsl:if test="string(mbgid)">
            <owl:sameAs rdf:resource="http://dbtune.org/musicbrainz/resource/track/{mbgid/text()}"/>
            <mo:musicbrainz rdf:resource="http://musicbrainz.org/track/{mbgid/text()}"/>
            </xsl:if>
            <mo:license rdf:resource="{license/text()}"/>
            <xsl:for-each select="Tags/tag">
            <tags:taggedWithTag>
                <tags:Tag rdf:about="http://dbtune.org/jamendo/tag/{idstr/text()}" tags:tagName="{idstr/text()}" dc:title="{idstr/text()}" />
            </tags:taggedWithTag>
            </xsl:for-each>
            <mo:available_as rdf:resource="http://api.jamendo.com/get2/stream/track/redirect/?id={id/text()}&amp;streamencoding=mp31" />
            <mo:available_as rdf:resource="http://api.jamendo.com/get2/stream/track/redirect/?id={id/text()}&amp;streamencoding=ogg3" />
        </mo:Track>
    </mo:track>
    </xsl:for-each>
</mo:Record>
</foaf:made>
</xsl:for-each>
</mo:MusicArtist>
</xsl:for-each>
</rdf:RDF>
</xsl:template>

</xsl:transform>
