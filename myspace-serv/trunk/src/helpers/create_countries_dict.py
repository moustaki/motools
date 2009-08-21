#!/usr/bin/python
'''
create a dict object from the list of countries myspace uses
such that
    key = myspace country text
    value = geonames uri for country

store in a pickle to be used by myspace2rdf.py
'''
from urllib2 import urlopen, quote
from xml.dom import minidom
import cPickle as pickle

GEO_WS = 'http://ws.geonames.org/search?'
GEO_URI_BASE = 'http://sws.geonames.org/'

def queryGeonames(country):
    resp = urlopen(GEO_WS+'q=%s&maxRows=1' % quote(country))
    xml = resp.read()
    resp.close()
    xmld = minidom.parseString(xml)
    try:
        fuck = xmld.getElementsByTagName('geonameId')[0].toxml()
    except IndexError:
        print 'error of country: '+country
        return None
    else:
        geoId = fuck.strip('<geonameId></')
        return geoId

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

        print 'processing country: '+country

        geoId = queryGeonames(country)
        # minidom failing like fuck here
        if geoId != None:
            master_dict[country]=GEO_URI_BASE+geoId+'/'
        else:
            error_list.append(country)

    for err in error_list:
        if err.find('('):
            country = err.split('(')[0]
            print "trying %s as %s" % (err, country)
            geoId = queryGeonames(country)
            if geoId != None:
                master_dict[err] = GEO_URI_BASE + geoId+'/'
                error_list.pop(error_list.index(err))


    # fixing errors by hand
    master_dict['Cocoa (Keeling) Islands'] = GEO_URI_BASE+'1547356/'
    master_dict['United ArabEmirates'] = GEO_URI_BASE+'290557/'
    master_dict['Former Yugoslavia'] = GEO_URI_BASE +'3277605/' # set to bosnia
    master_dict['Syrian ArabRepublic'] = GEO_URI_BASE+'163843/'
    master_dict['Cote Divoire'] = GEO_URI_BASE+'2287781/' #ivory coast
    master_dict['Korea,  Democratic Peoples Republic of'] = GEO_URI_BASE + '1835841/'
    master_dict['Korea, Republic of'] = GEO_URI_BASE + '1835841/'
    master_dict['Virgin Islands (British)'] = GEO_URI_BASE + '3577718/'
    master_dict['DoDDs Schools'] = GEO_URI_BASE + '6252001/' #just say us

    f = open('countries','w')
    pickle.dump(master_dict, f)
    f.close()
    print master_dict
    print error_list
    print len(error_list)





if __name__ == '__main__':
    main()