'''
Created on Jul 20, 2010

@author: kurtjx
'''

import RDF, uuid,cherrypy
from pyechonest import artist, config
import urllib
import xml.dom.minidom as minidom
try:
    from xml.etree.cElementTree import fromstring
except ImportError:
    from xml.etree.ElementTree import fromstring

from settings import URI_BASE_MBID, METHOD_URI
# kurtjx's api key hard coded, nice
config.ECHO_NEST_API_KEY = 'NN5CXYTRMEXRFSPZZ'



ttl_prefix = '''
@prefix sim: <http://purl.org/ontology/similarity/> .
@prefix mo: <http://purl.org/ontology/mo/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

<%(suburi)s> a mo:MusicArtist .
'''

ttl_sim_tmpl = '''
<%(simuri)s> a sim:Similarity ;
  sim:subject <%(suburi)s> ;
  sim:object <%(objuri)s> ;
  sim:distance "%(rank)s"^^xsd:integer ;
  sim:method <%(method)s> .
  
<%(objuri)s> foaf:name "%(obj_name)s" ;
  a mo:MusicArtist .
'''

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
    suburi = URI_BASE_MBID+mbid
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
                objuri = URI_BASE_MBID+obj_mbid
                
            else:
                pass
        
        obj_name = str(atree.findtext('name'))
        rank = str(atree.findtext('rank'))
        simuri = suburi+'#sim'+rank
        ttl+=ttl_sim_tmpl%locals()
    
    parser.parse_string_into_model(model, ttl.encode('utf-8'), suburi)
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
    
ttl_method = '''
@prefix meth: <%s> .
@prefix sim: <http://purl.org/ontology/similarity/> .
@prefix mo: <http://purl.org/ontology/mo/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

meth: a sim:AssociationMethod ;
  rdfs:label "Similarities between artists are determined by Echonest using some proprietary algorithm and retrieved from the Echonest API described at http://developer.echonest.com/docs/v4/artist.html#similar."@en .
  
'''% METHOD_URI

method = RDF.Model()
p = RDF.TurtleParser()
p.parse_string_into_model(method, ttl_method)