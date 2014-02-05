__author__ = 'awhite'

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib import parse

import PledgeServer.database as dbs
from PledgeServer.memberPage import MemberPage


PledgeServerInstance = None


def setinstance(i):
    global PledgeServerInstance
    PledgeServerInstance = i


class PledgeServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global PledgeServerInstance
        g = MemberPage(PledgeServerInstance)
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
            self.wfile.write("<!DOCTYPE html>\n".encode('utf-8'))
            if authentication_error:
                import HTML.Convenience

                g.add_pending_message(
                    HTML.Convenience.create_message(style=("style", "color:red"),
                                                    content="Error: Login does not exist. Try again."))
            l = str(g.retrieve(public=pub, alumni=False)).encode('utf-8')
            self.wfile.write(l)
        else:
            if query[0] in PledgeServerInstance.config.values:
                c = PledgeServerInstance.config.values[query[0]]
                d = c.handler(PledgeServerInstance)
                self.send_response(200)
                self.send_header("Content-type", d.content_type)
                self.end_headers()
                self.wfile.write(str(d.retrieve(query[0])).encode('utf-8'))

    def do_POST(self):
        global PledgeServerInstance
        query = self.requestline.split(" ")
        print(query[1])
        print(self.requestline)
        if query[1] in PledgeServerInstance.config.values:
            c = PledgeServerInstance.config.values[query[1]]
            if query[1] != '/members':
                d = c.handler(PledgeServerInstance)
            else:
                d = MemberPage(PledgeServerInstance)
            length = int(self.headers["Content-length"])
            postcontent = parse.parse_qs(self.rfile.read(length).decode('utf-8'))
            import sqlite3

            try:
                d.post(postcontent)
                self.send_response(204)
                self.send_header("Content-type", d.content_type)
                self.end_headers()
            except sqlite3.IntegrityError:
                print("Failed somewhere.")
                self.send_response(204)

        else:
            print("No entry found for given path")


class PServer:
    def __init__(self):
        import PledgeServer.configuration as configur

        self.config = configur.Configuration()
        self.database = dbs.Database()
        self.http_server = HTTPServer(('', 8080), PledgeServerHandler)
        setinstance(self)

    def run(self):
        self.http_server.serve_forever()
