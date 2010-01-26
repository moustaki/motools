'''
Created on Jun 17, 2009

@author: kurtjx
'''
import unittest
import os
# change to src directory
os.chdir('../src')
from myspace2rdf import MyspaceScrape
import pyodbc
from ODBC import ODBC
import sys
VODBC = ODBC()
GRAPH = "http://insertsparql.test.graph"

class InsertSparqlTest(unittest.TestCase):

    def setUp(self):
        self.connect = VODBC.connect()
        self.connect.execute('SPARQL CLEAR GRAPH <%s>' % GRAPH) 
        print 'getting myspace data'
        self.short_url_artist = 'kurtisrandom'
        self.uid_artist = '30650288'
        self.A = MyspaceScrape(uid=self.uid_artist)
        self.A.run()
    
    def test_insert_sparql(self):
        print 'inserting'
        #cursor = self.connect.cursor()
        self.A.insert_sparql(self.connect, GRAPH)
        print 'checking insert'
        res = self.connect.execute('''SPARQL SELECT ?same FROM <%s> WHERE { <http://dbtune.org/myspace/uid/30650288> <http://www.w3.org/2002/07/owl#sameAs> ?same } ''' % GRAPH)
        same = res.next()[0]
        assert 'http://dbtune.org/myspace/kurtisrandom' == same, 'wrong sameAs result: ' +str(same)
        self.connect.commit() 
        #cursor.close()
        
        
    def tearDown(self):
        self.connect.execute('SPARQL CLEAR GRAPH <%s>' % GRAPH)
        self.connect.close() 
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_insert_sparql']
    unittest.main()