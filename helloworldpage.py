__author__ = "Alexander White"

import PledgeServer.GenericPageGenerator


class handler(PledgeServer.GenericPageGenerator.GenericPage):
    def __init__(self, server):
        super().__init__(server)

    def retrieve(self, title):
        return "hello world"