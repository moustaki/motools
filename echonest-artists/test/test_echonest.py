'''
Created on Jul 21, 2010

@author: kurtjx
'''
import unittest
import sys
sys.path.append('../src')
import echonest

JB_MBID = '20ff3303-4fe2-4a47-a1b6-291e26aa3438'
JOSE_MBID = '481c8894-c898-4332-8882-db5a90c318e1'

class ENTest(unittest.TestCase):


    def test_get_similar(self):
        model = echonest.get_similar(JB_MBID)
        print len(model)
        model = echonest.get_similar(JOSE_MBID)
        print len(model)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()