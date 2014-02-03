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
        @rtype : HTMLDeclr
        @return: An HTMLDeclr with the properties specified
        """
        h = HTMLDeclr()
        j = Head()
        t = Title()
        t.add_content(title)
        j.add_content(t)
        h.add_content(j)
        b = Body()
        for i in self.message:
            b.add_content(i)
        h.add_content(b)
        return h
