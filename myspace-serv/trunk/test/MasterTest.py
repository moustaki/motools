'''
Created on Jun 11, 2009

@author: kurtjx
'''
import unittest
import os
# change to src directory
os.chdir('../src')
from myspace.myspace2rdf import Myspace


class MasterTest(unittest.TestCase):

    def setUp(self):
        self.short_url_artist = 'kurtisrandom'
        self.uid_artist = '30650288'
        
        self.Artist = Myspace(short_url=self.short_url_artist)
        

    def testRun(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()