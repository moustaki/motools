#!/usr/bin/python
import csv
import sys

list = []

f = open("brands_artists/brands_artists.txt","rb")
parser = csv.reader(f,delimiter=' ')

rdf = open("brands_artist.n3","w")

for line in parser:
	brand = line[0]
	for k in range(1,len(line)/2):
		artist = line[2*k-1]
		playcount = (line[2*k].split(','))[0]
		rdf_line = "<http://bbc-programmes.dyndns.org/programmes/"+brand+"> "+"<http://purl.org/ontology/playcount/playcount> [<http://purl.org/ontology/playcount/count> \""+playcount+"\"; <http://purl.org/ontology/playcount/object> <http://dbtune.org/musicbrainz/resource/artist/"+artist+">].\n"
		rdf.write(rdf_line)
		
f.close()

