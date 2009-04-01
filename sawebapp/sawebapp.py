
from __future__ import with_statement
import os,sys,time
import datetime
import ConfigParser
import cherrypy
from cherrypy.lib import static
import mopy
from mopy import vamp as vamp
from Cheetah.Template import Template
import threading
import shutil
from musicbrainz2.webservice import Query, TrackFilter

# from shutil import copyfileobj, rmtree
# from pylab import *
# from numpy import *

import dl
sys.setdlopenflags(dl.RTLD_NOW|dl.RTLD_GLOBAL)

from cherrypy.lib.sessions import Session

class MusicBrainz(object):
	
	def lookup_puid(self,_puid):
		q = Query()
		f = TrackFilter(puid=_puid)
		try :
			r = q.getTracks(f)
			track = r[0].track
			return track
		except:
			print 'MusicBrainz::lookup_puid: Error finding track metadata.'
			# raise AssertionError('MusicBrainz::lookup_puid: Error finding track metadata.')
			return None
		

class DirectorySession(Session):

	cache = {}
	locks = {}
	instanceList = []
	# SESSIONS_PATH = '/Users/Shared/Development/sonic-annotator-webapp/sessions/'
	
	def __init__(self, id=None, **kwargs):
		for i in self.instanceList : 
			print 'previous-sessions: ', i.id
			if (i.id == id) :
				print 'got instance already!'
		self.instanceList.append(self)
		print 'instance initialised:' + str(len(self.instanceList))
		# kwargs['SESSIONS_PATH'] = os.path.abspath(kwargs['SESSIONS_PATH'])        
		Session.__init__(self, id=id, **kwargs)
		print 'active sessions: ' + str(self.__len__())

	def setup(cls,**kwargs):
		print 'Setting up storage class... Nothing to do here yet.'
		for k, v in kwargs.iteritems():
			setattr(cls, k, v)
			print k,v
		# cls.SESSIONS_PATH = kwargs['SESSIONS_PATH']
		# we could setup a cleanup thread here for the dirs too.
        # kwargs['sessions_path'] = os.path.abspath(kwargs['sessions_path'])

		if (os.path.exists(cls.SESSIONS_PATH)) :
			shutil.rmtree (cls.SESSIONS_PATH, ignore_errors=True, onerror=None)
		if not (os.path.exists(cls.SESSIONS_PATH)) :
			os.mkdir(cls.SESSIONS_PATH)

	setup = classmethod(setup)
	
	def get_session_path(self):
		""" Return a valid path for this session """
		if self.has_key('session_path') : 
			return self.get('session_path',None)
		else :
			if not self.id : 
				raise AssertionError("Can not create directory for uninitialised session.")
				return None
			sessionPath = os.path.join(self.SESSIONS_PATH,str(self.id))
			if os.path.exists(sessionPath) :
				# clash of session IDs (unprobable), flush data
				shutil.rmtree (sessionPath, ignore_errors=True, onerror=None)
				print "flushed data in %s" % sessionPath
			try : 
				os.makedirs(sessionPath)
			except:
				raise AssertionError("Session directory for id %r not created." % self.id)
				return None
			if os.path.exists(sessionPath) :
				# create an entry in self so that the clean_up thread knows about this session
				# setattr(self._data,'session_path',sessionPath)
				self['session_path'] = sessionPath
				return  sessionPath


	def write_fsfile(self,fsFile,fileType = 'any_file'):
		#fsFile is a cgi.FieldStorage object : cherrypy._cpcgifs.FieldStorage()
		if hasattr (fsFile,'filename') and hasattr(fsFile,'file'):
			self._write_file(fsFile.file,fsFile.filename,fileType)
			
	# TODO: the other use case: write the output of a pipe
	def write_file(self,fileObj,fileName,fileType = 'any_file'):
		pass
	
	def _write_file(self,file,filename,filetype):
		filename = filename.replace(' ','_')
		sessionPath = self.get_session_path()
		filePath = os.path.join(sessionPath,filename)
		print 'writing file to: ',filePath

		file.seek(0)
		newFile = open(filePath,'wb')
		try :
			shutil.copyfileobj(file,newFile)
		except :
			try :
				while True:
					data = file.read(8192)
					if not data: break
					newFile.write(data)
			except:
				print 'Could not write file to session %r' % self.id
				raise AssertionError("Could not write file to session %r " % self.id)
		finally:
			newFile.close()
		
		if os.path.exists(filePath) and os.stat(filePath).st_size > 0 :
			if self.has_key(filetype) :
				ol = self.get(filetype,None)
				ol.append(os.path.basename(filePath))
				self[filetype] = list(ol)
			else:
				self[filetype]= list([os.path.basename(filePath)])
			self.save()
			
				
	def getFiles(self,filelist):
		pass
           
	def clean_up(self):
		"""Clean up expired sessions."""
		now = datetime.datetime.now()
		print 'In custom Cleanup Method!'
		print 'Length of cache = ', len(self.cache)
		print 'cache members: ', self.cache.keys()
		for id, (data, expiration_time) in self.cache.items():
			print 'Id: ', id
			print 'expiration time: ', expiration_time
			print 'Length of data: ', len(data)
			print 'data members: ', data.keys()

			if expiration_time < now:

				path = os.path.join(self.sessionsPath,str(id))
				if os.path.exists(path) :
					for fname in os.listdir(path):
						os.remove(os.path.join(path,fname))
					# os.removedirs(path) -> removes sessions too
					os.rmdir(path)					
				try:
					del self.cache[id]
				except KeyError:
					pass
				try:
					del self.locks[id]
				except KeyError:
					pass
	
	def _exists(self):
		return self.id in self.cache
	
	def _load(self):
		return self.cache.get(self.id)

	#this is always called on an on_end_request hook (by cherrypy.session.save)
	def _save(self, expiration_time):
		print 'Saving Session ', self.id
		self.cache[self.id] = (self._data, expiration_time)
	
	def _delete(self):
		del self.cache[self.id]
	
	def acquire_lock(self):
		"""Acquire an exclusive lock on the currently-loaded session data."""
		self.locked = True
		self.locks.setdefault(self.id, threading.RLock()).acquire()
	
	def release_lock(self):
		"""Release the lock on the currently-loaded session data."""
		self.locks[self.id].release()
		self.locked = False
	
	def __len__(self):
		"""Return the number of active sessions."""
		return len(self.cache)

cherrypy.lib.sessions.DirectorySession = DirectorySession

#Holds the current configuration environment
class Config(object):

	# Load config from file and setup the environment
	def __init__(self,debug = False, forceWrite = False, configFile = './config/default.cfg'):

		self.localdir = os.path.dirname(__file__)
		self.absdir = os.path.join(os.getcwd(), self.localdir)
		self.debug = debug

		# Config File Reader
		self.cfgobj = ConfigParser.ConfigParser();
		if forceWrite or self.cfgobj.read(configFile) == list() :
			self.write(configFile)

        # Sonic Annotator Environment
		self.bindir = self.cfgobj.get('Files','bin-directory')
		self.binary_name = self.cfgobj.get('Sonic Annotator','binary-name')
		self.listopt = self.cfgobj.get('Sonic Annotator','list-transforms')
		self.default = self.cfgobj.get('Sonic Annotator','default-transforms')
		self.binary = os.path.join(self.bindir,self.binary_name)
		# if os.path.isfile(self.sa) : os.chmod(self.sa,448|56)
		
		# CherryPy-Server Environment
		self.server_config = os.path.join(self.localdir, self.cfgobj.get('Cherrypy Server','configuration-file'))
		self.server_session_timeout = self.cfgobj.get('Cherrypy Server','session-timeout')
		self.server_cleanup_frequency = self.cfgobj.get('Cherrypy Server','cleanup-frequency')
		self.server_sessions_path = self.cfgobj.get('Cherrypy Server','sessions-path')
		

	# Rewrite the configuration file
	def write(self,configFile):

		self.cfgobj.add_section('Files')
		self.cfgobj.set('Files','bin-directory','./bin')
		self.cfgobj.set('Files','rdf-directory','./rdf')
		self.cfgobj.set('Files','sessions-directory','./sessions')
		self.cfgobj.set('Files','plugin-directory','/Library/Audio/Plug-Ins/Vamp/')

		self.cfgobj.add_section('Sonic Annotator')
		self.cfgobj.set('Sonic Annotator','binary-name','sonic-annotator')
		self.cfgobj.set('Sonic Annotator','list-transforms','-l')
		self.cfgobj.set('Sonic Annotator','default-transforms','$binary -d $transform $audio -w $writer $output $fileOption')
				
		self.cfgobj.add_section('Cherrypy Server')
		self.cfgobj.set('Cherrypy Server','configuration-file','./config/server.cfg')
		self.cfgobj.set('Cherrypy Server','session-timeout','60')
		self.cfgobj.set('Cherrypy Server','cleanup-frequency','10')
		self.cfgobj.set('Cherrypy Server','sessions-path','/Users/Shared/Development/sonic-annotator-webapp/sessions/')
		
		print "Writing new config file."
		cfgdir = os.path.dirname(configFile)
		if not os.path.isdir(cfgdir) : os.mkdir(cfgdir)
		with open(configFile,'w') as f : self.cfgobj.write(f)
		if not os.path.isfile(configFile) : print 'Could not write config file!'

# We should use MOPY objects to represent these:

#A dictionary of plugins in the library
class PluginLibrary(dict):

	def __init__(self,type,identifier):
		dict.__init__(self)
		self.type = type
		self.identifier = identifier
		self.friendlyName = 'Plugin Library'
	
#A dictionary of outputs plus some info about the plugin
class VampPlugin(dict):

	def __init__(self,identifier):
		dict.__init__(self)
		self.identifier = identifier
		self.friendlyName = 'Vamp Plugin'
		
#An available transform: plugin output config templates
class PluginOutput:

	def __init__(self,identifier):
		self.identifier = identifier

#A transform is a (plugin-output,configuration) pair, in another way a configured transform
class Transform:
	pass	

class SonicAnnotatorException(Exception):
	def __init__(self, message) :
		self.message = message
	def __str__(self) :
		return self.message

#Python wrapper for Sonic Annotator
class SonicAnnotator(object):
	
	def __init__(self,config):
		self.conf = config
		self.binary = self.conf.binary
				
	def getTransforms(self):
		listtr = ' '.join([self.binary,self.conf.listopt])
		libs = {}
		try :
			with os.popen(listtr,'r') as tl :
				transformList = tl.readlines();
		except : 
			raise SonicAnnotatorException('Error obtaining transform list.')
		for transform in transformList :
			t = transform.split(':')
			if len(t) < 4 : 
				print 'Invalid transform? :',transform
				continue

			type,library,plugin,output = t
			if type != 'vamp' : 
				print 'Unknown plugin library:',type
				continue
			
			if not library in libs.keys() :
				lib = {}
				libs[library] = lib
			else:
				lib = libs[library]
			
			if not plugin in lib.keys() :
				plug = set()
				lib[plugin] = plug
			else:
				plug = lib[plugin]
				
			plug.add(transform)
				
		return libs

	def getPuid(self,audioFiles):
		if type(audioFiles) != type([]) : audioFiles = [audioFiles]
		template = Template(self.conf.default)
		template.binary = self.binary
		template.transform = 'vamp:ofa-vamp-plugin:ofa_puid:puid'
		audioFiles = map(lambda x: '"'+x+'"',audioFiles)
		template.audio = ' '.join(audioFiles)
		template.writer = 'csv'
		template.output = '--csv-stdout'
		template.fileOption = ''
		puid = '-1'

		try :
			with os.popen(str(template),'r') as output :
				result = output.readlines();
		except : 
			raise SonicAnnotatorException('sonicAnnotator::getPuid: Error executiong transform.')
		try :
			puid = result[0].split(',')[2]
			puid = puid.replace('"','')
		except:
			print ('sonicAnnotator::getPuid: Error in parsing results.')
			# raise SonicAnnotatorException('sonicAnnotator::getPuid: Error in parsing results.')
		return puid.strip()                                 


	def runDefaultTransform (self,transform,audioFiles):
		if type(audioFiles) != list : audioFiles = [audioFiles]
		if type(transform) != list : transform = [transform]
		template = Template(self.conf.default)
		template.binary = self.binary
		template.transform = ' -d '.join(transform)
		audioFiles = map(lambda x: '"'+x+'"',audioFiles)
		template.audio = ' '.join(audioFiles)
		template.writer = 'rdf'
		template.output = '--rdf-stdout'
		template.fileOption = ''

		try :
			with os.popen(str(template),'r') as output :
				result = output.readlines();
		except : 
			raise SonicAnnotatorException('Error executiong transform.')
		return str().join(result)

# This class generates the individual web pages 
# independently of the site structure
# It requires an instance of Sonic Annotator passed in through the config object
class Generator(object):
	
	# originalCallback = None

	def __init__(self,config):
		self.config = config
		self.sonic = config.sonicAnnotator
		if hasattr (config,'server') : self.server = config.server
		
	def newCallback(self):
		print 'callback reached at: ' + str(datetime.datetime.now())
		self.originalCallback()
		
	def omrasTestPage(self):
		page = Template(file="./templates/index-omras2style.html")
		page.sessionID = self.server.getSessionID()
		
		return str(page)

    #generate json objects for musicbrainz track metadata
	def jsDataGenerator(self,filelist):
		js_object = "trackMetadata[%s] = {subject:'%s', predicate:'%s', object:'%s'};\n"
		
        #musicbrainz Track props
		# mbMap = ['title','duration','id','puids']
		mbMap = ['title','duration','id']

		result = str()
		for filename in filelist :
			if cherrypy.session.has_key(filename) :
				track = cherrypy.session[filename]
				result = result + js_object % (0,filename,"Puid: ",track.puids[0])
				result = result + js_object % (1,filename,"Artist: ",track.artist.name)
				for i,pred in enumerate(mbMap) :
					result = result + js_object % (i+2,filename,pred,str(getattr(track,pred)))
					
		return result
				
    #generate the main index page
	def multipartTestPage(self):
		omras_page = Template(file="./templates/omras-template.html")
		omras_page.title = "Sonic Annotator Webapplication"
		
		#content = main content within an omras page
		content = Template(file="./templates/main-content.html")
		content.title = "OMRAS2 Music Analysis and Feature Extraction Service"
		
		#see if we have audio, hence if we need the id block...
		if cherrypy.session.has_key('audio_file') :
			#file_id_block = list of files uploaded so far
			filelist = list(cherrypy.session['audio_file'])
			file_id_block = Template(file="./templates/fileID-block.html")
			file_id_block.section_title = "File Identification"
			file_id_block.javascript_data = self.jsDataGenerator(filelist)
			file_id_block.file_list = list(cherrypy.session['audio_file'])
			content.file_id_block = str(file_id_block)
			omras_page.on_load_script = """ window.location.hash="upload_file" """
		else:
			content.file_id_block = ''
			omras_page.on_load_script = ''

		vamp_transforms = self.sonic.getTransforms()
		content.text = vamp_transforms.items()
		content.transforms = vamp_transforms
		content.sessionID = self.server.getSessionID()

		omras_page.content = str(content)
		count = cherrypy.session.get('count', 0) + 1
		cherrypy.session['count'] = count

		return str(omras_page)
		
	#this is just junk (to be deleted)
	def saTestPage(self):
		trs = self.sonic.getTransforms()
		# print trs.items()
		result = Template(file="./templates/index2.html")
		result.text = trs.items()
		result.transforms = trs
		result.sessionID = self.server.getSessionID()
		
		server = self.config.server

		count = cherrypy.session.get('count', 0) + 1
		cherrypy.session['count'] = count

		t = cherrypy.session.clean_thread
		s = cherrypy.session
		# currentCB = cherrypy.session.clean_thread.callback
		# cherrypy.session.clean_thread.callback = self.newCallback

		# result.session_data =  str(dir(t)) + " \n" + str(dir(t.callback))
		result.session_data = '>>'+str(type(cherrypy.session))
		# print dir(cherrypy.session.clean_thread.callback)
		# print cherrypy.session.timeout
		# print cherrypy.session.clean_freq
		# print hasattr(cherrypy.session,'cache')
		
		#we are in a RamSession Class: s
		print 'clean thread', s.clean_thread
		print 'callback', s.clean_thread.callback
		
		# self.originalCallback = s.clean_thread.callback
		# cherrypy.session.clean_thread.callback = self.newCallback
		# print 'reassigned callback', s.clean_thread.callback
		#restart the Monitor (cleanup) thread
		# s.clean_thread.graceful()
		
		#make sure the thread is started
		# s['make_start_thread'] = 1
		#change the callback to ours...

		return str(result)  


class Application(object):

	def __init__(self,config, generator = None) :
		self.config = config
		self.server = config.server
		if (generator == None and hasattr(config,'generator')) :
			self.generator = config.generator

	# #set the configuration of the cherrypy app. e.g. session timeout
	# _cp_config = {
	# 'tools.sessions.on': True ,
	# 'tools.sessions.timeout': 5,
	# 'tools.sessions.clean_freq': 6,
	# 'tools.sessions.storage_type': 'directory',
	# 'tools.sessions.sessions_path': 'whatever'
	# }

class SiteRoot(Application):
		
	def index(self):
		count = self.server.getHitCount()
		# indexPage = self.generator.saTestPage()
		# indexPage = self.generator.omrasTestPage()		
		indexPage = self.generator.multipartTestPage()
		return indexPage 

	index.exposed = True
	
    #file upload request handler
	def upload_file(self, audioFile = None, identify = None):
		if (audioFile == None or audioFile.filename == '') : 
			return "<html><body>Error: You must upload an audio file.</body></html>"
		cherrypy.session.write_fsfile(audioFile,'audio_file')

		#get musicbrainz data
		filename = audioFile.filename.replace(' ','_')		
		file = self.server.getFullPath(filename)
		puid = self.config.sonicAnnotator.getPuid(file)

		print 'got puid: ',puid
		m = MusicBrainz()
		trackdata = m.lookup_puid(puid)
		if trackdata != None :
			trackdata.addPuid(puid)
			print trackdata.artist.name
			cherrypy.session[filename] = trackdata
		return self.index()

	upload_file.exposed = True

	#run selected transfoms (using the default for now)
	def process(self, filelist = None, transform = None, identify = None):
		print filelist
		print transform
		filelist = self.server.getFullPath(filelist)
		result = self.config.sonicAnnotator.runDefaultTransform(transform,filelist)

		omras_page = Template(file="./templates/omras-template.html")
		omras_page.title = "Sonic Annotator Webapplication"
		omras_page.on_load_script = '' 
		omras_page.content = """ 
		<pre>%s</pre> """ % result.replace('<','&#60;').replace('>','&#62;')
		
		template = """<html>
		<head>
		<title>Sonic Annotator Webapplication</title>
		<meta http-equiv="Content-Type" content="text/plain; charset=utf-8" />
		</head>
		<body>
		<PRE>%s</PRE>
		</body>
		</html>""" 
		# return template % result.replace('<','&#60;').replace('>','&#62;')
		return str(omras_page)
		
	process.exposed = True

		
	def download(self):
		path = os.path.join(absDir, "result.rdf")
		return static.serve_file(path, "application/x-download","attachment", os.path.basename(path))
	download.exposed = False

# cherrypy.tree.mount(SiteRoot(Generator()))

# This is a tiny wrapper on cherrypy
class CherryPyServer(object):
	
	def __init__(self,config):
		self.conf = config
	
	def quickstart(self):
		#set the configuration of the cherrypy app. e.g. session timeout
		_cp_config = {
		'tools.sessions.on': True ,
		'tools.sessions.timeout': int(self.conf.server_session_timeout),
		'tools.sessions.clean_freq': int(self.conf.server_cleanup_frequency),
		'tools.sessions.storage_type': 'directory',
		'tools.sessions.SESSIONS_PATH': self.conf.server_sessions_path
		}
		# cherrypy.quickstart(config=self.conf.server_config)
		cherrypy.quickstart(config=_cp_config)
		
	
	def mount(self,requesthandler):
		cherrypy.tree.mount(requesthandler)
		
	def getHitCount(self):
		if hasattr(cherrypy,'session') :
			count = cherrypy.session.get('count', 0) + 1
			cherrypy.session['count'] = count
			return count
		else:
			return 0
		
	def getSessionID(self):
		if hasattr(cherrypy,'session') :
			return str(cherrypy.session.id)
		else:
			raise AssertionError('server::getSessionID: No session information available.') 
	
	def getFullPath(self,filelist):
		if (type(filelist) == list) :
			return map(lambda x: self.getFullPath(x),filelist)
		else:
			if (type(filelist) != str) : 
				raise AssertionError('server::getFullPath: Wrong path name in file list:%s' %filelist)
			return os.path.join(self.getSessionPath(),filelist) 
		
	def getSessionPath(self):
		if hasattr(cherrypy,'session') :
			return cherrypy.session.get_session_path()
		else:
			raise AssertionError('server::getSessionPath: No session information available.') 
		

def main(args):

	debug = False
	if args.count('-debug') : debug = True; args.remove('-debug'); print 'Debug mode.'  
	c = Config(debug,True)
	
	s = SonicAnnotator(c)

	#mopy has trouble importing the rdf vamp plugin descriptors
	#this needs to be patched at some point
	#mi = mopy.RDFInterface.importRDFFile("./rdf/vamp-example-plugins.n3","n3")
	
	#simple test workflow:
	#create a page for the transform list
	#accept file
	#run a default transform

	# cherrypy.tree.mount(SiteRoot(Generator()))
	# cherrypy.quickstart(config=os.path.join(c.localdir, './config/server.cfg'))

	#create server and web page generator instances
	server = CherryPyServer(c)
	c.sonicAnnotator = s
	c.server = server
	g = Generator(c)
	c.generator = g

	#create request handler root object
	app = SiteRoot(c)
	
	#mount the request handler and start the service
	server.mount(app)
	server.quickstart()

if __name__ == '__main__':
	main(sys.argv[1:])

