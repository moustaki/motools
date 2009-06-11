'''
Created on Jun 10, 2009

@author: kurtjx
'''
import unittest
import os
# change to src directory
os.chdir('../src')
from myspace2rdf import Myspace


class Test(unittest.TestCase):


    def setUp(self):
        self.short_url_artist = 'kurtisrandom'
        self.short_url_non = 'flexboogie'
        self.uid_non = '8840037'
        self.uid_artist = '30650288'


    def tearDown(self):
        pass
    
    def test_get_image(self):
        M = Myspace(short_url=self.short_url_artist)
        M.get_page()
        M.get_uid()
        M.is_artist()
        print M.get_image()
        M = Myspace(uid=self.uid_non)
        M.get_page()
        M.get_uid()
        M.is_artist()
        print M.get_image()
        
    
    def test_get_uid(self):
        M = Myspace(short_url=self.short_url_artist)
        M.get_page()
        M.get_uid()
        assert M.uid == self.uid_artist, 'uid mismatch, got '+str(M.uid)+ ' expected ' +str(self.uid_artist)
        
    def test_is_artist(self):
        M = Myspace(short_url=self.short_url_artist)
        M.get_page()
        M.get_uid()
        assert M.is_artist(), 'should be an artist'
        M = Myspace(uid=self.uid_non)
        M.get_page()
        M.get_uid()
        M.is_artist()
        assert M.name == '''Flex Boogie  (Flex Boogie For Real)'''
        
    def test_get_genres(self):
        M = Myspace(short_url=self.short_url_artist)
        M.get_page()
        M.get_uid()
        M.is_artist()
        genres = M.get_genres()
        gnames = []
        for genre in genres:
            gnames.append(genre.name.pop())
        gnames.sort()
        assert gnames == ['Experimental', 'Hip Hop', 'R&B'], 'wrong genre names ' +str(gnames)
        
        
    def test_get_friends(self):
        M = Myspace(short_url=self.short_url_artist)
        M.get_page()
        M.get_uid()
        M.is_artist()
        M.get_friends()
        print M.mi.MainIdx
        # TODO: make into real test for friends

    def test_get_page(self):
        S = Myspace(short_url=self.short_url_artist)
        S.get_page()
        assert len(S.html) > 1, 'error page is too short when using name-based url'
        # speed up testing comment this out
        #S = Myspace(uid=self.uid_non)
        #S.get_page()
        #assert len(S.html) > 1, 'error page is too short when using uid'


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_get_page']
    unittest.main()