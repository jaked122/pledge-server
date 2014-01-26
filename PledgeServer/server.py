__author__ = 'awhite'

import PledgeServer.database
class PledgeServer:
    def __init__(self):
        self.database=PledgeServer.database.Database()