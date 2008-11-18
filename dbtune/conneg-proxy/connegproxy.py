import mimeparse
from httplib import HTTPConnection
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

host = 'localhost'
port = 8001

representations = [
        'application/rdf+xml',
        'image/gif',
        'text/css',
        'text/html',
        'application/json',
        'application/atom+xml',
        'text/calendar',
        'audio/x-pn-realaudio',
        'application/rss+xml',
        'text/plain',
        'text/vnd.wap.wml',
        'application/x-yaml',
        'application/xml'
    ]

class ConnegHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print self.headers
        accept = self.__parse_accept(self.headers.get('Accept'))
        print accept
        con = HTTPConnection(host,port)
        headers = {
            "Accept": accept,
            "User-Agent": self.headers.get('User-Agent'),
            "Host": self.headers.get('Host'),
            "Accept-Language": self.headers.get('Accept-Language'),
            "Accept-Encoding": self.headers.get('Accept-Encoding'),
            "Accept-Charset": self.headers.get('Accept-Charset'),
            "Keep-Alive": self.headers.get('Keep-Alive'),
            "Connection": self.headers.get('Connection'),
            "Cache-Control": self.headers.get('Cache-Control')
        }
        con.request("GET",self.path,None,headers)

    def __parse_accept(self,accept):
        return mimeparse.best_match(representations, accept)


def main():
    try:
        server = HTTPServer(('',8000), ConnegHandler)
        print "Started content negotiation proxy..."
        server.serve_forever()
    except KeyboardInterrupt:
        print "^C received, shutting down content negotiation proxy"
        server.socket.close()
    

if __name__ == '__main__':
    main()

