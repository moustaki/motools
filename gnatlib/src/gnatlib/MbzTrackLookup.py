"""
  Perform a track lookup on the Musicbrainz database, using
  embedded ID3 tags or manually supplied metadata

    Copyright (C) 2009  Yves Raimond, Kurt Jacobson

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>

  Yves Raimond, C4DM, Queen Mary, University of London
  yves.raimond (at) elec.qmul.ac.uk
  kurt.jacobson (at) elec.qmul.ac.uk
"""

from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.apev2 import APEv2
from mutagen.mp3 import MP3
from mutagen.asf import ASF
from mutagen.mp4 import MP4
from mutagen.musepack import Musepack
from mutagen.oggvorbis import OggVorbis
from mutagen.oggflac import OggFLAC
from mutagen.oggtheora import OggTheora
from mutagen.trueaudio import TrueAudio
from mutagen.wavpack import WavPack
from MbzURIConverter import *
from CachedMBZQuery import *
from musicbrainz2.webservice import ResponseError, ConnectionError, WebServiceError, Query
import musicbrainz2.webservice as ws
import sys
import logging
from logging import log, error, warning, info, debug
import re

DBTUNE_URI='http://dbtune.org/musicbrainz/resource'

class MbzLookupException :

    def __init__(self,message) :
        self.message = message

    def __str__(self) :
        return self.message

class FileTypeException :

    def __init__(self,message) :
        self.message = message

    def __str__(self) :
        return self.message

class MbzLookup :
    '''
        Base class for Lookup into musicbrainz using the gnat technique
    '''

    def __init__(self,
                 artist=None,
                 album=None,
                 title=None,
                 tracknumber=None,
                 threshold=60,
                 duration_distance_threshold=10000,
                 verbose=True,
                 allow_ambiguous=False,
                 use_cache=True) :
        '''

        @param artist:
        @param album:
        @param title:
        @param tracknumber:
        @param threshold:
        @param duration_distance_threshold:
        @param verbose:
        @param allow_ambiguous:
        '''
        if verbose:
            self._setlogger()
        self.threshold = threshold
        self.ddt=duration_distance_threshold
        self.cleaner = re.compile(r"[^A-Za-z0-9 ]").sub
        self.use_cache = use_cache


        if title != None:
            #[title] = self.audio['title']
            self.title = self.__clean_literal(str(title))
        else :
            self.title = None
        if artist != None :
            #[artist] = self.audio['artist']
            self.artist = self.__clean_literal(str(artist))
        else :
            self.artist = None
        if album != None :
            #[album] = self.audio['album']
            self.album = self.__clean_literal(str(album))
        else :
            self.album = None
        if tracknumber != None:
            self.tracknumber = int(self.__clean_literal(str(tracknumber)))
        else:
            self.tracknumber = None

        if self.title==None and self.artist==None and self.album ==None:
            raise MbzLookupException('must supply at least one of the following: artist, album, title')


    def mbzQuery(self) :
        if self.use_cache:
            self.query = CachedMBZQuery()
        else:
            self.query = Query()

        debug(' - Trying to guess an ID for track \"'+str(self.title)+'\", artist \"'+str(self.artist)+'\", release \"'+str(self.album)+'\", track number '+str(self.tracknumber))

        track_mapping = []

        # check for the 'one parameter' case
        if self.artist != None and self.title==None and self.album==None:
            debug("only artist name available, doing simple lookup")
            artists = self.getArtists()
            for artist in artists:
                track_mapping.append((artist.score, None, artist, None))

            self.track_mapping = track_mapping
            return
        elif self.artist == None and self.title!=None and self.album==None:
            debug("only track title given, doing simple lookup")
            tracks = self.getTracks()
            for track in tracks:
                track_mapping.append((track.score, track, None, None))

            self.track_mapping = track_mapping
            return
        elif self.artist == None and self.title==None and self.album==None:
            debug("only album title available, doing simple lookup")
            releases = self.getReleases()
            for release in releases:
                track_mapping.append((release.score, None, None, release))
            self.track_mapping = track_mapping
            return


        try:
            artists = self.getArtists()

            artist_mapping = []
            release_mapping = []
            track_mapping = []

            if(self.album==None):
                debug("No release information, dropping release lookup")

            for artist in artists :
                artist_id = (MbzURIConverter(artist.artist.id)).getId()
                artist_mapping.append((artist.score,artist))
                if(self.album!=None) :
                    # do the releases call
                    releases = self.getReleases(artist_id)
                    if releases == [] :
                        # do the mbz track call
                        tracks = self.getTracks(artist_id)
                        for track in tracks :
                            track_mapping.append(((track.score + artist.score)/2 ,track, artist, None))
                    for release in releases :
                        release_id = (MbzURIConverter(release.release.id)).getId()
                        release_mapping.append(((release.score + artist.score)/2,release))
                        # do the mbz track call
                        tracks = self.getTracks(artist_id,release_id)
                        if tracks==[]:
                            track_mapping.append(((artist.score + release.score)/2, None, artist, release))
                        for track in tracks :
                            track_mapping.append(((track.score +release.score + artist.score)/3 ,track, artist, release))

                else :
                    tracks = self.getTracks(artist_id)
                    for track in tracks :
                        track_mapping.append(((track.score + artist.score)/2 ,track, artist, None))





            if artists==[] :
                if(self.album!=None) :
                    releases = self.getReleases()
                    if releases == [] :
                        tracks = self.getTracks()
                        for track in tracks :
                            track_mapping.append((track.score ,track, None, None))
                    for release in releases :
                        release_id = (MbzURIConverter(release.release.id)).getId()
                        release_mapping.append((release.score,release))
                        tracks = self.getTracks(None,release_id)
                        for track in tracks :
                            track_mapping.append(((track.score +release.score)/2 ,track, None, release))

        except ResponseError, e:
            raise MbzLookupException('Musicbrainz response error')
        except ConnectionError, e:
            raise MbzLookupException('Musicbrainz connection error')
        except WebServiceError, e:
            raise MbzLookupException('Musicbrainz webservice error')

        # err might need to do this differently
        track_mapping.sort()
        track_mapping.reverse()
#        artist_mapping.sort()
#        artist_mapping.reverse()
#        release_mapping.sort()
#        release_mapping.reverse()
        #self.artist_mapping = artist_mapping
        #self.release_mapping = release_mapping
        self.track_mapping = track_mapping
        #if self.empty_results() :
        #    raise MbzLookupException('No results')
        #    debug('no track results')

        #if not self.confident() :
        #    raise MbzLookupException('Not confident enough about matching MBZ tracks')
        #self.clean_results()
        #if self.ambiguous() :
        #    debug('Disambiguating through duration')
        #    self.disambiguate_through_duration()
        #if self.empty_results() :
        #    raise MbzLookupException('No results')
        #debug('ID Found : '+self.track_mapping[0][1].track.getId())

    def getArtists(self) :
        if self.artist == None :
            return []
        else :
            artist_filter = ws.ArtistFilter(name=str(self.artist))
            artists = self.query.getArtists(filter=artist_filter)
            return artists

    def getTracks(self,artist_id=None,release_id=None) :
        if self.title == None:
            debug('no track title specified - skipping getTracks')
            return []
        else :
            if not(self.tracknumber == None) and not(release_id == None) :
                track_filter = ws.TrackFilter(query='tnum:'+str(self.tracknumber)+ ' AND reid:'+release_id)
            elif release_id==None and not(self.tracknumber == None) and not(self.title == None) and not(artist_id==None):
                track_filter = ws.TrackFilter(query='(track:"'+str(self.title)+'" AND tnum:'+str(self.tracknumber)+' )'+' AND arid:'+artist_id)
            elif artist_id==None and release_id==None :
                track_filter = ws.TrackFilter(query='(track:"'+str(self.title)+'")')
            elif release_id==None :
                track_filter = ws.TrackFilter(query='(track:"'+str(self.title)+'") '+' AND arid:'+artist_id)
            elif artist_id==None :
                track_filter = ws.TrackFilter(query='(track:"'+str(self.title)+'") '+' AND reid:'+release_id)
            else :
                track_filter = ws.TrackFilter(query='(track:"'+str(self.title)+'") '+' AND reid:'+release_id+' AND arid:'+artist_id)
            tracks = self.query.getTracks(track_filter)
            return tracks

    def getReleases(self,artist_id=None) :
        if self.album == None :
            return []
        else :
            if artist_id==None:
                release_filter = ws.ReleaseFilter(query='(release:'+str(self.album)+')')
            else :
                release_filter = ws.ReleaseFilter(query='(release:"'+str(self.album)+'") '+' AND arid:'+artist_id)
            releases = self.query.getReleases(release_filter)
            return releases


    def getMbzTrackURI(self) :
        if self.track_mapping[0][1] != None:
            return self.track_mapping[0][1].track.getId()
        else:
            return None

    def getMbzArtistURI(self) :
        if self.track_mapping[0][2] != None:
            return self.track_mapping[0][2].artist.getId()
        else:
            return None

    def getMbzReleaseURI(self) :
        if self.track_mapping[0][3] != None:
            return self.track_mapping[0][3].release.getId()
        else:
            return None

    # returns true if the first result have a confidence higher than the confidence threshold
    def confident(self) :
        if self.track_mapping[0][0] > self.threshold :
            return True
        else :
            return False

    # returns true in case there are no results, false otherwise
    def empty_results(self) :
        return self.track_mapping == []

    # drop results with not the highest confidence
    def clean_results(self) :
        samescoreresults = []
        k = 0
        while k < len(self.track_mapping) and self.track_mapping[k][0] == self.track_mapping[0][0] :
            samescoreresults.append(self.track_mapping[k])
            k = k + 1
        self.track_mapping = samescoreresults

    # returns true if two results have the same confidence, false otherwise
    def ambiguous(self)  :
        if self.empty_results() :
            return False
        a = self.track_mapping
        if len(a) == 1 :
            return False
        else :
            return True

    # changed this to return True is disambiguation was successful, False otherwise
    def disambiguate_through_duration(self) :
        if not hasattr(self.audio,"info"): # no duration info available (eg. with CSV input)
            #self.track_mapping = []
            return False

        duration = self.audio.info.length * 1000
        debug('Duration of the audio file (ms):' + str(duration))
        closest = self.ddt
        for result in self.track_mapping :
            if (result[1].track).getDuration()!=None :
                debug('Duration of matching track in MBZ: '+ str((result[1].track).getDuration()))
                if abs(duration - (result[1].track).getDuration()) < closest :
                    closest = duration - (result[1].track).getDuration()
                    closest_result = result
        if closest==self.ddt :
            #self.track_mapping = []
            return False
        else :
            self.track_mapping = [closest_result]
            return True


    def __clean_literal(self,literal) :
        t = self.cleaner("", literal)
        return re.sub(r' {2,}',' ',t)

    def _setlogger(self) :
        '''
            set the logger locally for debugging
        '''
        loggingConfig = {"format":'%(asctime)s %(levelname)-8s %(message)s',
                                   "datefmt":'%d.%m.%y %H:%M:%S',
                                    "level": logging.DEBUG,
                                    #"filename":logPath + "musicGrabber.log",
                                    "filemode":"w"}
        logging.basicConfig(**loggingConfig)

class MetadataLookup(MbzLookup):
    '''
        lookup by metadata
        lookup = MetadataLookup(artist=None, album=None, title=None, tracknumber=None, threshold=60)
        note you must supply at least one of artist, album, or title
    '''
    def __init__(self,
                 artist=None,
                 album=None,
                 title=None,
                 tracknumber=None,
                 threshold=60,
                 verbose=True,
                 allow_ambiguous=False,
                 use_cache=True):
        '''

        @param artist -  artist name of music entity in question
        @param album - album title of music entity in question
        @param title -  title of a track related to the entity in question
        @param tracknumber -  track number of a given music track with title=@title
        @param threshold=60 - threshold hold value for deciding if results are reliable
        @param verbose=True - if True, set logger to std out
        @param allow_ambiguous=False - if True, allow results to be ambiguous (have same score)
        @param use_cache=True - if True, write queries to disk and re-use queries where possible
        '''

        duration_distance_threshold=10000
        self.allow_ambiguous = allow_ambiguous



        try :
            # Note : I think we're too sensitive to track number
            # Before adding this check for track numbers of the form 'x/y' mapping would fail when it should probably have succeeded
            if tracknumber.find('/') > 0:
                self.tracknumber = int(str(tracknumber[0:tracknumber.find("/")]))
            else:
                self.tracknumber = int(str(tracknumber))
        except :
            self.tracknumber = None

        MbzLookup.__init__(self, artist, album, title, tracknumber, threshold, duration_distance_threshold, verbose, allow_ambiguous, use_cache)

        self.mbzQuery()
        self.check_results()

    def check_results(self):
        if self.empty_results() :
            raise MbzLookupException('No results')


        if not self.confident() :
            raise MbzLookupException('Not confident enough about matching MBZ tracks')
        self.clean_results()
        if not self.allow_ambiguous and self.ambiguous():
            raise MbzLookupException('Ambiguous results returned by search, try re-running with @allow_ambiguous=True')
        #if self.ambiguous() :
        #    debug('Disambiguating through duration')
        #    self.disambiguate_through_duration()
        if self.empty_results() :
            raise MbzLookupException('No results')
        debug('ID Found ! ')#+self.track_mapping[0][1].track.getId())

class FileLookup(MbzLookup):
    '''
        lookup a set of mbz URI based on the ID3 tag of the input file
    '''
    def __init__(self,
                 file,
                 threshold=60,
                 duration_distance_threshold=10000,
                 verbose=True,
                 allow_ambiguous=False,
                 use_cache=True):
        '''

        @param file -  path to file with ID3 tag to be used for lookup
        @param threshold=60 - threshold score for accepting a lookup result, lower this to be more forgiving of false positives
        @param duration_distance_threshold=10000 - duration threshold for disambiguating through audio file duration
        @param verbose=True
        @param allow_ambiguous=False - set to true to allow for ambiguous results to be accepted (results w/ the same score)
        @param use_cache=True - if True, write queries to disk and re-use queries where possible
        '''

        self.audio = None
        self.file = file
        self.cleaner = re.compile(r"[^A-Za-z0-9 ]").sub
        self.allow_ambiguous = allow_ambiguous


        # Try MP3 last cause it doesn't seem to throw an exception on wrong filetypes...
        handlers = [FLAC,OggVorbis,OggFLAC,OggTheora,APEv2,ASF,MP4,Musepack,TrueAudio,WavPack,lambda x: MP3(x,ID3=EasyID3)]
        for handler in handlers:
            if self.audio is None:
                try:
                    self.audio = handler(file)
                except:
                    pass
        if self.audio is None:
            raise FileTypeException('Unknown file type, no metadata, or file not found.')

        try :
            [title] = self.audio['title']
        except :
            title = None
        try :
            [artist] = self.audio['artist']
        except :
            artist = None
        try :
            [album] = self.audio['album']

        except :
            album = None
        try :
            # Note : I think we're too sensitive to track number
            # Before adding this check for track numbers of the form 'x/y' mapping would fail when it should probably have succeeded
            [tracknumber] = self.audio['tracknumber']
            if tracknumber.find('/') > 0:
                tracknumber = int(str(tracknumber[0:tracknumber.find("/")]))
            else:
                tracknumber = int(str(tracknumber))
        except :
            tracknumber = None

        MbzLookup.__init__(self, artist, album, title, tracknumber, threshold, duration_distance_threshold, verbose, allow_ambiguous, use_cache)
        self.mbzQuery()
        self.check_results()

    def check_results(self):
        if self.empty_results() :
            raise MbzLookupException('No results')
        if not self.confident() :
            raise MbzLookupException('Not confident enough about matching MBZ tracks')
        self.clean_results()
        if self.ambiguous() :
            debug('Disambiguating through duration')
            if not self.disambiguate_through_duration() and not self.allow_ambiguous:
                raise MbzLookupException('Ambiguous results returned by search, try re-running with @allow_ambiguous=True')
        if self.empty_results() :
            raise MbzLookupException('No results')
        debug('ID Found ! ')#+self.track_mapping[0][1].track.getId())


def filelookup(file,
               threshold=60,
               duration_distance_threshold=10000,
               verbose=True,
               allow_ambiguous=False,
               use_cache=True):
    '''
    Lookup a set of musicbrainz ids based on the ID3 tag of an input audio file

    filelookup(file,
               threshold=60,
               duration_distance_threshold=10000,
               verbose=True,
               allow_ambiguous=False,
               use_cache=True)

    parameters:
        @param file -  path to file with ID3 tag to be used for lookup
        @param threshold=60 - threshold score for accepting a lookup result, lower this to be more forgiving of false positives
        @param duration_distance_threshold=10000 - duration threshold for disambiguating through audio file duration
        @param verbose=True
        @param allow_ambiguous=False - set to true to allow for ambiguous results to be accepted (results w/ the same score)
        @param use_cache=True - if True, write queries to disk and re-use queries where possible

    returns:
        a dictionary of the form

        ['artistURI']     =     URI for artist match or None if no match found
        ['artistMbz']     =     Artist's musicbrainz page
        ['artist']        =     a musicbrainz2.model.Artist object or None if no match found
        ['releaseURI']    =     URI for release (album) or None if no match found
        ['releaseMbz']    =     release musicbrainz page
        ['release']       =     a musicbrainz2.model.Release object or None if no match found
        ['trackURI']      =     URI for track match or None if no match found
        ['trackMbz']      =     track musicbrainz page
        ['track']         =     a musicbrainz2.model.Track object or None if no match found
        ['score']         =     overall score for the match out of 100


    '''
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    mbz = FileLookup(file, threshold, duration_distance_threshold, verbose, allow_ambiguous, use_cache)
    return __setdict__(mbz)

def __setdict__(mbz):
    dict = {}
    if mbz.getMbzArtistURI() != None:
        dict['artistURI'] = DBTUNE_URI+mbz.getMbzArtistURI().split('http://musicbrainz.org')[1]
        dict['artistMbz'] = mbz.getMbzArtistURI()
    if mbz.track_mapping[0][2] != None:
        dict['artist'] = mbz.track_mapping[0][2].artist
        #dict['artistID'] = mbz.track_mapping[0][2].artist.getID()
    else:
        dict['artist'] = None
    if mbz.getMbzReleaseURI() !=None:
        dict['releaseURI'] = DBTUNE_URI+mbz.getMbzReleaseURI().split('http://musicbrainz.org')[1]
        dict['releaceMbz'] = mbz.getMbzReleaseURI()
    if mbz.track_mapping[0][3] != None:
        dict['release'] = mbz.track_mapping[0][3].release
    else:
        dict['release'] = None
    if mbz.getMbzTrackURI() !=None:
        dict['trackURI'] = DBTUNE_URI+mbz.getMbzTrackURI().split('http://musicbrainz.org')[1]
        dict['trackMbz'] = mbz.getMbzTrackURI()
    if mbz.track_mapping[0][1]!=None:
        dict['track'] = mbz.track_mapping[0][1].track
    else:
        dict['track'] = None
    dict['score'] = mbz.track_mapping[0][0]

    return dict

def metadatalookup(artist=None,
                 release=None,
                 track=None,
                 tracknumber=None,
                 threshold=60,
                 verbose=True,
                 allow_ambiguous=False,
                 use_cache=True):
    '''
    Lookup a set of musicbrainz ids based on the input metadata

    metadatalookup(artist=None,
                 release=None,
                 track=None,
                 tracknumber=None,
                 threshold=60,
                 verbose=True,
                 allow_ambiguous=False,
                 use_cache=True)

    parameters:
        @param artist -  artist name of music entity in question
        @param release - release (album) title of music entity in question
        @param track -  title of a track (song) related to the entity in question
        @param tracknumber -  track number of a given music track with title=@title
        @param threshold=60 - threshold hold value for deciding if results are reliable
        @param verbose=True - if True, set logger to std out
        @param allow_ambiguous=False - if True, allow results to be ambiguous (have same score)
        @param use_cache=True - if True, write queries to disk and re-use queries where possible:

    returns:
        a dictionary of the form

        ['artistURI']     =     URI for artist match or None if no match found
        ['artistMbz']     =     Artist's musicbrainz page
        ['artist']        =     a musicbrainz2.model.Artist object or None if no match found
        ['releaseURI']    =     URI for release (album) or None if no match found
        ['releaseMbz']    =     release musicbrainz page
        ['release']       =     a musicbrainz2.model.Release object or None if no match found
        ['trackURI']      =     URI for track match or None if no match found
        ['trackMbz']      =     track musicbrainz page
        ['track']         =     a musicbrainz2.model.Track object or None if no match found
        ['score']         =     overall score for the match out of 100

    '''
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    mbz = MetadataLookup(artist, release, track, tracknumber, threshold, verbose, allow_ambiguous, use_cache)
    return __setdict__(mbz)