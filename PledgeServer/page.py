__author__ = 'awhite'

from HTML import *


class Page:
    master = None

    def __init__(self, server):
        self.master = server
        self.message = list()

    def add_pending_message(self, m):
        """
        Add a message to be displayed at the top of the page.
        @rtype : NoneType
        @param m: The message to be displayed.
        @return: None
        """
        self.message.append(m)

    def retrieve(self, title=""):
        """
        Obtain a webpage with default content with the messages and elements found in the
        message queue
        @rtype : HTMLSidebarGen
        @return: An HTMLSidebarGen with the properties specified
        """
        h = HTMLSidebarGen(title=title)
        for i in self.message:
            h.page_content.add_content(i)
        if "sidebar" in self.master.config.values:
            v = self.master.config.values["sidebar"]
            for c in v:
                i = Anchor(c[1])
                i.add_content(c[0])
                h.sidebar.add_content(i)
        return h
