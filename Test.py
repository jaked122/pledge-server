__author__ = 'awhite'
import sqlite3

import HTML


a = HTML.Anchor("HTTP://Google.com")
a.add_content("Here's google")
c = HTML.Table()
d = ["Hello", "Goodbye", a]
c.add_row(d)

print(str(c))
e = HTML.Paragraph()
e.add_content("Hellow there.")
c.getCell(0, 1).add_content(e)
c.getCell(0, 1).name = "Hellow"
print(str(c))
try:
    able = HTML.HTML_Declr()
    able.add_content(able)
except:
    print("HTML declaration nesting prevented")

import HTML.Css

goober = HTML.Css.Stylesheet()
gobbler = HTML.Css.CSS_Class("body")
goober.add_class(gobbler)
gobbler.addDirective(HTML.Css.CSS_Property("border", "Dashed solid solid Dash"))
gobbler.addDirective(HTML.Css.CSS_Property("color", "#0FC0D0"))
print(str(goober))

createtables = False
import os

if not os.path.isfile("Hello.db"):
    createtables = True
cd = sqlite3.connect("Hello.db")

if createtables:
    cd.execute("CREATE VIRTUAL TABLE vfs USING fts3(title,keywords,condom,body)")
cd.execute("INSERT INTO vfs VALUES('title','keywords','condom','body')")
cd.close()
import http.server as server


class Custom_handler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.request
        c = HTML.HTML_Declr()
        b = HTML.Body()
        p = HTML.Paragraph()
        p.add_content("Hello from ASIGPHI server")
        i=HTML.HTML_Attribute("style","background-color:red")
        p.add_attribute(i)
        b.add_content(p)
        c.add_content(b)
        gh = str(c)
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(gh, "UTF-8"))



http = server.HTTPServer(("", 8001), Custom_handler)
http.serve_forever()
