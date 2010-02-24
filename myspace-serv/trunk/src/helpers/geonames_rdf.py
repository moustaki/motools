#!/usr/bin/env python
# encoding: utf-8
'''
grab all the geo-names rdf and add to repo

Created on Feb 24, 2010

@author: kurtjx
'''

from rdflib import ConjunctiveGraph
import cPickle as pickle


f = open('./countries', 'r')
COUNTRIES = pickle.load(f)
f.close()


def get_rdf():
    rdf = ConjunctiveGraph()
    for key in COUNTRIES.keys():
        print 'parsing %s'%COUNTRIES[key]
        rdf.parse(COUNTRIES[key])
    print 'serialize'
    rdf.serialize('countries.rdf')


if __name__ == "__main__":
    get_rdf()
