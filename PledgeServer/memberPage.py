__author__ = 'awhite'

from HTML import *
import PledgeServer.database
import PledgeServer.page
import PledgeServer.server


class MemberPage(PledgeServer.page.Page):
    def __init__(self, server):
        super().__init__(server)

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
        t.add_attribute(("border", "1"))
        #Initialize the table
        t.add_row(["Name", "Roster Number", "Major", "Position", "Graduation Date", "Bio"])
        for i in c:
            t.add_row([i[0], str(i[1]), i[2], i[3], i[4], i[5]])
        b.add_content(t)
        import HTML.Convenience

        form = HTML.Convenience.generate_forms(("Member-name", "text"),
                                               ("Roster-Number", "text"),
                                               ("Major", "text"),
                                               ("Position", "text"),
                                               ("Graduation", "text"),
                                               ("bio", "text"), action="#", pagebreak=True)
        b.add_content(form)
        return h

    def post(self, *args):
        """
        Post new member information.
        @param args: In a tuple (name, roster number, major, house position,graduation, bio
        @return: None
        """
        assert isinstance(args[0], dict)
        a = args[0]
        print(a["Roster-Number"])
        b = (a["Member-name"][0], int(a["Roster-Number"][0]), a["Major"][0], a["Position"][0], a["Graduation"][0],
             a["bio"][0])
        #post to database.
        self.master.database.post_member(b)

        handler = MemberPage
        return self.retrieve()