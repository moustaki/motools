'''
Created on 2 Apr 2009

@author: kurtjx
'''

import BaseHTTPServer
import artistlookup

class SemWebHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def do_GET(self):
        try: 
            if self.path.startswith('/mbid'):
                mbid = self.path.rsplit('/mbid/')[1]
                print mbid
                lses = artistlookup.LastFMSession()
                lses.authenticate()
                lses.getLastFMdata(mbid)
                
                self.send_header('Content-type', 'application/rdf+xml')
                self.end_headers()
                self.wfile.write(lses.createRDFGraph())
            
            elif self.path.startswith('/'):
                artistname = self.path.rsplit('/')[1]
                lses = artistlookup.LastFMSession(artistname)
                lses.authenticate()
                lses.getLastFMdata()
                
                self.send_header('Content-type', 'application/rdf+xml')
                self.end_headers()
                self.wfile.write(lses.createRDFGraph())
        except:
            self.wfile.write("server error")
    
        return
    

def main():
    try:
        server = BaseHTTPServer.HTTPServer(('', 2059), SemWebHandler)
        print "server started"
        server.serve_forever()
    except:
        server.socket.close()

if __name__ == '__main__':
    main()
            