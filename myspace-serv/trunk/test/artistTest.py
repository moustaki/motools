'''
Created on Jun 11, 2009

@author: kurtjx
'''
import unittest
import os
# change to src directory
os.chdir('../src')
from myspace2rdf import MyspaceScrape
import mopy
from rdflib import ConjunctiveGraph

class ArtistTest(unittest.TestCase):


    def setUp(self):
        self.short_url_artist = 'kurtisrandom'
        self.uid_artist = '30650288'
        self.M = MyspaceScrape(uid=self.uid_artist)
        self.M.get_page()
        self.M.get_uid()
        self.M.is_artist()

    def test_get_nice_url(self):
        url = self.M.get_nice_url()
        assert url == 'kurtisrandom', 'clean url is wrong: '+str(url)

    def test_get_image(self):
        img = self.M.get_image()
        # just check it looks vaguely like an image url
        assert img.startswith('http://') and img.endswith('.jpg'), 'does not look like an image url: '+str(img)

    def test_get_genres(self):
        genres = self.M.get_genres()
        gnames = []
        for genre in genres:
            gnames.append(genre.name.pop())
        gnames.sort()
        assert gnames == ['Experimental', 'Hip Hop', 'R&B'], 'wrong genre names ' +str(gnames)

    def test_get_friends(self):
        self.M.get_friends()
        self.M.serialize()
        graph = self.M.graph
        friends=[]
        for row in graph.query('''SELECT ?friends WHERE { ?s <http://purl.org/ontology/myspace#topFriend> ?friends } '''):
            friend = '%s' % row
            friends.append(friend)
        friends.sort()
        assert friends == [u'http://dbtune.org/myspace/7shotscreamers', u'http://dbtune.org/myspace/Dawit7', u'http://dbtune.org/myspace/dbaad', u'http://dbtune.org/myspace/dbirghenthal', u'http://dbtune.org/myspace/djthumpasaurus', u'http://dbtune.org/myspace/duplicateband', u'http://dbtune.org/myspace/flexboogie', u'http://dbtune.org/myspace/fliplynch', u'http://dbtune.org/myspace/serpientesmsn', u'http://dbtune.org/myspace/speedballband', u'http://dbtune.org/myspace/thelegendjamesbrown', u'http://dbtune.org/myspace/uid/30642042'] , 'wrong friends list '+str(friends)

    def test_get_stats(self):
        self.M.get_stats()
        self.M.serialize()
        graph = self.M.graph
        #graph = mopy.exportRDFGraph(self.M.mi)

        # raw country and city text
        tCountry = 'United Kingdom'
        tCity = 'London,'
        for row in graph.query('''SELECT ?loc ?co where { ?x <http://purl.org/ontology/myspace#locality> ?loc . ?x <http://purl.org/ontology/myspace#country> ?co . } '''):
            loc = row[0]
            #print loc
            co = row[1]
            #print co
        assert loc == 'London' , 'wrong locality '+ str(loc)
        assert co == 'United Kingdom' , 'wrong country '+ str(co)

        # check based near
        for row in graph.query('''select ?based where { ?x <http://xmlns.com/foaf/0.1/based_near> ?based } '''):
            based = row[0]
        assert str(based) == 'http://sws.geonames.org/2635167/', 'wrong based_near: '+ str(based)

        # total friends count
        totf = -1
        for row in graph.query('SELECT ?totf where { ?x <http://purl.org/ontology/myspace#totalFriends> ?totf } '):
            totf = row[0]
        assert int(totf)>190 , 'wrong number of total friends '+str(totf)

        views = -1
        for row in graph.query('SELECT ?views WHERE { ?x <http://purl.org/ontology/myspace#profileViews> ?views } '):
            views = row[0]
        assert views != -1 , 'faild to get profile views: ' + str(views)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()