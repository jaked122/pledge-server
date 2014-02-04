__author__ = 'awhite'

from HTML import *
import PledgeServer.database
import PledgeServer.page
import PledgeServer.server


class Memberpage(PledgeServer.page.Page):
    def __init__(self, server):
        PledgeServer.page.Page.__init__(self, server)


    def retrieve(self, public=True, alumni=False):
        """
        Retrieve the membership list
        @param public: Whether or not to display as a form which may be posted
        @param alumni: Whether or not to include alumni in the return
        """
        assert isinstance(self.master, PledgeServer.server.PServer)
        h = super().retrieve("Members")
        b = h.page_content
        db = self.master.database
        assert isinstance(db, PledgeServer.database.Database)
        c = db.get_members()
        t = Table()
        t.add_attribute(("border","1"))
        #Initialize the table
        t.add_row(["Name", "Roster Number", "Major", "Position", "Graduation Date", "Bio"])
        for i in c:
            t.add_row([i[0], str(i[1]), i[2], i[3], i[4], i[5]])
        b.add_content(t)
        return h


