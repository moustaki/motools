#!/usr/bin/python2.4
'''
Created on 2 Apr 2009

A really simple python webserver to implement linked data - style 
303 redirects and last.fm lookups - uses CherryPy

@author: kurtjx

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import cherrypy
from artistlookup import LastFMSession

f = open('index.html')
HTML_USAGE = f.read()
f.close()


URL_BASE = 'http://dbtune.org/artists/last-fm/'

# make a global LastFMSession instance


class SWServer:
    @cherrypy.expose
    def default(self, urlpath):
        lses = LastFMSession()
        lses.authenticate()
        if urlpath.endswith('.rdf'):
            cherrypy.response.headers['Content-Type'] = 'application/rdf+xml'
            #lses = artistlookup.LastFMSession(urlpath.rsplit('.rdf')[0])
            #lses.authenticate()
            
            lses.artistname = urlpath.rsplit('.rdf')[0]
            lses.getLastFMdata()
            return lses.createRDFGraph()
        else:
            # do a 303 redirect adding '.rdf' to the end
            lses.artistname = urlpath
            mbid = lses.getMBID()
            if mbid:
                raise cherrypy.HTTPRedirect(URL_BASE+'mbid/'+mbid)
            else:
                raise cherrypy.HTTPRedirect(URL_BASE+urlpath+'.rdf', 303)

    
    @cherrypy.expose
    def index(self):
        return HTML_USAGE
    
class MBIDServer:
    @cherrypy.expose
    def default(self, urlpath):
        lses = LastFMSession()
        lses.authenticate()
        if urlpath.endswith('.rdf'):
            # actually do the lookup
            cherrypy.response.headers['Content-Type'] = 'application/rdf+xml'
            #lses = artistlookup.LastFMSession()
            #lses.authenticate()
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
appconf = {'/': {'tools.proxy.on':True,}}
cherrypy.config.update({'server.socket_port': 1210,
                        'server.socket_host': '192.168.122.144', 
                        'log.screen': True 
                        #,'log.access_file': '/var/log/artist-last-fm-access.log' 
                        #,'log.error_file':'/var/log/artist-last-fm-error.log'
                        ,'server.thread_pool':30
                        ,'server.socket_queue_size': 10
                        ,'response.timeout': 100000000  # do we need this??
                        ,'request.timeout':  100000000
                        })

print cherrypy.config
cherrypy.quickstart(root, '/', appconf)
            
