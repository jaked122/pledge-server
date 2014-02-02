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
            #Create The membership table
            self.db.execute('''CREATE TABLE Members (name TEXT,
                                Roster INTEGER UNIQUE,
                                Major TEXT,
                                position TEXT,
                                graduation TEXT,
                                bio TEXT)''')
            #create the ARTICLE tables. The public boolean should indicate whether or not the article is to be listed
            #when there is no login information supplied.
            self.db.execute('''CREATE VIRTUAL TABLE ARTICLE USING FTS3(
                                ROWID PRIMARY KEY INTEGER,
                                TITLE TEXT,
                                description TEXT,
                                public BOOLEAN)''')
            #And here we are with a user with a password blob.
            self.db.execute('''CREATE TABLE USERS (username TEXT, password BLOB)''')

    def __del__(self):
        self.db.close()
        print("Database closing")

    def vacuum(self):
        if self.numinserts >= 30:
            self.db.execute("VACUUM")
            self.numinserts = 0

    def check_user(self, un, p):
        """
        Checks if the username is in the database
        @param un: the username queried
        @param p: the password for the user
        @return: True or False
        """
        print(un)
        l = self.db.execute("SELECT 1 FROM USERS WHERE username = ?", un)
        c = l.fetchone()
        if c is not None and c[1] == p:
            return True
        else:
            return False

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
        i = self.db.cursor()
        final_list = list()
        #Retrieve the members and sort by their roster number.
        i.execute("SELECT * FROM MEMBERS ORDER BY ROSTER")
        if not includealumni:
            import datetime

            for c in i:
                q = datetime.datetime.strptime(c[4], "%Y")
                if q.year > datetime.datetime.now().year:
                    final_list.append(c)
        else:
            for c in i:
                final_list.append(c)
        return final_list

    def post_user(self, tup):
        assert isinstance(tup, tuple)
        self.db.execute("INSERT INTO USERS VALUES (?,?)", tup)
        self.numinserts += 1
        self.vacuum()

    def post_member(self, tup):
        self.db.execute("INSERT INTO members VALUES (?,?,?,?,?,?)", tup)
        self.numinserts += 1
        self.vacuum()