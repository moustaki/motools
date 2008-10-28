#! /bin/bash

# Generate the RDF/XML from the Turtle code

rapper -I "http://purl.org/ontology/event-notes" -i turtle -o rdfxml-abbrev event-notes.n3 > event-notes.rdf


