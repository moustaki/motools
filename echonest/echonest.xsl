<xsl:transform 
    xmlns:xsl  ="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:rdf  ="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs ="http://www.w3.org/2000/02/rdfschema#"
    xmlns:mo   ="http://purl.org/ontology/mo/"
    xmlns:af   ="http://purl.org/ontology/af/"
    xmlns:dc   ="http://purl.org/dc/elements/1.1/"
    xmlns:tl   ="http://purl.org/NET/c4dm/timeline.owl#"
    xmlns:en   = "http://purl.org/ontology/echonest/"
    xmlns:event="http://purl.org/NET/c4dm/event.owl#"
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
<xsl:for-each select='Track'>

<!-- Describing the signal resource and track-wide features -->
<mo:Signal 
	rdf:about="#signal" 
	en:loudnessDynamicsVariance='{Tags/@loudnessDynamicsVariance}'
	en:timbreMean='{Tags/@timbreMean}'
	en:endOfFadeIn='{Tags/@endOfFadeIn}'
	en:loudnessBeginVariance='{Tags/@loudnessBeginVariance}'
	en:loudnessBeginMean='{Tags/@loudnessBeginMean}'
	en:beatVariance='{Tags/@beatVariance}'
	en:timeSignature_Stability='{Tags/@timeSignatureStability}'
	en:loudnessDynamicsMean='{Tags/@loudnessDynamicsMean}'
	en:timbreVariance='{Tags/@timbreVariance}'
	en:loudnessMaxVariance='{Tags/@loudnessMaxVariance}'
	en:loudnessMaxMean='{Tags/@loudnessMaxMean}'
	en:segmentDurationVariance='{Tags/@segmentDurationVariance}'
	en:sizeTimbre='{Tags/@sizeTimbre}'
	en:pitchMean='{Tags/@pitchMean}'
	en:startOfFadeOut='{Tags/@startOfFadeOut}'
	en:tatum='{Tags/@tatum}'
	en:timeLoudnessMaxMean='{Tags/@timeLoudnessMaxMean}'
	en:numTatums='{Tags/@numTatums}'
	en:tempoConfidence='{Tags/@tempoConfidence}'
	en:loudness='{Tags/@loudness}'
	en:tempo='{Tags/@tempo}'
	en:segmentDurationMean='{Tags/@segmentDurationMean}'
	en:numSections='{Tags/@numSections}'
	en:tatumConfidence='{Tags/@tatumConfidence}'
	en:timeSignature='{Tags/@timeSignature}'
	en:numBeats='{Tags/@numBeats}'
	en:sizePitches='{Tags/@sizePitches}'
	en:pitchVariance='{Tags/@pitchVariance}'
	en:numSegments='{Tags/@numSegments}'
	en:numTatumsPerBeat='{Tags/@numTatumsPerBeat}'
	en:tatums='{Tatums}'
	> 
<mo:time>
<tl:Interval>
<tl:duration><xsl:value-of select='@duration'/></tl:duration>
<tl:onTimeLine> <!-- Should be unique -->
<tl:TimeLine rdf:about="#timeline"/>
</tl:onTimeLine>
</tl:Interval>
</mo:time>
</mo:Signal>

<!-- Describing local features -->

<!--- Sadly XSLT 2.0 -->
<!--<xsl:variable name="tantumID" select="tokenize('@Tatums',' ')"/>
<xsl:for-each select="$tantumID">
<en:Tantum>
<event:time>
<tl:at><xsl:value-of select='.'/></tl:at>
<tl:onTimeLine rdf:resource="#timeline"/>
</event:time>
</en:Tantum>
</xsl:for-each>
-->


</xsl:for-each>
</rdf:RDF>
</xsl:template>

</xsl:transform>
