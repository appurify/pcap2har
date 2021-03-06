import urlparse

import dpkt

from .message import Message


class Request(Message):
    '''
    HTTP request. Parses higher-level info out of dpkt.http.Request
    Members:
    * query: Query string name-value pairs. {string: [string]}
    * host: hostname of server.
    * fullurl: Full URL, with all components.
    * url: Full URL, but without fragments. (that's what HAR wants)
    '''

    def __init__(self, tcpdir, pointer):
        super(Request, self).__init__(tcpdir, pointer, dpkt.http.Request)
        # get query string. its the URL after the first '?'
        uri = urlparse.urlparse(self.msg.uri)
        self.host = self.msg.get_header('host') or ''
        fullurl = urlparse.ParseResult('http', self.host, uri.path, uri.params, uri.query, uri.fragment)
        self.fullurl = fullurl.geturl()
        self.url, frag = urlparse.urldefrag(self.fullurl)
        self.query = urlparse.parse_qs(uri.query, keep_blank_values=True)
