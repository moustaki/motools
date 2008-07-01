<xsl:transform 
    xmlns:xsl  ="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:rdf  ="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs ="http://www.w3.org/2000/02/rdfschema#"
    xmlns:mo   ="http://purl.org/ontology/mo/"
    xmlns:af   ="http://purl.org/ontology/af/"
    xmlns:dc   ="http://purl.org/dc/elements/1.1/"
    xmlns:tl   ="http://purl.org/NET/c4dm/timeline.owl#"
    xmlns ="http://dbtune.org/echonest/" 
    >

<xsl:output method="xml" indent="yes" encoding="utf-8"/>

<div xmlns="http://www.w3.org/1999/xhtml">
<p>testing GRDDL for the Echonest Analyze API
</p>
<p>Copyright (c) <a href="http://moustaki.org/">Yves Raimond</a>, 2008</p>

<a rel="license"
href="http://creativecommons.org/licenses/by-sa/2.0/"><img alt="Creative
Commons License" border="0"
src="http://creativecommons.org/images/public/somerights20.gif"
/></a><br />
This work is licensed under a <a rel="license"
href="http://creativecommons.org/licenses/by-sa/2.0/">Creative Commons
License</a>.
</div>

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

<xsl:template match='Analysis'>
<rdf:RDF>
<mo:Signal rdf:about="#signal">
<mo:time>
<tl:Interval>
<tl:duration><xsl:value-of select='Track/@duration'/></tl:duration>
</tl:Interval>
</mo:time>
</mo:Signal>
</rdf:RDF>
</xsl:template>

</xsl:transform>
