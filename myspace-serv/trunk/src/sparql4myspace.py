'''
Created on Jun 12, 2009

@author: kurtjx
'''

import re
import time
from datetime import date, timedelta
from rdflib import ConjunctiveGraph
from ConfigParser import ConfigParser, Error
import time


config = ConfigParser()
try:
    config.read('config')
except:
    print 'error, no config file\n  exting...'
    sys.exit(1)

GRAPH = config.get('ODBC', 'graph')[1:-1]

EXPIRE_DAYS = 30

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
        
    def select(self):
        data = []
        q = '''SPARQL SELECT ?p ?o FROM '''+GRAPH+''' WHERE {<%s> ?p ?o}'''
        self.cursor.execute(q % self.uri)
        for r in self.cursor:   data.append(r)
        # blank data if it is too old or not time stamped
        old_date = '2009-01-01'     # should never be older than this :-)
        q = '''SPARQL SELECT ?time FROM '''+GRAPH+''' WHERE { <%s> <http://purl.org/dc/terms/modified> ?time}'''
        self.cursor.execute(q % self.uri)
        for r in self.cursor:   old_date = r[0]
        if not self.__still_fresh__(old_date):
            data = []
            
        if len(data)>0:
            self.triples = data
            return True
        else:
            return False
        
    def make_graph(self):
        self.graph = ConjunctiveGraph()
        self.graph.namespace_manager.bind("mo", rdflib.URIRef("http://purl.org/ontology/mo/"))
        self.graph.namespace_manager.bind("foaf", rdflib.URIRef("http://xmlns.com/foaf/0.1/"))
        self.graph.namespace_manager.bind("myspace", rdflib.URIRef("http://purl.org/ontology/myspace#"))
        self.graph.namespace_manager.bind("dc", rdflib.URIRef("http://purl.org/dc/elements/1.1/"))
        self.graph.namespace_manager.bind("owl", rdflib.URIRef("http://www.w3.org/2002/07/owl#"))
        for triple in self.triples:
            self.graph.add((self.uri, triple[0], triple[1]))
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
        