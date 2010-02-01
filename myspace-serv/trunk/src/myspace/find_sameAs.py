'''
Created on Jul 2, 2009

@author: kurtjx
'''

from gnatlib import metadatalookup, MbzLookupException
from ConfigParser import ConfigParser, Error
from rdflib import ConjunctiveGraph, Namespace, URIRef
import os
import sys

config = ConfigParser()
try:
    config.read('config')
except Error:
    print 'error, no config file\n  exting...'
    sys.exit(1)

URL_BASE = config.get('urls', 'base')[1:-1] #"http://dbtune.org/myspace"
GRAPH = config.get('ODBC', 'graph')[1:-1]
WRITE_PATH = config.get('ODBC', 'write_path')[1:-1]


# set namespaces
OWL = Namespace("http://www.w3.org/2002/07/owl#")

class FindSameAs(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
        
        
    def get_sameAs(self, limit=500, offset=0):
        print '''getting list with limit %s and offset %s''' % (str(limit), str(offset))
        q = '''SPARQL define sql:log-enable 2 SELECT distinct ?name ?tname ?uri ?track ?mbz WHERE {?s <http://xmlns.com/foaf/0.1/name> ?name . ?s <http://xmlns.com/foaf/0.1/made> ?track . ?track <http://purl.org/dc/elements/1.1/title> ?tname . ?s <http://www.w3.org/2002/07/owl#sameAs> ?o . ?uri <http://www.w3.org/2002/07/owl#sameAs> ?o . optional { ?s <http://purl.org/ontology/mo/musicbrainz> ?mbz } } limit %s offset %s ''' % (str(limit), str(offset))
        self.cursor.execute(q)
        self.graph = ConjunctiveGraph()
        while(True):
            row = self.cursor.fetchone()
            if row == None:
                break
            mysp_artist_uri = row[2]
            mysp_track_uri = row[3]
            mbz = row[4]
            # if the artist already has a musicbrainz property, we don't try to find it again
            if mbz == None:
                try:
                    results = metadatalookup(artist=row[0], track=row[1], allow_ambiguous=True)
                except MbzLookupException, err:
                    print '''$$$$ MbzLookupException for %s with name %s and track %s''' % (mysp_artist_uri, row[0], row[1])
                    print str(err)
                    try:
                        results = metadatalookup(artist=row[0])
                    except MbzLookupException, err:
                        print '''straight aritst lookup failed as well, moving on... '''
                    else:
                        if results['score']==100:
                            print '''found a 100 score on pure artist lookup'''
                            self.graph.add((URIRef(mysp_artist_uri), OWL['sameAs'], URIRef(results['artistURI'])))
                            
                else:
                    self.graph.add((URIRef(mysp_artist_uri), OWL['sameAs'], URIRef(results['artistURI'])))
                    self.graph.add((URIRef(mysp_track_uri), OWL['sameAs'], URIRef(results['trackURI'])))
        
        fname = 'offset-%s.rdf' % str(offset)
        fname = os.path.join(WRITE_PATH, fname)
        self.graph.serialize(fname)
        q = "DB.DBA.RDF_LOAD_RDFXML_MT (file_to_string('"+ fname+"'), 'junk', '"+GRAPH+"')"
        self.cursor.execute(q)
        os.remove(fname)
        

def main():
    fsa = FindSameAs()
    limit = 500
    offset = 0
    while(True):
        fsa.get_sameAs(limit, offset)
        offset += limit
            
if __name__ == "__main__":
    sys.exit(main())
                       