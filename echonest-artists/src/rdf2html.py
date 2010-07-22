'''
Created on Jul 21, 2010

@author: kurtjx
'''

import RDF
from collections import defaultdict
from dothtml_tmpl import dothtml_tmpl
from settings import URI_BASE_MBID

sim = RDF.NS('http://purl.org/ontology/similarity/')
mo = RDF.NS('http://purl.org/ontology/mo/')
rdf = RDF.NS('http://www.w3.org/1999/02/22-rdf-syntax-ns#')

prefix_dict = {'http://purl.org/ontology/similarity/':'sim',
               'http://purl.org/ontology/mo/':'mo',
               'http://www.w3.org/1999/02/22-rdf-syntax-ns#':'rdf',
               'http://dbtune.org/artists/echonest/':'dben',
               'http://xmlns.com/foaf/0.1/':'foaf'}

query_sims = '''
SELECT DISTINCT ?s ?p ?o WHERE {
?s a <http://purl.org/ontology/similarity/Similarity> ;
   ?p ?o .
}
'''

query_artists = '''
SELECT DISTINCT ?s ?p ?o WHERE {
?s a <http://purl.org/ontology/mo/MusicArtist> ;
   ?p ?o .
}
'''

def rdf2html(model,mbid):
    #for sim_statment in m.find_statements(RDF.Statement(None,rdf.type,sim.Similarity)):
    #    for triple in sim_statement
    html = dothtml_tmpl()
    query = RDF.SPARQLQuery(query_sims)
    uri = URI_BASE_MBID+mbid
    sims = {}
    for result in query.execute(model):
        s_html = '<a href="%s">%s</a>' % (str(result['s'])[1:-1],_get_curie(str(result['s'])[1:-1]))
        p_html = '<a href="%s">%s</a>' % (str(result['p'])[1:-1],_get_curie(str(result['p'])[1:-1]))
        if result['o'].is_literal():
            o_html = str(result['o']).replace('<','&lt;').replace('>','&gt;')
        else: 
            o = str(result['o'])[1:-1]
            o_html = '<a href="%s">%s</a>' % (o,_get_curie(o))
        if not sims.has_key(s_html): sims.update({s_html:{} })
        if not sims[s_html].has_key(p_html): sims[s_html].update({p_html:[]})
        sims[s_html][p_html].append(o_html)
        
    artists = {}
    query = RDF.SPARQLQuery(query_artists)
    for result in query.execute(model):
        s_html = '<a href="%s">%s</a>' % (str(result['s'])[1:-1],_get_curie(str(result['s'])[1:-1]))
        p_html = '<a href="%s">%s</a>' % (str(result['p'])[1:-1],_get_curie(str(result['p'])[1:-1]).replace('rdf:type', 'a'))
        if result['o'].is_literal():
            o_html = str(result['o']).replace('<','&lt;').replace('>','&gt;')
        else: 
            o = str(result['o'])[1:-1]
            o_html = '<a href="%s">%s</a>' % (o,_get_curie(o))
        if not artists.has_key(s_html): artists.update({s_html:{} })
        if not artists[s_html].has_key(p_html): artists[s_html].update({p_html:[]})
        artists[s_html][p_html].append(o_html)
        
    html.title = uri
    html.n3 = uri+'.ttl'
    html.rdfxml = uri+'.rdf'
    html.sims = sims
    html.artists = artists
    return html.respond()
    
    #artists = model.find_statements(mo.MusicArtist)
    
def _get_curie(uri):
    for prefix,abbrv in prefix_dict.items():
        if prefix in uri: uri=uri.replace(prefix, abbrv+':')
    return uri
    
    