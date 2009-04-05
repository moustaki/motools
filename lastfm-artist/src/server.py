'''
Created on 2 Apr 2009

A really simple python webserver to implement linked data - style 
303 redirects and last.fm lookups - uses CherryPy

@author: kurtjx
'''


import cherrypy
import artistlookup

f = open('index.html')
HTML_USAGE = f.read()
f.close()


URL_BASE = 'http://dbtune.org/artists/last-fm/'

class SWServer:
    @cherrypy.expose
    def default(self, urlpath):
        if urlpath.endswith('.rdf'):
            cherrypy.response.headers['Content-Type'] = 'application/rdf+xml'
            print cherrypy.response.headers
            lses = artistlookup.LastFMSession(urlpath.rsplit('.rdf')[0])
            lses.authenticate()
            lses.getLastFMdata()
            return lses.createRDFGraph()
        else:
            # do a 303 redirect adding '.rdf' to the end
            raise cherrypy.HTTPRedirect(URL_BASE+urlpath+'.rdf', 303)

    
    @cherrypy.expose
    def index(self):
        return HTML_USAGE
    
class MBIDServer:
    @cherrypy.expose
    def default(self, urlpath):
        if urlpath.endswith('.rdf'):
            # actually do the lookup
            cherrypy.response.headers['Content-Type'] = 'application/rdf+xml'
            lses = artistlookup.LastFMSession()
            lses.authenticate()
            lses.getLastFMdata(urlpath.rsplit('.rdf')[0])
            return lses.createRDFGraph()
        else:
            # redirect
            raise cherrypy.HTTPRedirect(URL_BASE+'mbid/'+urlpath+'.rdf', 303)
        
    @cherrypy.expose
    def index(self):
        return HTML_USAGE

root = SWServer()
root.mbid = MBIDServer()
#appconf = {'/': {'tools.proxy.on':True,}}
cherrypy.config.update({'server.socket_port': 2059})

cherrypy.quickstart(root)#, '/', appconf)
            
