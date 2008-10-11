<xsl:transform 
    xmlns:xsl  ="http://www.w3.org/1999/XSL/Transform" version="1.0">

<xsl:output method="html" indent="yes" encoding="utf-8"/>


<xsl:template match="/">
<div xmlns="http://www.w3.org/1999/xhtml">
  <h1>XSPF Namespace Document</h1>
  <p>This is the namespace of <a href="http://xspf.org">XSPF</a>.</p>
  <p>There is <a href="http://xspf.org/xspf-v1.html">documentation</a> and a <a href="XSPF.xsl">GRDDL namespace transformation</a> available.</p>

  <h2>Example XSPF</h2>
The below is an example XSPF playlist
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
</div>

</xsl:template>
<!-- don't pass text thru -->
<xsl:template match="text()|@*">
</xsl:template>

</xsl:transform>
