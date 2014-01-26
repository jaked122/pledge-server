__author__ = 'awhite'

import time

from HTML import *
import PledgeServer.database


class Memberpage:
    #Set this initially to the UNIX epoch's start date.
    cached = None
    UTC = 0

    def __init__(self, server):
        self.master = server


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
            f = List(ordered=False)
            if public:
                for i in c:
                    quaff = List_Element()
                    name, roster, major, position, bio = i
                    center = Centered()
                    center.add_content(name)
                    tab = Table()
                    tab.add_row(("Roster", "Major", "Position"))
                    tab.add_row((str(roster), major, position))
                    quaff.add_content(center)
                    quaff.add_content(tab)
                    

            else:
                pass

