__author__ = 'awhite'

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib import parse

import PledgeServer.database as dbs
from PledgeServer.memberpage import Memberpage


PledgeServerInstance = None


def setinstance(i):
    global PledgeServerInstance
    PledgeServerInstance = i


class PledgeServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global PledgeServerInstance
        g = Memberpage(PledgeServerInstance)
        query = self.path.split('?')
        #self.send_header("Content-Type", "text/html")
        self.send_response(200)
        #self.end_headers()
        h = parse.urlparse(self.requestline)
        m = parse.parse_qs(h.query)

        if query[0] == "/members":
            pub = False
            authentication_error = False
            if m["public"] is not None:
                if m["user"] is not None:
                    #check that the authentication is correct
                    pub = not PledgeServerInstance.database.check_user(m["user"], m["password"])
                    authentication_error = True

            self.wfile.write("<!DOCTYPE html>\n".encode('utf-8'))
            if authentication_error:
                import HTML.Convenience

                g.add_pending_message(
                    HTML.Convenience.create_message(style=("style", "color:red"),
                                                    content="Error: Login does not exist. Try again."))
            l = g.retrieve(public=pub, alumni=False).encode('utf-8')

            self.wfile.write(l)


class PServer:
    def __init__(self):
        self.database = dbs.Database()
        self.http_server = HTTPServer(('', 8080), PledgeServerHandler)
        setinstance(self)

    def run(self):
        self.http_server.serve_forever()
