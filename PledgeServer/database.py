__author__ = 'awhite'
import sqlite3


class Database:
    numinserts = 0

    def __init__(self):
        createtables = False
        import os

        if not os.path.exists("Pledge.db"):
            createtables = True
        self.db = sqlite3.connect("Pledge.db")
        if createtables:
            self.db.execute('''CREATE TABLE Members (name TEXT,
                                Roster INTEGER UNIQUE,
                                Major TEXT,
                                position TEXT,
                                graduation TEXT,
                                bio TEXT)''')
            self.db.execute('''CREATE VIRTUAL TABLE ARTICLE USING FTS3(
                                ROWID PRIMARY KEY INTEGER,
                                TITLE TEXT,
                                description TEXT,
                                public BOOLEAN)''')
            self.db.execute('''CREATE TABLE USERS (username TEXT, password BLOB)''')

    def __del__(self):
        self.db.close()
        print("Database closing")

    def vacuum(self):
        if self.numinserts >= 30:
            self.db.execute("VACUUM")
            self.numinserts = 0

    def get_page(self, indice):
        cur = self.db.cursor()
        i = (indice)
        cur.execute("SELECT 1 FROM ARTICLE WHERE ROWID = ?", i)
        return cur.fetchone()

    def post_page(self, name, roster, major, position, graduation, bio=""):
        tup = (name, roster, major, position, graduation, bio)
        self.db.execute("INSERT INTO ARTICLE(title,description,public) VALUES (?,?,?)", tup)
        self.numinserts += 1
        self.vacuum()

    def get_members(self, includealumni=False):
        i=self.db.cursor()
        finallist=list()
        i.execute("Select * from MEMBERS")
        if not includealumni:
            import datetime
            for c in i:
                q=datetime.datetime.strptime(c[4],"%Y")
                if q.year>datetime.datetime.now().year:
                    finallist.append(c)
        else:
            for c in i:
                finallist.append(c)
        return finallist

    def post_user(self, tup):
        assert isinstance(tup, tuple)
        self.db.execute("INSERT INTO USERS VALUES (?,?)", tup)
        self.numinserts += 1
        self.vacuum()

    def post_member(self, tup):
        self.db.execute("INSERT INTO members VALUES (?,?,?,?,?,?)", tup)
        self.numinserts += 1
        self.vacuum()