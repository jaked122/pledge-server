__author__ = 'awhite'

import time

from HTML import *
import PledgeServer.database


class Memberpage:
    #Set this initially to the UNIX epoch's start date.
    cached = None
    UTC = 0
    message = list()

    def __init__(self, server):
        self.master = server

    def add_pending_message(self, m):
        """
        Add a message to be displayed at the top of the page.
        @param m: The message to be displayed.
        @return: None
        """
        self.message.append(m)

    def retrieve(self, public=True, alumni=False):

        """
        Retrieve the membership list
        @param public: Whether or not to display as a form which may be posted
        @param alumni: Whether or not to include alumni in the return
        """
        needsupdate = False
        db = self.master.database
        assert isinstance(db, PledgeServer.database.Database)
        if (self.cached is None
            or self.UTC - time.time() > 100):

            c = db.get_members()
            self.UTC = time.time()
            h = HTML_Declr()
            head = Head()
            title = Title()
            title.add_content("ASIGPHI members")
            head.add_content(title)
            h.add_content(head)
            b = Body()
            h.add_content(b)
            f = List(ordered=False)

            #Print headers etc.
            while len(self.message) > 0:
                b.add_content(self.message.pop())
            b.add_content(f)
            for i in c:
                quaff = List_Element()
                name, roster, major, graduation, position, bio = i
                center = Centered()
                center.add_content(name)
                tab = Table()
                tab.add_attribute(HTML_Attribute("border", "1"))
                tab.add_row(("Roster", "Major", "Position"))
                tab.add_row((str(roster), major, position))
                quaff.add_content(center)
                quaff.add_content(tab)
                bparagraph = Paragraph()
                bparagraph.add_content(bio)
                quaff.add_content(bparagraph)
                f.add_content(quaff)
            if not public:
                f=Form()
                n=Input("text")
                n.add_attribute(HTML_Attribute("name","n"))
                b=Input("text")
                b.add_attribute()

        return str(h)

