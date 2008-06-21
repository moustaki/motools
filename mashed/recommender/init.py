#!/usr/bin/env python

from rdflib import Graph,ConjunctiveGraph, Namespace
from rdflib.store import Store
from sys import argv
from rdflib import plugin
import sys

store = plugin.get('SQLite',Store)('rdfstore')
rt = store.open('db',create=True)

g = Graph(store)

g.load("brands_artist.n3",format='n3')

g.commit()


