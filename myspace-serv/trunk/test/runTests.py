#!/usr/bin/env python
# encoding: utf-8
"""

Created by kurtjx on 1 Feb 2010

copyright notice to go here
"""
from unittest import TestSuite, TextTestRunner, TestLoader
import sys
sys.path.append("../src")

from artistTest import ArtistTest
from commonTest import CommonTest
from getSongsTest import GetSongsTest
from nonArtistTest import NonArtistTest
from insertSparqlTest import InsertSparqlTest


def runTests():
    suite = TestSuite()
    suite.addTest(TestLoader().loadTestsFromTestCase(ArtistTest))
    suite.addTest(TestLoader().loadTestsFromTestCase(CommonTest))
    suite.addTest(TestLoader().loadTestsFromTestCase(GetSongsTest))
    suite.addTest(TestLoader().loadTestsFromTestCase(NonArtistTest))
    suite.addTest(TestLoader().loadTestsFromTestCase(InsertSparqlTest))
    #suite.addTests([ArtistTest(), CommonTest(), GetSongsTest(), NonArtistTest(), InsertSparqlTest()])
    TextTestRunner(verbosity=2).run(suite)
    #unittest.main()


def main(argv=None):
    runTests()


if __name__ == "__main__":
    sys.exit(main())