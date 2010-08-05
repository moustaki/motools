'''
Created on Jul 20, 2010

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

import sys, os
import cherrypy
import RDF
import echonest2rdf
from rdf2html import rdf2html
import settings

f = open('static/index.html','r')
INDEX_HTML = f.read()
f.close()

def set_namespaces(ser):
    ser.set_namespace('sim','http://purl.org/ontology/similarity/')
    ser.set_namespace('mo','http://purl.org/ontology/mo/')
    ser.set_namespace('foaf', 'http://xmlns.com/foaf/0.1/')

class RDFServer:
    ''' content neg and serve RDF'''
    
    @cherrypy.expose
    def index(self):
        return INDEX_HTML
    
    @cherrypy.expose
    def default(self, urlpath):
        if urlpath.startswith('method'):
            if urlpath.endswith('.rdf'):
                cherrypy.response.headers['Content-Type'] = 'application/rdf+xml'
                ser = RDF.RDFXMLSerializer()
                return ser.serialize_model_to_string(echonest2rdf.method, None)
            
            elif urlpath.endswith('.ttl'):
                cherrypy.response.headers['Content-Type'] = 'text/n3'
                ser = RDF.TurtleSerializer()
                return ser.serialize_model_to_string(echonest2rdf.method, None)
            
            elif urlpath.endswith('.html'):
                cherrypy.response.headers['Content-Type'] = 'text/html'
                return echonest2rdf.method_html
            else:
                accept = cherrypy.tools.accept.callable(['text/html', 'text/plain','application/rdf+xml','text/n3']) #@UndefinedVariable
                if accept== 'text/html' or accept=='text/plain': 
                    raise cherrypy.HTTPRedirect(settings.URI_BASE+urlpath+'.html')
                elif accept == 'application/rdf+xml' : 
                    raise cherrypy.HTTPRedirect(settings.URI_BASE+urlpath+'.rdf')
                elif accept == 'text/n3' : 
                    raise cherrypy.HTTPRedirect(settings.URI_BASE+urlpath+'.ttl')
        else:
            raise cherrypy.HTTPError(status=404, message="what you're looking for isn't here.")
        
    @cherrypy.expose
    def mbid(self, urlpath):
        if urlpath.endswith('.rdf'):
            cherrypy.response.headers['Content-Type'] = 'application/rdf+xml'
            model = echonest2rdf.get_similar(urlpath.split('.rdf')[0])
            ser = RDF.RDFXMLSerializer()
            return ser.serialize_model_to_string(model, None)
        
        elif urlpath.endswith('.ttl'):
            cherrypy.response.headers['Content-Type'] = 'text/n3'
            model = echonest2rdf.get_similar(urlpath.split('.ttl')[0])
            ser = RDF.TurtleSerializer()
            return ser.serialize_model_to_string(model, None)
        
        elif urlpath.endswith('.html'):
            cherrypy.response.headers['Content-Type'] = 'text/html'
            mbid = urlpath.split('.html')[0]
            return rdf2html(echonest2rdf.get_similar(mbid),mbid)

        
        else:
            accept = cherrypy.tools.accept.callable(['text/html', 'text/plain','application/rdf+xml','text/n3']) #@UndefinedVariable
            if accept== 'text/html' or accept=='text/plain': 
                raise cherrypy.HTTPRedirect(settings.URI_BASE+'mbid/'+urlpath+'.html')
            elif accept == 'application/rdf+xml' : 
                raise cherrypy.HTTPRedirect(settings.URI_BASE+'mbid/'+urlpath+'.rdf')
            elif accept == 'text/n3' : 
                raise cherrypy.HTTPRedirect(settings.URI_BASE+'mbid/'+urlpath+'.ttl')
    
            
        

# setup some static files for js, css, etc
home_config = {'/':
               {'tools.sessions.on': True,
                #'tools.auth.on': True,
                'tools.proxy.on':True,
                #'tools.encode.on': True,
                #'tools.decode.on': True,
                #'tools.caching.on': True
                },
               '/images':
                {'tools.staticdir.on':True,
                 'tools.staticdir.dir': os.path.join(os.path.abspath(''), 'static','img'),
                 #'tools.caching.on': True
                 },
               '/css':
                {'tools.staticdir.on':True,
                 'tools.staticdir.dir': os.path.join(os.path.abspath(''), 'static','css'),
                 #'tools.caching.on': True 
                 },
                '/js':
                {'tools.staticdir.on':True,
                 'tools.staticdir.dir': os.path.join(os.path.abspath(''), 'static','js'),
                 #'tools.caching.on': True
                 }
               }

# hard code config here
cherrypy.config.update({
                        'server.socket_port': settings.PORT,
                        'server.socket_host': settings.HOST,
                        'log.screen': True 
                        })

# mount each application
cherrypy.tree.mount(RDFServer(),'/', home_config)

# actually start cherrypy
if hasattr(cherrypy.engine, 'block'):
    cherrypy.engine.start()
    cherrypy.engine.block()
else:
    print "Appears cherrypy version < 3.1, please upgrade"
    sys.exit(1)