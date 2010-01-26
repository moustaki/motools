#!/usr/bin/env python
"""
create_based_near_rdf.py
    query the endpoint for people/artists and countries and
    write some rdf files with foaf:based_near for countries

    @author: kurtjx
    @contact: kurtjx at gmail
"""

from SPARQLWrapper import SPARQLWrapper2
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed, EndPointNotFound
import sys
import logging
from logging import debug, error, info
from rdflib import ConjunctiveGraph, Namespace, URIRef
import cPickle as pickle
import os

f = open('./countries', 'r')
COUNTRIES = pickle.load(f)
f.close()
FOAF = Namespace('http://xmlns.com/foaf/0.1/')

WRITE_PATH = '/Users/kurtjx/c4dm/based_near/'

def get_based_near(limit=500, offset=0):
    debug('''getting list with limit %s and offset %s''' % (str(limit), str(offset)))
    sparql = SPARQLWrapper2('http://virtuoso.dbtune.org/sparql', 'http://dbtune.org/myspace/')
    query = '''
                SELECT DISTINCT ?per ?coun WHERE {

                 ?per a <http://purl.org/ontology/mo/MusicArtist> .
                ?per <http://purl.org/ontology/myspace#country> ?coun . }
                limit %s offset %s
            ''' % (limit, offset)
    sparql.setQuery(query)
    try:
        ret = sparql.query()
    except QueryBadFormed, err:
        error(err)
        sys.exit(1)
    except EndPointNotFound, err:
        error(err)
        sys.exit(1)

    debug('query done')
    if len(ret.bindings)==0:
        info('''empty sparql result, assuming we're done :-)''')
        sys.exit(0)
    graph = ConjunctiveGraph()
    for binding in ret.bindings:
        person = binding['per'].value
        country = binding['coun'].value

        try:
            graph.add((URIRef(person), FOAF['based_near'], URIRef(COUNTRIES[country])))
        except KeyError, err:
            error(err)

    fname = 'offset-%s.rdf' % str(offset)
    fname = os.path.join(WRITE_PATH, fname)
    debug('writing file %s' % fname)
    graph.serialize(fname)



def setLogger():
    '''just set the logger'''
    loggingConfig = {"format":'%(asctime)s %(levelname)-8s %(message)s',
                               "datefmt":'%d.%m.%y %H:%M:%S',
                                "level": logging.DEBUG,
                                #"filename":logPath + "based_near.log",
                                "filemode":"w"}
    logging.basicConfig(**loggingConfig)


def main():
    limit = 500
    offset = 152000 #0
    setLogger()
    while(True):
        get_based_near(limit, offset)
        offset += limit


if __name__ == '__main__':
    main()
