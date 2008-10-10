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
    >

 <!-- 

see http://xspf.org/

-->


<xsl:output method="xml" indent="yes" encoding="utf-8"/>

<div xmlns="http://www.w3.org/1999/xhtml">
<p>testing GRDDL for xspf.com: examples taken from
http://gonze.com/xspf/xspf-draft-8.html
</p>
<p>Copyright (c) <a href="http://www.asemantics.com">Asemantics
S.R.L</a>, 2005</p>

<!-- Creative Commons License -->
<a rel="license"
href="http://creativecommons.org/licenses/by-sa/2.0/"><img alt="Creative
Commons License" border="0"
src="http://creativecommons.org/images/public/somerights20.gif"
/></a><br />
This work is licensed under a <a rel="license"
href="http://creativecommons.org/licenses/by-sa/2.0/">Creative Commons
License</a>.
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


<address>
<a href="mailto:libby@asemantics.com">libby Miller</a>
</address>
</div>

<!--<xsl:apply-templates />-->

<xsl:template match='play:playlist'>
<rdf:RDF>

  <mo:Playlist>
    <version><xsl:value-of select='@version'/></version>
  
    <!-- Track List -->
    <xsl:for-each select="play:trackList/play:track">
      <mo:track>
        <xsl:choose>

        <xsl:when test="play:identifier">
          <xsl:call-template name="track">      
            <xsl:with-param name="id">
              <xsl:value-of select="play:identifier" />
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

  </mo:Playlist>
</rdf:RDF>
</xsl:template>


<!-- Track -->
<xsl:template name='track'>
  <xsl:param name="id" />
  
  <mo:Track rdf:about="{$id}">

    <!-- 0 or more -->
    <xsl:if test="play:location">
      <mo:available_as rdf:resource="{play:location}"/>
    </xsl:if>

    <xsl:if test="play:creator">
       <dc:creator>
         <xsl:value-of select="play:creator" />
       </dc:creator>
       <!-- mo:MusicalArtist? -->
    </xsl:if>

    <xsl:if test="play:title">
      <dc:title><xsl:value-of select="play:title" /></dc:title>
    </xsl:if>

    <xsl:if test="play:album">
      <!-- WRONG -->
      <mo:album><xsl:value-of select="play:album" /></mo:album>
    </xsl:if>

    <xsl:if test="play:annotation">
      <dc:description><xsl:value-of select="play:annotation" /></dc:description>
    </xsl:if>

    <xsl:if test="play:image">
      <mo:image rdf:resource="{play:image}" />
    </xsl:if>

    <xsl:if test="play:info">
      <rdfs:seeAlso rdf:resource="{play:info}" />
    </xsl:if>
<!--
    <duration>271066</duration>
-->
  </mo:Track>
</xsl:template>

<!--<xsl:variable name="itemURI">-->

<!-- don't pass text thru -->
<xsl:template match="text()|@*">
</xsl:template>

</xsl:transform>
