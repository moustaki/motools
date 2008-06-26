<xsl:transform 
    xmlns:xsl  ="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:rdf  ="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs ="http://www.w3.org/2000/02/rdfschema#"
    xmlns:play ="http://xspf.org/ns/0/" 
    xmlns:mo   ="http://purl.org/ontology/mo/"
    xmlns ="http://xspf.org/ns/0/" 
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
<mo:track>
<xsl:for-each select="play:trackList/play:track">
  <xsl:apply-templates select="play:track"/>
   <mo:Track>
   <mo:available_as rdf:resource="{play:location}"/>
  </mo:Track>
</xsl:for-each>
</mo:track>
</mo:Playlist>
</rdf:RDF>
</xsl:template>

<xsl:template match='play:track'>
<mo:Track>
 <mo:available_as rdf:resource="{play:location}"/>
</mo:Track>
</xsl:template>

<!--<xsl:variable name="itemURI">-->

<!-- don't pass text thru -->
<xsl:template match="text()|@*">
</xsl:template>

</xsl:transform>
