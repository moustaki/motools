'''
Created on Jul 20, 2010

@author: kurtjx
'''

import RDF, cherrypy
from pyechonest import config
import urllib
import xml.dom.minidom as minidom
try:
    from xml.etree.cElementTree import fromstring
except ImportError:
    from xml.etree.ElementTree import fromstring

from settings import URI_BASE_MBID, METHOD_URI
# kurtjx's api key hard coded, nice
config.ECHO_NEST_API_KEY = 'NN5CXYTRMEXRFSPZZ'

def get_bbc_uri(mbid):
    return 'http://www.bbc.co.uk/music/artists/'+str(mbid)+'#artist'
    
def get_musicbrainz_uri(mbid):
    return 'http://dbtune.org/musicbrainz/resource/artist/'+mbid


ttl_prefix = '''
@prefix sim: <http://purl.org/ontology/similarity/> .
@prefix mo: <http://purl.org/ontology/mo/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

<%(sub_uri)s> a mo:MusicArtist ;
  owl:sameAs <%(sub_bbc)s>, <%(sub_mbz)s> .
'''

ttl_sim_tmpl = '''
<%(sim_uri)s> a sim:Similarity ;
  sim:subject <%(sub_uri)s> ;
  sim:object <%(obj_uri)s> ;
  sim:distance "%(rank)s"^^xsd:integer ;
  sim:method <%(method)s> .
  
'''.encode('utf-8')

ttl_obj_tmpl = '''
<%(obj_uri)s> foaf:name "%(obj_name)s" ;
  owl:sameAs <%(obj_bbc)s> , <%(obj_mbz)s> ;
  a mo:MusicArtist .'''.encode('utf-8')
  
ttl_obj_tmpl_err = '''
<%(obj_uri)s> a mo:MusicArtist ;
  owl:sameAs <%(obj_bbc)s> , <%(obj_mbz)s> .'''

def get_similar(mbid):
    params = {'id': 'musicbrainz:artist:'+mbid,
              'api_key':config.ECHO_NEST_API_KEY,
              'version': 3}
    for k,v in params.items():
        if isinstance(v, unicode):
            params[k] = v.encode('utf-8')
    params = urllib.urlencode(params)
    url = 'http://%s%s%s?%s' % (config.API_HOST, config.API_SELECTOR,
                                'get_similar',params)
    for bucket in ['id:musicbrainz']:
        url+='&bucket='+bucket
    f = urllib.urlopen(url)
    xml = f.read()
    tree = fromstring(xml)
    if check_status(tree) is None:
        raise cherrypy.HTTPError(status="404",message="could not resolve mbid %s"%mbid)
    
    model = RDF.Model()
    parser = RDF.TurtleParser()
    
    method = METHOD_URI
    sub_bbc = get_bbc_uri(mbid)
    sub_uri = URI_BASE_MBID+mbid
    sub_mbz = get_musicbrainz_uri(mbid)
    ttl = ttl_prefix % locals()

    dom = minidom.parseString(xml)
    artists_dom = dom.getElementsByTagName('similar')[0].childNodes
    for idx,adom in enumerate(artists_dom):
        # stupid bnodes need to start w/ a letter
        #bnode = 'b'+str(uuid.uuid1()).replace('-','')
        atree = tree.find('similar').getchildren()[idx]
        ids = adom.getElementsByTagName('id')
        for id in ids:
            if id.attributes.has_key('type'):
                obj_mbid = id.firstChild.toxml().split('musicbrainz:artist:')[1]
                obj_uri = URI_BASE_MBID+obj_mbid
                obj_bbc = get_bbc_uri(obj_mbid)
                obj_mbz = get_musicbrainz_uri(obj_mbid)
            else:
                pass
        
        obj_name = atree.findtext('name').encode('utf-8')
        rank = str(atree.findtext('rank'))
        sim_uri = sub_uri+'#sim'+rank
        ttl+=ttl_sim_tmpl%locals()
        
        try:
            l = locals()
            for k,v in l.items():
                if isinstance(v, unicode):
                    l[k] = v.encode('utf-8')
            ttl+=ttl_obj_tmpl%l
        except UnicodeDecodeError:
            ttl+=ttl_obj_tmpl_err%locals()
            
    
    parser.parse_string_into_model(model, ttl.encode('utf-8'), sub_uri)
    return model


def dictify(result):
    return dict((element.tag, element.text)for element in result.getchildren())
    

def check_status(etree):
    code = int(etree.getchildren()[0].getchildren()[0].text)
    #message = etree.getchildren()[0].getchildren()[1].text
    if code!=0:
        #raise EchoNestAPIError(code, message)
        return None
    else:
        return etree

label = 'Similarities between artists are determined by Echonest using some proprietary algorithm and retrieved from the Echonest API described at http://developer.echonest.com/docs/v4/artist.html#similar.' 
ttl_method = '''
@prefix meth: <%s> .
@prefix sim: <http://purl.org/ontology/similarity/> .
@prefix mo: <http://purl.org/ontology/mo/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

meth: a sim:AssociationMethod ;
  rdfs:label "%s"@en .
  
'''% (METHOD_URI,label)

method = RDF.Model()
p = RDF.TurtleParser()
p.parse_string_into_model(method, ttl_method, METHOD_URI)

method_html = '''<html
    version="XHTML+RDFa 1.0"
    xmlns="http://www.w3.org/1999/xhtml"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xml:lang="en">
    
  <head>
    <title>Echonest Association Method</title><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="alternate" type="application/rdf+xml" href="method.rdf" title="RDF/XML"/>
    <link rel="alternate" type="text/n3" href="method.ttl" title="Turtle"/>
    
    <link rel="stylesheet" type="text/css" href="css/rdfstyle.css" media="screen" />
  </head>
  <body>
    <h1>about</h1>
  <h2>http://dbtune.org/artists/echonest/method</h2>
  <p>view as <a href="method.rdf" title="RDF/XML">RDF/XML</a> or <a href="method.ttl" title="Turtle">Turtle</a></p>
  <table>
  <th>property</th><th>object</th>
  <tr class="odd">
  <td>rdf:type</td><td>sim:AssociationMethod</td>
  </tr>
  <tr class="odd">
  <td>rdfs:label</td><td>%s</td>

</body>
</html>
'''%label