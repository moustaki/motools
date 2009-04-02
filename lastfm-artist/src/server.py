'''
Created on 2 Apr 2009

@author: kurtjx
'''

import BaseHTTPServer
import artistlookup

class SemWebHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def do_GET(self):
        #try:
            if self.path.startswith('/mbid') and not self.path.endswith('.rdf'):
                self.send_response(303, 'http://localhost:2059/'+self.path+'.rdf')
                #return
            elif self.path.startswith('/mbid') and self.path.endswith('.rdf'):
                mbid = self.path.rsplit('/mbid/')[1].rsplit('.rdf')[0]
                lses = artistlookup.LastFMSession()
                lses.authenticate()
                lses.getLastFMdata(mbid)
                
                #self.send_header('Content-type', 'application/rdf+xml')
                #self.end_headers()
                self.wfile.write(lses.createRDFGraph())
                #return
            
            elif self.path.startswith('/'):
                artistname = self.path.rsplit('/')[1]
                lses = artistlookup.LastFMSession(artistname)
                lses.authenticate()
                lses.getLastFMdata()
                
                #self.send_header('Content-type', 'application/rdf+xml')
                #self.end_headers()
                self.wfile.write(lses.createRDFGraph())
                #return
        #except Exception:
            
        #    self.wfile.write("server error")
        #return


def main():
    try:
        server = BaseHTTPServer.HTTPServer(('', 2059), SemWebHandler)
        print "server started"
        server.serve_forever()
    except:
        server.socket.close()

if __name__ == '__main__':
    main()
            