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
        #The response must be sent first.

        h = parse.urlparse(self.requestline)
        m = parse.parse_qs(h.query)

        if query[0] == "/members":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            pub = False
            authentication_error = False
            if "public" in m:
                if "user" in m:
                    #check that the authentication is correct
                    pub = not PledgeServerInstance.database.check_user(m["user"], m["password"])
                    authentication_error = True

            self.wfile.write("<!DOCTYPE html>\n".encode('utf-8'))
            if authentication_error:
                import HTML.Convenience

                g.add_pending_message(
                    HTML.Convenience.create_message(style=("style", "color:red"),
                                                    content="Error: Login does not exist. Try again."))
            l = str(g.retrieve(public=pub, alumni=False)).encode('utf-8')
            if query[0] == "/css":
                self.send_response(200)
                self.send_header("Content-type", "stylesheet/css")
                self.end_headers()
            self.wfile.write(l)


class PServer:
    def __init__(self):
        self.database = dbs.Database()
        self.http_server = HTTPServer(('', 8080), PledgeServerHandler)
        setinstance(self)

    def run(self):
        self.http_server.serve_forever()
