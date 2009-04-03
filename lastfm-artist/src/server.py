'''
Created on 2 Apr 2009

A really simple python webserver to implement linked data - style 
303 redirects and last.fm lookups

@author: kurtjx
'''

import BaseHTTPServer
import artistlookup

PORT = 2059
HOST_BASE = "http://localhost:"+str(PORT)
#HOST_BASE = "http://dbtune.org/sandbox"


class SemWebHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def do_HEAD(self):
        self.send_response(303)
        self.send_header("Location", HOST_BASE+self.path+'.rdf')
        self.end_headers()
            
    
    def do_GET(self):
        try:
            if self.path.startswith('/mbid') and not self.path.endswith('.rdf'):
                self.do_HEAD()
                
            elif self.path.startswith('/mbid') and self.path.endswith('.rdf'):
                mbid = self.path.rsplit('/mbid/')[1].rsplit('.rdf')[0]
                
                # set the headers
                self.resp200()
                
                lses = artistlookup.LastFMSession()
                lses.authenticate()
                lses.getLastFMdata(mbid)
                
                
                self.wfile.write(lses.createRDFGraph())
                #return
            
            elif self.path.startswith('/') and not self.path.endswith('.rdf'):
                self.do_HEAD()
            
            elif self.path.startswith('/') and self.path.endswith('.rdf'):
                artistname = self.path.rsplit('/')[1].rsplit('.rdf')[0]
                
                # set the headers
                self.resp200()
                
                lses = artistlookup.LastFMSession(artistname)
                lses.authenticate()
                lses.getLastFMdata()
                
                #self.send_header('Content-type', 'application/rdf+xml')
                #self.end_headers()
                self.wfile.write(lses.createRDFGraph())
                
            else:
                self.wfile.write("invalid URI")

        except Exception:
            self.wfile.write("internal server error")
        #return
        
    def resp200(self):
        '''return 200 ok headers and rdf/xml'''
        self.send_response(200)
        self.send_header('Content-type', 'application/rdf+xml')
        self.end_headers()


def main():
    try:
        server = BaseHTTPServer.HTTPServer(('', PORT), SemWebHandler)
        print "server started"
        server.serve_forever()
    except:
        server.socket.close()

if __name__ == '__main__':
    main()
            