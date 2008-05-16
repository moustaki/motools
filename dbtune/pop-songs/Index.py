import urllib
import sys
from BeautifulSoup import BeautifulSoup

url = 'http://chordtranscriptions.net/popsongs/'

f = urllib.urlopen(url)
html = f.read()
f.close()
soup = BeautifulSoup(html)

o = open('index.ttl','w')
o.write('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.\n\n')

for link in soup('a') :
	o.write('<> rdfs:seeAlso <')
	o.write(url)
	o.write(link.attrs[0][1])
	o.write('>.\n')

o.close()

