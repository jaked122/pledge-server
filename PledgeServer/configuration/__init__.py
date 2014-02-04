__author__ = 'awhite'


class Configuration:
    """
    Stores configuration options to control certain aspects of program behavior.
    """
    values = dict()

    def __init__(self):
        import os
        import sys

        sys.path.append(os.getcwd())
        if not os.path.exists("configuration.txt"):
            #load no values
            pass

        else:
            with open("configuration.txt", 'r') as file:
                for f in file:
                    assert isinstance(f, str)
                    #ignore comments using that all powerful character, the Hash sign
                    if f[0] == '#':
                        continue
                    c = f.split(' ')
                    t = c[0]
                    n = c[1]
                    if t == 'int':
                        if len(c) == 3:
                            self.values[n] = int(c[2])
                        else:
                            self.values[n] = list()
                            for i in range(2, len(c)):
                                self.values[n].append(c[i])
                    if t == 'string':
                        tmp = ""
                        for i in range(2, len(c)):
                            tmp += "{0} ".format(c[i])
                        self.values[n] = tmp.replace('\\n', '\n')
                    if t == 'path':
                        #Turn it into a directory name.
                        n = "/" + n
                        p = c[2]
                        #dynamic module loading for the Win.
                        self.values[n] = __import__(p.rstrip('\n'))
                    else:
                        if t == 'string':
                            tmp = ""
                            for i in range(3, len(c)):
                                tmp += "{0} ".format(c[i])
                            self.values[n] = tmp.replace('\\n', '\n')
                            #add content to the sidebar globally in the site.
                        if t == "sidebar":
                            if not "sidebar" in self.values:
                                #initialize the list
                                self.values["sidebar"] = list()
                                #format goes link-text,path
                            self.values["sidebar"].append((n, c[2]))