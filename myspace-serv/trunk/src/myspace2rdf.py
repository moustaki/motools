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
#from xml.dom import minidom

from BeautifulSoup import BeautifulSoup as BS


class MyspaceException(Exception):
    def __init__(self, msg):
        self.msg = msg

class Myspace(object):
    '''
    classdocs
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
        
    def get_friends(self):
        ''' get list of top friends '''
        #friendTupleList = scrapePageTuple(self.html, friendDict)
        friendUIDs = scrapePageWhile(self.html, uris.friendTag[0], uris.friendTag[1])
        friendNames = scrapePageWhile(self.html, uris.friendNameTag[0], uris.friendNameTag[1])
        friendPics = scrapePageWhile(self.html, uris.friendPicTag[0], uris.friendPicTag[1])
            
        # TODO fix this horrible hack - for non-artists, they appear here as well
        if len(friendUIDs) != len(friendNames):
            friendUIDs = friendUIDs[1:]

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
                    
    def get_image(self):
        imageURL = scrapePage(self.html, [uris.picTag[0]+str(self.uid)+'''"><img src="'''], uris.picTag[1])
        img = mopy.foaf.Image(imageURL)
        self.subject.depiction.add(img)
        self.mi.add(img)
        return imageURL
    
    def get_image_non_artist(self):
        ''' find the photo for a non-artist account'''
        image_url = self.soup.find('img', 'photo ').get('src')
        img = mopy.foaf.Image(image_url)
        self.subject.depiction.add(img)
        self.mi.add(img)
        return image_url