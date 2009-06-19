'''
Created on Jun 10, 2009

@author: kurtjx
'''

import myspaceuris as uris
from tryurl import try_open
#from rdflib import ConjunctiveGraph, URIRef
from scraping import scrapePage, scrapePageWhile
import mopy
import re
from urllib2 import quote
from xml.dom import minidom
import os
from BeautifulSoup import BeautifulSoup as BS
from ConfigParser import ConfigParser, Error
import time


config = ConfigParser()
try:
    config.read('config')
except:
    print 'error, no config file\n  exting...'
    sys.exit(1)

USE_SPARQL = config.get('ODBC', 'sparql') 
#change to a blank string for local testing, no trailing '/'
URL_BASE = config.get('urls', 'base')[1:-1] #"http://dbtune.org/myspace"
GRAPH = config.get('ODBC', 'graph')[1:-1]
WRITE_PATH = config.get('ODBC', 'write_path')[1:-1]

class MyspaceException(Exception):
    def __init__(self, msg):
        self.msg = msg

class MyspaceScrape(object):
    '''
    Class for scpraping a myspace.com page
    '''


    def __init__(self, short_url=None, uid=None):
        '''
        Constructor
        '''
        self.mi = mopy.MusicInfo()
        #self.rdf_graph = ConjunctiveGraph()
        if short_url != None:
            self.url = uris.www_myspace + short_url
        elif uid != None:
            self.url = uris.viewProfileURLbase + str(uid)
        else:
            raise MyspaceException, 'neither short_url or uid provided'
    
    def run(self):
        self.get_page()
        self.get_uid()
        artist = self.is_artist()
        if artist:
            self.get_nice_url()
            self.get_friends()
            self.get_image()
            self.get_songs()
            self.get_stats()
        else:
            self.get_nice_url_non_artist()
            self.get_friends_non_artist()
            self.get_image_non_artist()
            self.get_stats_non_artist()
    
    def get_page(self):
        if self.url != None:
            resp = try_open(self.url, try_num=0, limit=3)
            if resp==None:
                raise MyspaceException, 'failed to open url '+str(self.url)
            self.html = resp.read()
            self.soup = BS(self.html)
            resp.close()
        else:
            self.html = None
    
    def get_uid(self):
        ''' get the uid from the html '''
        self.uid = scrapePage(self.html, [uris.userIDTag[0]], uris.userIDTag[1])
        
    def is_artist(self):
        '''do artist check, assign a self.subject (Person or MusicArtist) and return True or False'''
        genrePresent = scrapePage(self.html, [uris.genreTag[0]], uris.genreTag[1])
        if genrePresent:
            self.subject = mopy.mo.MusicArtist(uris.dbtune+'uid/'+str(self.uid))
            # add foaf:primaryTopic
            ppd = mopy.foaf.PersonalProfileDocument("")
            ppd.primaryTopic.set(self.subject)
            self.mi.add(ppd)
            # assuming the 'name' tag must be present, if not it's a bad url
            self.name = scrapePage(self.html, [uris.nameTag[0]], uris.nameTag[1])
            if self.name:
                self.subject.name.set(self.name)
            else:
                raise MyspaceException, "seems to be an invalid - could not find foaf:name"
            return True
        else:
            self.subject = mopy.foaf.Person(uris.dbtune+'uid/'+str(self.uid))
            # add foaf:primaryTopic
            ppd = mopy.foaf.PersonalProfileDocument("")
            ppd.primaryTopic.set(self.subject)
            self.mi.add(ppd)
            self.name = self.soup.title.string.strip('\r').strip('\t').strip('\n').split(uris.non_artist_name_split)[0].strip()
            #print self.name
            if self.name:
                self.subject.name.set(self.name)
            else:
                raise MyspaceException, "seems to be an invalid - could not find foaf:name"
            return False
    
    def get_friends_non_artist(self):
        results = self.soup.findAll('span', 'msProfileLink')
        for r in results:
            # clever BSoup stuff for finding friends, only in non-artist this works as of 11/06/09
            f = mopy.foaf.Person(uris.dbtune+r.next.get('href').split(uris.www_myspace)[1])
            f.name.set(unicode(r.next.get('title')))
            img = mopy.foaf.Image(r.next.next.next.next.get('src'))
            f.depiction.add(img)
            
            self.subject.topFriend.add(f)
            self.mi.add(f)
        
        
    def get_friends(self):
        ''' get list of top friends '''
        #friendTupleList = scrapePageTuple(self.html, friendDict)
        friendUIDs = scrapePageWhile(self.html, uris.friendTag[0], uris.friendTag[1])
        friendNames = scrapePageWhile(self.html, uris.friendNameTag[0], uris.friendNameTag[1])
        friendPics = scrapePageWhile(self.html, uris.friendPicTag[0], uris.friendPicTag[1])
            
        # TODO fix this horrible hack - for non-artists, they appear here as well
        #if len(friendUIDs) != len(friendNames):
        #    friendUIDs = friendUIDs[1:]

        for i in range(len(friendUIDs)):
            currentUID = friendUIDs[i]
            if currentUID.isdigit():
                friend = mopy.foaf.Person(uris.dbtune+'uid/' + str(friendUIDs[i]))
            else:
                friend = mopy.foaf.Person(uris.dbtune+str(friendUIDs[i]))
            friend.name.set(friendNames[i])
            try:
                img = mopy.foaf.Image(friendPics[i])
                friend.depiction.add(img)
            except:
                pass

            
            #self.subject.knows.add(friend)
            
            # self.subject.knows.add(friend)
            # since when did this happen??? mopy wont take foaf:knows as a prop of mo:MusicArtist
                
            self.subject.topFriend.add(friend)
            self.mi.add(friend)
        
    def get_genres(self):
        '''get the genres for an artist'''
        localGenres = scrapePage(self.html, [uris.genreTag[0]], uris.genreTag[1])
        if localGenres == None:
            return None
        genreNums = re.findall(''':"([0-9]+)"''', localGenres) # should return only 2 or 3 char string between 
        genres = []
        for gnum in genreNums:
            try:
                genre = mopy.mo.Genre(uris.myspaceOntology+quote(uris.genreDict[int(gnum)]))
            except KeyError:
                pass
            else:
                genre.name.set(uris.genreDict[int(gnum)])
                self.mi.add(genre)
                self.subject.genreTag.add(genre)
                genres.append(genre)
        
        return genres
    
    def get_image_non_artist(self):
        try:
            imageURL = self.soup.find('img', 'photo ').get('src')
        except:
            imageURL = None
        else:
            img = mopy.foaf.Image(imageURL)
            self.subject.depiction.add(img)
            self.mi.add(img)
        return imageURL
    
    def get_stats(self):
        mess = scrapePage(self.html, [uris.cityTag[0]], uris.cityTag[2])
        if mess != None:
            locality = mess.split(uris.cityTag[1])[0]
            country = mess.split(uris.cityTag[1])[1]
            self.subject.country.set(str(unicode(country).encode('utf-8')))
            self.subject.locality.set(str(unicode(locality).encode('utf-8')))
        profile_views = scrapePage(self.html, [uris.profileViews[0]], uris.profileViews[1])
        if profile_views != None:
            self.subject.profileViews.set(int(profile_views))
        try:
            totfri = self.soup.find(property="myspace:friendCount").string
        except AttributeError, err:
            totfri = '0'
        else:
            self.subject.totalFriends.set(int(totfri))
    
    def get_stats_non_artist(self):
        try:
            gender = self.soup.find('span', 'gender').string
        except AttributeError, err:
            pass
        else:
            self.subject.gender.set(str(gender).lower())
        try:
            country = self.soup.find('span', 'country-name').string
        except AttributeError, err:
            pass
        else:
            self.subject.country.set(str(unicode(country).encode('utf-8')))
        try:
            locality = self.soup.find('span', 'locality').string
        except AttributeError, err:
            pass
        else:
            self.subject.locality.set(str(unicode(locality).encode('utf-8')))
        try:
            region = self.soup.find('span', 'region').string
        except AttributeError, err:
            pass
        else:
            self.subject.region.set(str(region).encode('utf-8'))
        try:
            age = self.soup.find('span', 'age').string
        except AttributeError, err:
            pass
        else:
            try:
                self.subject.age.set(int(age))
            except ValueError:
                pass # probably means age set to private
        try:
            totfri = self.soup.find('span','count').string
        except AttributeError, err:
            pass
        else:
            self.subject.totalFriends.set(int(totfri))
            
                    
    def get_image(self):
        imageURL = scrapePage(self.html, [uris.picTag[0]+str(self.uid)+'''"><img src="'''], uris.picTag[1])
        if imageURL != None:
            img = mopy.foaf.Image(imageURL)
            self.subject.depiction.add(img)
            self.mi.add(img)
        return imageURL
    
    def get_nice_url(self):
        niceURL = scrapePage(self.html, [uris.niceURLTag[0]], uris.niceURLTag[1])
        if niceURL:
            niceURL = niceURL.rsplit(uris.www_myspace)[1]
            thing = mopy.owl.Thing(uris.dbtune+niceURL)
            self.subject.sameAs.set(thing)
            self.mi.add(thing)
        return niceURL
    
    def get_nice_url_non_artist(self):
        url = None
        try:
            url = self.soup.find('a', 'url').get('href')
        except AttributeError, err:
            url = ''
        else:
            url = url.rsplit(uris.www_myspace)[1]
            thing = mopy.owl.Thing(uris.dbtune+url)
            self.subject.sameAs.set(thing)
            self.mi.add(thing)
        return url
                
    
    def get_songs(self):
        ''' do some tricky stuff to get the songs of an artist account '''
        if self.__get_artist_id() and self.__get_playlist_id():
            xml_page = try_open(uris.mediaBase[0] + str(self.artistID) + uris.mediaBase[1] + str(self.playlistID) + uris.mediaBase[2] + str(self.uid) + uris.mediaBase[3])
            
            if xml_page:
                xml = xml_page.read()
                #print xml
                xml_struct = minidom.parseString(xml)
                song_list = xml_struct.getElementsByTagName('song')
                xml_page.close()
                for song in song_list:
                    # trickery to get the songs - one http request for each song :-/
                    song_plays = song.getElementsByTagName('stats')[0].getAttribute('plays')
                    songID = song.getAttribute('songId')
                    resp = try_open(uris.songBase[0] + str(songID) + uris.songBase[1])
                    this_xml = minidom.parseString(resp.read())
                    # add to mopy rdf
                    track = mopy.mo.Track(os.path.join(uris.dbtune, 'uid',self.uid+'.rdf#'+songID))
                    try:
                        track.plays.set(int(song_plays))
                    except ValueError:
                        pass # sometimes we get empty string '' which throws ValueError
                    try:
                        song_title = this_xml.getElementsByTagName('title')[0].firstChild.nodeValue
                    except AttributeError:
                        pass
                    else:
                        track.title.set(song_title)
                    try:
                        song_image = this_xml.getElementsByTagName('small')[0].firstChild.nodeValue
                    except AttributeError:
                        pass
                    else:
                        img = mopy.foaf.Image(song_image)
                        track.depiction.set(img)
                    try:
                        song_avas = this_xml.getElementsByTagName('rtmp')[0].firstChild.nodeValue
                    except AttributeError:
                        pass
                    else:
                        avas = mopy.mo.MusicalItem(song_avas)
                        track.available_as.set(avas)
                        self.mi.add(avas)
                    self.subject.made.add(track)
                    self.mi.add(track)
    
    def __get_artist_id(self):
        '''attempt to find via scrape of page the internal artist number.'''
        ids = scrapePageWhile(self.html, uris.artistIDtag[0], uris.artistIDtag[1])
        for i in ids:
            if i.isdigit():
                self.artistID = i
                return True
        return False
    
    def __get_playlist_id(self):
        """attempts to find via scrape of the internal identifier of an artist's playlist of songs"""
        # make sure we get a digit and not some crap - maybe should to regex
        ids = scrapePageWhile(self.html, uris.playlistIDtag[0], uris.playlistIDtag[1])
        for i in ids:
            if i.isdigit():
                self.playlistID = i
                return True
        return False
    
    def insert_sparql(self, cursor, graph=GRAPH):
        '''DB.DBA.RDF_LOAD_RDFXML (file_to_string ('/usr/local/virtuoso-opensource/var/lib/virtuoso/db/vc-db-1.rdf'), '', 'http://mygraph.com');'''
        self.mi.add(self.subject)
        fname = str(self.uid)+'.rdf'
        #print 'writing file'
        fname = os.path.join(WRITE_PATH, fname)
        mopy.exportRDFFile(self.mi, fname)
        # do odbc insert, cp caching should make this cool right?
        q = "DB.DBA.RDF_LOAD_RDFXML_MT (file_to_string('"+ fname+"'), 'junk', '"+graph+"')"
        #print q
        cursor.execute(q)
        # assign a time stamp here
        q = '''SPARQL define sql:log-enable 2 INSERT in graph <'''+graph+'''> {<%s> <http://purl.org/dc/terms/modified> "%s"^^xsd:dateTime}'''
        uri = os.path.join(uris.dbtune,'uid/', str(self.uid))
        tstamp = time.strftime('%Y-%m-%dT%H:%M:%S')
        q = q % (uri, tstamp)
        #print q
        cursor.execute(q)
        #cursor.commit()
        os.remove(fname)
    
    def serialize(self):
        self.mi.add(self.subject)
        graph = mopy.exportRDFGraph(self.mi)
        return graph.serialize()
        
