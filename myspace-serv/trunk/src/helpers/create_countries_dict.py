#!/usr/bin/python
'''
create a dict object from the list of countries myspace uses
such that
    key = myspace country text
    value = geonames uri for country
'''
from urllib2 import urlopen, quote
from xml.dom import minidom
import cPickle as pickle

GEO_WS = 'http://ws.geonames.org/search?'
GEO_URI_BASE = 'http://sws.geonames.org/'

def main():
    # open the list of countries
    f = open('list_of_countries.txt', 'r')
    countries = f.readlines()
    f.close()
    # remove annoying newline char
    for idx, country in enumerate(countries):
        countries[idx] = country[:-1]

    error_list = []
    master_dict = {}
    for country in countries:
        resp = urlopen(GEO_WS+'q=%s&maxRows=1' % quote(country))
        xml = resp.read()
        print 'processing country: '+country
        resp.close()
        xmld = minidom.parseString(xml)
        # minidom failing like fuck here
        try:
            fuck = xmld.getElementsByTagName('geonameId')[0].toxml()
        except IndexError:
            print 'error of country: '+country
            error_list.append(country)
        else:
            geoId = fuck.strip('<geonameId></')
            master_dict[country]=GEO_URI_BASE+geoId+'/'


    f = open('countries','w')
    pickle.dump(master_dict, f)
    f.close()
    print master_dict
    print error_list





if __name__ == '__main__':
    main()