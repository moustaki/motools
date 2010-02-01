'''
Created on May 15, 2009

@author: kurtjx
'''

from rdflib import ConjunctiveGraph, URIRef

class Htmlify:
    '''make an html version of rdf resource w/ audio'''
    def __init__(self, uri):
        self.uri = uri
        self.rdf_graph = ConjunctiveGraph()
        # lets make pretty namespaces
        self.rdf_graph.namespace_manager.bind("mo", URIRef("http://purl.org/ontology/mo/"))
        self.rdf_graph.namespace_manager.bind("foaf", URIRef("http://xmlns.com/foaf/0.1/"))
        self.rdf_graph.namespace_manager.bind("musim", URIRef("http://purl.org/ontology/musim#"))
        self.rdf_graph.namespace_manager.bind("dc", URIRef("http://purl.org/dc/elements/1.1/"))
        self.rdf_graph.namespace_manager.bind("owl", URIRef("http://www.w3.org/2002/07/owl#"))

        self.html_head = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>%s</title>
    <script type="text/javascript" src="http://mediaplayer.yahoo.com/js"></script>
        <link rel="stylesheet" type="text/css" href="/css/style.css" />
</head><body>''' % uri
        self.html_tail = '''</body>
</html>'''
        
    def parse_rdf(self):
        try:
            self.rdf_graph.parse(self.uri)
        except:
            self.rdf_graph = None
        
    def serialize_n3(self):
        '''serialize to n3 and return as html w/ <pre> tags'''
        if self.rdf_graph is not None:
            self.rdf_graph.namespace_manager.bind("mo", URIRef("http://purl.org/ontology/mo/"))
            self.rdf_graph.namespace_manager.bind("foaf", URIRef("http://xmlns.com/foaf/0.1/"))
            self.rdf_graph.namespace_manager.bind("musim", URIRef("http://purl.org/ontology/musim#"))
            self.rdf_graph.namespace_manager.bind("dc", URIRef("http://purl.org/dc/elements/1.1/"))
            self.rdf_graph.namespace_manager.bind("owl", URIRef("http://www.w3.org/2002/07/owl#"))
            self.rdf_graph.namespace_manager.bind("myspace", URIRef("http://purl.org/ontology/myspace#"))
            self.rdf_graph.namespace_manager.bind("dbtune", URIRef("http://dbtune.org/myspace/"))
            # TODO: fix unicode - ignoring errors cuz this was causing problems...
            html = unicode("<pre>"+self.rdf_graph.serialize(format='n3').replace('<', '&lt;').replace('>', '&gt;')+"</pre><br>", errors='ignore')
            return html
        else:
            return "internal error: should have an rdf graph but do not."
    
    def get_all(self):
        '''just print a list of triples as html @deprecated: use serialize_n3'''
        if self.rdf_graph != None:
            href =""
            for row in self.rdf_graph.query('''SELECT ?s ?p ?o WHERE { ?s ?p ?o . } ORDER BY DESC(?s)'''):
                href+= '''%s - %s - %s <br>''' % row
            self.html = href
        else:
            self.html = "nothing there???"
        
    def get_available_as(self):
        if self.rdf_graph != None:
            href = ""
            for row in self.rdf_graph.query("SELECT ?af ?title ?name WHERE { ?track <http://purl.org/ontology/mo/available_as> ?af; <http://purl.org/dc/elements/1.1/title> ?title . ?artist <http://xmlns.com/foaf/0.1/made> ?track ; <http://xmlns.com/foaf/0.1/name> ?name }"):
                track = "<track><location>%s</location><title>%s</title><creator>%s</creator></track>" % row
                href += '''<a href="'''+row[0]+'''">'''+row[1]+'''</a><br>'''
            self.tracks = href
            return href
        else:
            return "error - no rdf graph"
        