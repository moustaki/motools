'''
Created on Jun 17, 2009

@author: kurtjx
'''
import unittest
import os
# change to src directory
os.chdir('../src')
from sparql4myspace import SparqlSpace
import pyodbc
from ODBC import ODBC
import time
import sys
VODBC = ODBC()
# must reset this graph value
# do so CAREFULLY - you will CLEAR all data in graph by running test
GRAPH = "changeme"

class Sparql4MyspaceTest(unittest.TestCase):


    def setUp(self):
        self.connect = VODBC.connect()
        self.connect.execute('SPARQL CLEAR GRAPH <%s>' % GRAPH) 
        self.uri = 'http://dbtune.org/myspace/uid/30650288'
        self.connect.execute('SPARQL LOAD <%s.rdf> into <%s>' % (self.uri,GRAPH))
        self.connect.execute('SPARQL INSERT in graph <%s> {<%s> <http://purl.org/dc/terms/modified> "%s"^^xsd:dateTime}' % (GRAPH ,self.uri , time.strftime('%Y-%m-%dT%H:%M:%S')))
        self.old_date = '2009-03-17T14:27:59+01:00'
        self.connect.execute('SPARQL INSERT in graph <%s> {<%s> <http://purl.org/dc/terms/modified> "2009-03-17T14:27:59+01:00"^^xsd:dateTime}' % (GRAPH ,self.uri))
        



    def tearDown(self):
        self.connect.commit()
        self.connect.close()
        
    def test__still_fresh__(self):
        d = '2009-03-17T14:27:59+01:00'
        ss = SparqlSpace(self.uri, self.connect)
        assert not ss.__still_fresh__(d), 'this date should not be fresh'


    def test_select(self):
        uri = self.uri
        cursor = self.connect.cursor()
        ss = SparqlSpace(uri, cursor)
        assert ss.select(GRAPH), 'this uri should be present: '+str(uri)
        ss = SparqlSpace('http://junk.uri', cursor)
        assert not ss.select(GRAPH), 'this uri should not be present: http://junk.uri'
        cursor.close()
        
    def test_make_graph(self):
        cursor = self.connect.cursor()
        ss = SparqlSpace(self.uri, cursor)
        ss.select(GRAPH)
        print ss.make_graph()
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()