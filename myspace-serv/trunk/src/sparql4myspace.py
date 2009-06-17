'''
Created on Jun 12, 2009

@author: kurtjx
'''

import re
import time
from datetime import date, timedelta
from rdflib import ConjunctiveGraph, URIRef
from ConfigParser import ConfigParser, Error
import time


config = ConfigParser()
try:
    config.read('config')
except:
    print 'error, no config file\n  exting...'
    sys.exit(1)

GRAPH = config.get('ODBC', 'graph')[1:-1]

EXPIRE_DAYS = int(config.get('ODBC', 'expiration'))

class SparqlSpace(object):
    '''
    Check the sparql endpoint connected by odbc for the input uri
    
    
    '''


    def __init__(self, uri, cursor):
        '''
        Constructor
        '''
        self.cursor = cursor
        self.uri = uri
        
    def select(self, graph=GRAPH):
        data = []
        q = '''SPARQL SELECT DISTINCT ?p ?o FROM <'''+graph+'''> WHERE {<%s> ?p ?o}'''
        self.cursor.execute(q % self.uri)
        for r in self.cursor:   data.append(r)
        # blank data if it is too old or not time stamped
        old_date = '2009-01-01'     # should never be older than this :-)
        q = '''SPARQL SELECT DISTINCT ?time FROM <'''+graph+'''> WHERE { <%s> <http://purl.org/dc/terms/modified> ?time } ORDER BY ASC (?time)'''
        self.cursor.execute(q % self.uri)
        for r in self.cursor:   old_date = r[0]
        if not self.__still_fresh__(old_date):
            # delete the old modified triple to avoid confusion?
            data = []
            
        if len(data)>0:
            self.triples = data
            # get song triples
            self.cursor.execute('SPARQL SELECT ?track ?p ?o from <%s> WHERE { <%s> <http://xmlns.com/foaf/0.1/made> ?track . ?track ?p ?o . }' % (graph, self.uri))
            self.song_triples = []
            for triple in self.cursor:
                self.song_triples.append(triple)
            return True
        else:
            return False
        
    def make_graph(self):
        self.graph = ConjunctiveGraph()
        self.graph.namespace_manager.bind("mo", URIRef("http://purl.org/ontology/mo/"))
        self.graph.namespace_manager.bind("foaf", URIRef("http://xmlns.com/foaf/0.1/"))
        self.graph.namespace_manager.bind("myspace", URIRef("http://purl.org/ontology/myspace#"))
        self.graph.namespace_manager.bind("dc", URIRef("http://purl.org/dc/terms/"))
        self.graph.namespace_manager.bind("dcele", URIRef("http://purl.org/dc/elements/1.1/"))
        self.graph.namespace_manager.bind("owl", URIRef("http://www.w3.org/2002/07/owl#"))
        for triple in self.triples:
            self.graph.add((URIRef(self.uri), URIRef(triple[0]), URIRef(triple[1])))
        for triple in self.song_triples:
            self.graph.add((URIRef(triple[0]), URIRef(triple[1]), URIRef(triple[2])))
        return self.graph.serialize()
        
    def __still_fresh__(self, date_string):
        d = date(int(date_string.split('-')[0]), int(date_string.split('-')[1]), int(date_string.split('-')[2][:2]))
        now = time.strftime('%Y-%m-%d').split('-')
        today = date(int(now[0]), int(now[1]), int(now[2]))
        maxdays = timedelta(EXPIRE_DAYS)
        if today-d > maxdays:
            return False
        else:
            return True
        