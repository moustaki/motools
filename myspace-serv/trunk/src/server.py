#!/usr/bin/python2.4
'''
Created on 15 May 2009

A really simple python webserver to implement linked data - style 
303 redirects and myspace lookups - uses CherryPy

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
import os
from myspace2rdf import Scrape
from myspace2html import Htmlify

#change to a blank string for local testing, no trailing '/'
URL_BASE = "http://dbtune.org/test" 

class Myspace:
    @cherrypy.expose
    def index(self):
        f = open('static/index.html', 'r')
        html = f.read()
        return html
    
    @cherrypy.expose
    def default(self, artist_name):
        s = Scrape()
        try:
            s.getUserID(artist_name)
        except:
            print "invalid myspace url or problems w/ myspace server. if you are sure the url is correct, try again in a few seconds..."
        else:
            raise cherrypy.HTTPRedirect(URL_BASE+'/uid/'+s.uid, 303)
    
class MyspaceUID:
    @cherrypy.expose
    def index(self):
        pass
    
    @cherrypy.expose
    def default(self, uid):
        if uid.endswith('.rdf'):
            # serve the data
            cherrypy.response.headers['Content-Type'] = 'application/rdf+xml; charset=UTF-8;'
            s = Scrape(uid.rsplit('.rdf')[0])
            s.getPage()
            artist = s.isArtist()
            s.getFriends(artist)
            
            if artist:
                return s.createArtistRDF()
            else:
                return s.createRDF()
        
        elif uid.endswith('.html'):
            # serve the html
            mh = Htmlify("http://dbtune.org/myspace/uid/"+uid.rsplit('.html')[0])
            mh.parse_rdf()
            mh.get_all()
            return mh.html_head + mh.serialize_n3() + mh.get_available_as() +mh.html_tail
        else:
            # check accept header and do content negotiation
            accepts = cherrypy.request.headers['Accept']
            if accepts.find('application/rdf+xml') != -1:
                raise cherrypy.HTTPRedirect(URL_BASE+'/uid/'+uid+'.rdf', 303)
            elif accepts.find('text/html') != -1 :
                raise cherrypy.HTTPRedirect(URL_BASE+'/uid/'+uid+'.html', 303)
            else:
                return "unknown content type - bad accept header from client"
    
    
root = Myspace()
root.uid = MyspaceUID()

appconf = {'/': {'tools.proxy.on':True,}
           ,'/style.css': {'tools.staticfile.on': True,
                               'tools.staticfile.filename': os.path.join(os.path.abspath(''), 'static', 'style.css')}
           }
cherrypy.config.update({'server.socket_port': 1213, 
                        'log.screen': True 
                        ,'log.access_file': '/var/log/dbtune-myspace-access.log' 
                        ,'log.error_file':'/var/log/dbtune-myspace-error.log'
                        ,'tools.caching.on': True   #use cherrypy automagik caching
                        ,'server.thread_pool':30
                        ,'server.socket_queue_size': 10
                        ,'tools.encode.on': True    #allows unicode not on by default
                        })

cherrypy.quickstart(root, '/', appconf)
    