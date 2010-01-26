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

class CommonTest(unittest.TestCase):


    def setUp(self):
        self.short_url_artist = 'kurtisrandom'
        self.uid_artist = '30650288'
        self.A = MyspaceScrape(uid=self.uid_artist)
        self.A.get_page()
        
        self.short_url_non = 'flexboogie'
        self.uid_non = '8840037'
        # basic page getting
        self.M = MyspaceScrape(uid = self.uid_non)
        self.M.get_page()




    def test_get_uid(self):
        self.M.get_uid()
        assert self.M.uid == self.uid_non, 'uid mismatch, got '+str(M.uid)+ ' expected ' +str(self.uid_artist)
        self.A.get_uid()
        assert self.A.uid == self.uid_artist, 'uid mismatch, got '+str(M.uid)+ ' expected ' +str(self.uid_artist)
        
    def test_is_artist(self):
        self.A.get_uid()
        assert self.A.is_artist(), 'should be an artist'
        self.M.get_uid()
        assert not self.M.is_artist(), 'Flex Boogie is not an artist'
        assert self.M.name == '''Flex Boogie  (Flex Boogie For Real)''', 'wrong name: ' +str(self.M.name)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()