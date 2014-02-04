__author__ = "Alexander White"

import PledgeServer.GenericPageGenerator

#This is an example of how to properly use the GenericPageGenerator interface as well as
#A working example of how it should or can work.
#In general, you need to call it handler, so that python will find it easily.
class handler(PledgeServer.GenericPageGenerator.GenericPage):
    def __init__(self, server):
        super().__init__(server)

    def retrieve(self, title):
        return "hello world"