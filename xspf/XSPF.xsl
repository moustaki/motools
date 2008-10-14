<xsl:transform 
    xmlns:xsl  ="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:rdf  ="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs ="http://www.w3.org/2000/02/rdfschema#"
    xmlns:play ="http://xspf.org/ns/0/" 
    xmlns:mo   ="http://purl.org/ontology/mo/"
    xmlns ="http://xspf.org/ns/0/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:dct="http://purl.org/dc/terms/"
    xmlns:foaf="http://xmlns.com/foaf/0.1/"
    xmlns:cc="http://web.resource.org/cc/"
    xmlns:owl="http://www.w3.org/2002/07/owl#"
    xmlns:fn="http://www.w3.org/2005/xpath-functions"
    >

<xsl:output method="xml" indent="yes" encoding="utf-8"/>

<div xmlns="http://www.w3.org/1999/xhtml">
  <h1>Transform XSPF to MusicOntology RDF</h1>
  <p>This document specifies how to transform a valid <a href="http://xspf.org/">XSPF</a> document into <a href="http://musicontology.com">MusicOntology</a> RDF/XML.</p>
  <p>It is designed for use by agents who understand <a href="http://www.w3.org/TR/grddl/">GRDDL</a>, and acts as the XSPF <a href="http://www.w3.org/TR/grddl/#ns-bind">NamespaceTransformation</a>.</p>
  <p>Based on <a href="http://libby.asemantics.com/2005/01/XSPF/">original work</a> by <a href="mailto:libby@asemantics.com">Libby Miller</a></p>
  <p>Copyright <a href="http://moustaki.org/">Yves Raimond</a> &amp; <a href="http://clockwerx.blogspot.com/">Daniel O'Connor</a></p>

  <h2>Example</h2>
The below XSPF playlist
<pre>
&lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;playlist version="1" xmlns="http://xspf.org/ns/0/"&gt;

  &lt;title&gt;My playlist&lt;/title&gt;

  &lt;creator&gt;Jane Doe&lt;/creator&gt;
  &lt;annotation&gt;My favorite songs&lt;/annotation&gt;
  &lt;info&gt;http://example.com/myplaylists&lt;/info&gt;
  &lt;location&gt;http://example.com/myplaylists/myplaylist&lt;/location&gt;
  &lt;identifier&gt;magnet:?xt=urn:sha1:YNCKHTQCWBTRNJIV4WNAE52SJUQCZO5C&lt;/identifier&gt;
  &lt;image&gt;http://example.com/img/mypicture&lt;/image&gt;
  &lt;date&gt;2005-01-08T17:10:47-05:00&lt;/date&gt;
  &lt;license&gt;http://creativecommons.org/licenses/by/1.0/&lt;/license&gt;
  &lt;attribution&gt;
    &lt;identifier&gt;http://bar.com/secondderived.xspf&lt;/identifier&gt;
    &lt;location&gt;http://foo.com/original.xspf&lt;/location&gt;
  &lt;/attribution&gt;
  &lt;link rel="http://foaf.example.org/namespace/version1"&gt;http://socialnetwork.example.org/foaf/mary.rdfs&lt;/link&gt;
  &lt;meta rel="http://example.org/key"&gt;value&lt;/meta&gt;
  &lt;extension application="http://example.com"&gt;
    &lt;clip start="25000" end="34500"/&gt;
  &lt;/extension&gt;

&lt;trackList&gt;

    &lt;track&gt;

      &lt;location&gt;http://example.com/my.mp3&lt;/location&gt;
      &lt;identifier&gt;magnet:?xt=urn:sha1:YNCKHTQCWBTRNJIV4WNAE52SJUQCZO5C&lt;/identifier&gt;
      &lt;title&gt;My Way&lt;/title&gt;
      &lt;creator&gt;Frank Sinatra&lt;/creator&gt;
      &lt;annotation&gt;This is my theme song.&lt;/annotation&gt;
      &lt;info&gt;http://franksinatra.com/myway&lt;/info&gt;
      &lt;image&gt;http://franksinatra.com/img/myway&lt;/image&gt;
      &lt;album&gt;Frank Sinatra&apos;s Greatest Hits&lt;/album&gt;
      &lt;trackNum&gt;3&lt;/trackNum&gt;
      &lt;duration&gt;19200&lt;/duration&gt;
      &lt;link rel="http://foaf.org/namespace/version1"&gt;http://socialnetwork.org/foaf/mary.rdfs&lt;/link&gt;
      &lt;meta rel="http://example.org/key"&gt;value&lt;/meta&gt;
      &lt;extension application="http://example.com"&gt;
        &lt;clip start="25000" end="34500"/&gt;
      &lt;/extension&gt;

    &lt;/track&gt;

  &lt;/trackList&gt;


&lt;/playlist&gt;
</pre>
can be transformed into
<pre>
&lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:rdfs="http://www.w3.org/2000/02/rdfschema#" xmlns:play="http://xspf.org/ns/0/" xmlns:mo="http://purl.org/ontology/mo/" xmlns="http://xspf.org/ns/0/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dct="http://purl.org/dc/terms/" xmlns:foaf="http://xmlns.com/foaf/0.1/" xmlns:cc="http://web.resource.org/cc/" xmlns:owl="http://www.w3.org/2002/07/owl#"&gt;
  &lt;mo:MusicalItem rdf:about="magnet:?xt=urn:sha1:YNCKHTQCWBTRNJIV4WNAE52SJUQCZO5C"&gt;
    &lt;owl:sameAs rdf:resource="http://example.com/myplaylists/myplaylist"/&gt;
    &lt;rdfs:seeAlso rdf:resource="http://example.com/myplaylists"/&gt;
    &lt;foaf:maker&gt;Jane Doe&lt;/foaf:maker&gt;
    &lt;dc:created&gt;2005-01-08T17:10:47-05:00&lt;/dc:created&gt;
    &lt;cc:license rdf:resource="http://creativecommons.org/licenses/by/1.0/"/&gt;
    &lt;mo:license rdf:resource="http://creativecommons.org/licenses/by/1.0/"/&gt;
    &lt;dc:description&gt;My favorite songs&lt;/dc:description&gt;
    &lt;mo:image rdf:resource="http://example.com/img/mypicture"/&gt;
    &lt;mo:track&gt;
      &lt;mo:Track rdf:about="magnet:?xt=urn:sha1:YNCKHTQCWBTRNJIV4WNAE52SJUQCZO5C"&gt;
        &lt;mo:available_as rdf:resource="http://example.com/my.mp3"/&gt;
        &lt;foaf:maker&gt;Frank Sinatra&lt;/foaf:maker&gt;
        &lt;dc:title&gt;My Way&lt;/dc:title&gt;
        &lt;mo:album&gt;
          &lt;mo:MusicalWork&gt;
            &lt;dc:title&gt;Frank Sinatra's Greatest Hits&lt;/dc:title&gt;
          &lt;/mo:MusicalWork&gt;
        &lt;/mo:album&gt;
        &lt;dc:description&gt;This is my theme song.&lt;/dc:description&gt;
        &lt;mo:image rdf:resource="http://franksinatra.com/img/myway"/&gt;
        &lt;rdfs:seeAlso rdf:resource="http://franksinatra.com/myway"/&gt;
      &lt;/mo:Track&gt;
    &lt;/mo:track&gt;
  &lt;/mo:MusicalItem&gt;
&lt;/rdf:RDF&gt;
</pre>


  <h2>License</h2>
  <!-- Creative Commons License -->
  <a rel="license" href="http://creativecommons.org/licenses/by-sa/2.0/"><img alt="Creative Commons License" border="0" src="http://creativecommons.org/images/public/somerights20.gif" /></a><br />
This work is licensed under a <a rel="license"
href="http://creativecommons.org/licenses/by-sa/2.0/">Creative Commons License</a>.
<!-- /Creative Commons License -->

<!--

<rdf:RDF xmlns="http://web.resource.org/cc/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
<Work rdf:about="">
   <license
rdf:resource="http://creativecommons.org/licenses/by-sa/2.0/" />
</Work>

<License rdf:about="http://creativecommons.org/licenses/by-sa/2.0/">
   <permits rdf:resource="http://web.resource.org/cc/Reproduction" />
   <permits rdf:resource="http://web.resource.org/cc/Distribution" />
   <requires rdf:resource="http://web.resource.org/cc/Notice" />
   <requires rdf:resource="http://web.resource.org/cc/Attribution" />
   <permits rdf:resource="http://web.resource.org/cc/DerivativeWorks" />
   <requires rdf:resource="http://web.resource.org/cc/ShareAlike" />
</License>

</rdf:RDF>

-->
</div>


<xsl:template match='play:playlist'>
<rdf:RDF>
  <xsl:choose>

    <xsl:when test="play:identifier">
      <xsl:call-template name="playlist">      
        <xsl:with-param name="url">
          <xsl:choose>
            <xsl:when test="function-available('resolve-uri') and function-available('base-uri')">
              <xsl:value-of select="fn:resolve-uri(play:identifier, fn:base-uri(play:identifier))" />
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="play:identifier" />
            </xsl:otherwise>
          </xsl:choose>   
        </xsl:with-param>
      </xsl:call-template>
    </xsl:when>

    <xsl:when test="play:location">
      <xsl:call-template name="playlist">      
        <xsl:with-param name="url">
          <xsl:choose>
            <xsl:when test="function-available('resolve-uri') and function-available('base-uri')">
              <xsl:value-of select="fn:resolve-uri(play:location, fn:base-uri(play:location))" />
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="play:location" />
            </xsl:otherwise>
          </xsl:choose>   
        </xsl:with-param>
      </xsl:call-template>
    </xsl:when>
        
    <xsl:otherwise>
      <xsl:call-template name="playlist">
        <xsl:with-param name="url"></xsl:with-param>
      </xsl:call-template>
    </xsl:otherwise>

  </xsl:choose>
</rdf:RDF>
</xsl:template>

<!-- Playlist -->
<xsl:template name="playlist">
 <xsl:param name="url" />
 <mo:MusicalItem rdf:about="{$url}">

    <xsl:if test="play:title">
        <dc:title><xsl:value-of select="play:title" /></dc:title>
    </xsl:if>

    <!-- Do we have two URLs which can be used for this item? -->
    <xsl:if test="play:identifier and play:location">
      <xsl:choose>
        <xsl:when test="function-available('resolve-uri') and function-available('base-uri')">
          <owl:sameAs rdf:resource="{fn:resolve-uri(play:location, fn:base-uri(play:location))}" />
        </xsl:when>
        <xsl:otherwise>
          <owl:sameAs rdf:resource="{play:location}"/>
        </xsl:otherwise>
      </xsl:choose>   
    </xsl:if>
    
    <xsl:if test="play:info">
      <xsl:choose>
        <xsl:when test="function-available('resolve-uri') and function-available('base-uri')">
          <rdfs:seeAlso rdf:resource="{fn:resolve-uri(play:info, fn:base-uri(play:info))}" />
        </xsl:when>
        <xsl:otherwise>
          <rdfs:seeAlso rdf:resource="{play:info}" />
        </xsl:otherwise>
      </xsl:choose>   
    </xsl:if>

    <xsl:if test="play:creator">
      <foaf:maker><xsl:value-of select="play:creator" />
      </foaf:maker>
    </xsl:if>

    <xsl:if test="play:date">
       <dc:created><xsl:value-of select="play:date" /></dc:created>
    </xsl:if>

    <xsl:if test="play:license">
      <xsl:choose>
        <xsl:when test="function-available('resolve-uri') and function-available('base-uri')">
          <cc:license rdf:resource="{fn:resolve-uri(play:license, fn:base-uri(play:license))}" />
          <mo:license rdf:resource="{fn:resolve-uri(play:license, fn:base-uri(play:license))}" />
        </xsl:when>
        <xsl:otherwise>
          <cc:license rdf:resource="{play:license}" />
          <mo:license rdf:resource="{play:license}" />
        </xsl:otherwise>
      </xsl:choose>    

    </xsl:if>

    <xsl:if test="play:annotation">
      <dc:description><xsl:value-of select="play:annotation" /></dc:description>
    </xsl:if>
  
    <xsl:if test="play:image">
      <xsl:choose>
        <xsl:when test="function-available('resolve-uri') and function-available('base-uri')">
          <mo:image rdf:resource="{fn:resolve-uri(play:image, fn:base-uri(play:image))}" />
        </xsl:when>
        <xsl:otherwise>
          <mo:image rdf:resource="{play:image}" />
        </xsl:otherwise>
      </xsl:choose>    
    </xsl:if>

    <!-- TODO: meta -->
    <!-- TODO: version -->
    <!-- TODO: link -->
    <!-- TODO: attribution -->
    <!-- TODO: extension -->

    <!-- TODO: Worry about xml:base? -->

    <xsl:call-template name="track-list" />


  </mo:MusicalItem>
</xsl:template>

<!-- Track List -->
<xsl:template name="track-list">
  <xsl:for-each select="play:trackList/play:track">
    <mo:track>
      <xsl:choose>
 
        <xsl:when test="play:identifier">
          <xsl:call-template name="track">      
            <xsl:with-param name="id">
              <xsl:choose>
                <xsl:when test="function-available('resolve-uri') and function-available('base-uri')">
                  <xsl:value-of select="fn:resolve-uri(play:identifier, fn:base-uri(play:identifier))" />
                </xsl:when>
                <xsl:otherwise>
                  <xsl:value-of select="play:identifier" />
                </xsl:otherwise>
              </xsl:choose>   
            </xsl:with-param>
          </xsl:call-template>
        </xsl:when>

      
       <xsl:otherwise>
         <xsl:call-template name="track">
           <xsl:with-param name="id">#<xsl:value-of select="generate-id(.)" /></xsl:with-param>
         </xsl:call-template>
       </xsl:otherwise>
     </xsl:choose>
    </mo:track>
  </xsl:for-each>
</xsl:template>

<!-- Track -->
<xsl:template name='track'>
  <xsl:param name="id" />
  
  <mo:Track rdf:about="{$id}">

    <!-- 0 or more -->
    <xsl:if test="play:location">
      <xsl:choose>
        <xsl:when test="function-available('resolve-uri') and function-available('base-uri')">
          <mo:available_as rdf:resource="{fn:resolve-uri(play:location, fn:base-uri(play:location))}" />
        </xsl:when>
        <xsl:otherwise>
          <mo:available_as rdf:resource="{play:location}"/>
        </xsl:otherwise>
      </xsl:choose>   
    </xsl:if>

    <xsl:if test="play:creator">
       <foaf:maker><xsl:value-of select="play:creator" /></foaf:maker>
       <!-- mo:MusicArtist? -->
    </xsl:if>

    <xsl:if test="play:title">
      <dc:title><xsl:value-of select="play:title" /></dc:title>
    </xsl:if>

    <xsl:if test="play:album">
      <mo:album>
        <mo:MusicalWork>
          <dc:title><xsl:value-of select="play:album" /></dc:title>
        </mo:MusicalWork>
      </mo:album>
    </xsl:if>

    <xsl:if test="play:annotation">
      <dc:description><xsl:value-of select="play:annotation" /></dc:description>
    </xsl:if>

    <xsl:if test="play:image">
      <xsl:choose>
        <xsl:when test="function-available('resolve-uri') and function-available('base-uri')">
          <mo:image rdf:resource="{fn:resolve-uri(play:image, fn:base-uri(play:image))}" />
        </xsl:when>
        <xsl:otherwise>
          <mo:image rdf:resource="{play:image}" />
        </xsl:otherwise>
      </xsl:choose>    
    </xsl:if>

    <xsl:if test="play:info">
      <xsl:choose>
        <xsl:when test="function-available('resolve-uri') and function-available('base-uri')">
          <rdfs:seeAlso rdf:resource="{fn:resolve-uri(play:info, fn:base-uri(play:info))}" />
        </xsl:when>
        <xsl:otherwise>
          <rdfs:seeAlso rdf:resource="{play:info}" />
        </xsl:otherwise>
      </xsl:choose>   
    </xsl:if>

    <!-- duration -->
    <!-- trackNum -->
    <!-- link -->
    <!-- meta -->
    <!-- extension -->
  </mo:Track>
</xsl:template>

<!-- don't pass text thru -->
<xsl:template match="text()|@*">
</xsl:template>

</xsl:transform>
