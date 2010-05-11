#! /bin/bash

# Generate the RDF/XML from the Turtle code

rapper -I "http://purl.org/NET/c4dm/event.owl#" -i turtle -o rdfxml-abbrev event.n3 > event.rdf


