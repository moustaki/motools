'''
Created on Jun 17, 2009

@author: kurtjx
'''
import unittest
import os
# change to src directory
os.chdir('../src')
from myspace.myspace2rdf import MyspaceScrape
from myspace.triplestore import TripleStore
GRAPH = "http://insertsparql.test.graph"
import rdflib

class InsertSparqlTest(unittest.TestCase):

    def setUp(self):
        
        print 'getting myspace data'
        self.short_url_artist = 'kurtisrandom'
        self.uid_artist = '30650288'
        self.A = MyspaceScrape(uid=self.uid_artist)
        self.A.run()
    
    def test_insert_sparql(self):
        print 'inserting'
        #cursor = self.connect.cursor()
        self.A.insert_sparql()
        print 'checking insert'
        
        res = TripleStore().query('''SELECT ?same WHERE { <http://dbtune.org/myspace/uid/30650288> <http://www.w3.org/2002/07/owl#sameAs> ?same . }  ''')
        #print res
        same = res[0]['same']
        assert rdflib.URIRef('http://dbtune.org/myspace/kurtisrandom') == same, 'wrong sameAs result: ' +str(same)
         
        #cursor.close()
        
        
    def tearDown(self):
        TripleStore().delete_graph(GRAPH)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_insert_sparql']
    unittest.main()