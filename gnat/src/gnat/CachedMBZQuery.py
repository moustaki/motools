from musicbrainz2.webservice import Query
import cPickle as pickle
import os.path
import os
import md5
import time

class CachedMBZQuery(Query) :

	def __init__(self,wait=3) :
		if not os.path.isdir('cache') :
			os.mkdir('cache')
			os.mkdir(os.path.join('cache','artist_q'))
			os.mkdir(os.path.join('cache','release_q'))
			os.mkdir(os.path.join('cache','track_q'))
		self.wait = wait
		self.last_called = time.time()
		Query.__init__(self)

	def getArtists(self,filter=filter) :
		p = md5.new(pickle.dumps(filter)).hexdigest()
		cache_file = os.path.join('cache','artist_q',p)
		if os.path.exists(cache_file) :
			instream = open(cache_file,"r")
			toret = pickle.loads(instream.read())
			instream.close()
			return toret
		else :
			self.throttle()
			toret = Query.getArtists(self,filter=filter)
			outstream = open(cache_file,"w")
			outstream.write(pickle.dumps(toret))
			outstream.close()
			return toret

	def getReleases(self,filter=filter) :
		p = md5.new(pickle.dumps(filter)).hexdigest()
		cache_file = os.path.join('cache','release_q',p)
                if os.path.exists(cache_file) :
                        instream = open(cache_file,"r")
                        toret = pickle.loads(instream.read())
                        instream.close()
                        return toret
                else :
			self.throttle()
			toret = Query.getReleases(self,filter=filter)
                        outstream = open(cache_file,"w")
                        outstream.write(pickle.dumps(toret))
                        outstream.close()
			return toret

	def getTracks(self,filter=filter) :
		p = md5.new(pickle.dumps(filter)).hexdigest()
		cache_file = os.path.join('cache','track_q',p)
                if os.path.exists(cache_file) :
                        instream = open(cache_file,"r")
                        toret = pickle.loads(instream.read())
                        instream.close()
                        return toret
                else :
			self.throttle()
			toret = Query.getTracks(self,filter=filter)
                        outstream = open(cache_file,"w")
                        outstream.write(pickle.dumps(toret))
                        outstream.close()
                        return toret
	
	def throttle(self) :
		last = self.last_called
		t = time.time()
		dur = t - last
		if dur < self.wait :
			time.sleep(dur)
		self.last_called = time.time()



