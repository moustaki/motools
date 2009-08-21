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
        # adding 'define sql:log-enable 2' to preven dead lock as suggested by Hugh Williams on VOS-devel list


        # blank data if it is too old or not time stamped
        old_date = '2009-01-01'     # should never be older than this :-)
        q = '''SPARQL define sql:log-enable 2 SELECT DISTINCT ?time FROM <'''+graph+'''> WHERE { <%s> <http://purl.org/dc/terms/modified> ?time } ORDER BY ASC (?time)'''
        self.cursor.execute(q % self.uri)
        for r in self.cursor:   old_date = r[0]
        if not self.__still_fresh__(old_date):
            # TODO: delete some triple here?
            return False
        else:
            q = '''SPARQL define sql:log-enable 2 define output:format "RDF/XML" construct { <%s> ?p ?o . ?track ?pp ?oo .  } from <%s> where { <%s> ?p ?o . optional {<%s> <http://xmlns.com/foaf/0.1/made> ?track . ?track ?pp ?oo . } }'''
            q = q % (self.uri, GRAPH, self.uri, self.uri)
            self.cursor.execute(q)
            for r in self.cursor:   data.append(r)
            self.triples = data
            return True


    def make_graph(self):
        ret = ''
        for triple in self.triples:
            for d in triple: ret+=d
        return ret


    def __still_fresh__(self, date_string):
        d = date(int(date_string.split('-')[0]), int(date_string.split('-')[1]), int(date_string.split('-')[2][:2]))
        now = time.strftime('%Y-%m-%d').split('-')
        today = date(int(now[0]), int(now[1]), int(now[2]))
        maxdays = timedelta(EXPIRE_DAYS)
        if today-d > maxdays:
            return False
        else:
            return True
