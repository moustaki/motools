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

class NonArtistTest(unittest.TestCase):


    def setUp(self):
        self.short_url_non = 'flexboogie'
        self.uid_non = '8840037'
        
        # basic page getting
        self.M = MyspaceScrape(uid = self.uid_non)
        self.M.get_page()
        self.M.get_uid()
        self.M.is_artist()


    def test_get_nice_url(self):
        url = self.M.get_nice_url_non_artist()
        assert url == 'flexboogie', 'clean url is wrong: '+str(url)
    
    def test_get_stats_non_artist(self):
        self.M.get_stats_non_artist()
        self.M.serialize()
        graph = mopy.exportRDFGraph(self.M.mi)
        for row in graph.query('''SELECT ?age where { ?x <http://purl.org/ontology/myspace#age> ?age } '''):
            age = row[0]
            print age
        assert int(age)==100, 'wrong age ' + str(age)
        for row in graph.query('''SELECT ?gender where { ?x <http://xmlns.com/foaf/0.1/gender> ?gender . } '''):
            gender = row[0]
        assert gender == 'male' , 'wrong gender '+ str(gender)
        for row in graph.query('''SELECT ?loc ?reg ?co where { ?x <http://purl.org/ontology/myspace#locality> ?loc . ?x <http://purl.org/ontology/myspace#region> ?reg . ?x <http://purl.org/ontology/myspace#country> ?co . } '''):
            loc = row[0]
            #print loc
            reg=row[1]
            #print reg
            co = row[2]
            #print co
        assert loc == 'SAINT LOUIS' , 'wrong locality '+str(loc)
        assert reg == 'Missouri' , 'wrong region '+str(reg)
        assert co == 'US' , 'wrong country '+str(co)
        for row in graph.query('SELECT ?totf where { ?x <http://purl.org/ontology/myspace#totalFriends> ?totf } '):
            totf = row[0]
        assert int(totf)>2000 , 'wrong number of friends '+str(totf)

    def test_get_image_non_artist(self):
        img = self.M.get_image_non_artist()
        # just check it looks vaguely like an image url
        assert img.startswith('http://') and (img.endswith('.jpg') or img.endswith('.gif')), 'does not look like an image url: '+str(img)

    def test_get_friends(self):
        self.M.get_friends_non_artist()
        self.M.serialize()
        graph = mopy.exportRDFGraph(self.M.mi)
        friends = []
        for row in graph.query('''SELECT ?friends WHERE { ?s <http://purl.org/ontology/myspace#topFriend> ?friends } '''):
            friend = '%s' % row
            friends.append(friend)
        assert len(friends)>4 , 'too few friends found - some kind of problem in .get_friends_non_artist()'


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()