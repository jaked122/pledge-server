__author__ = 'awhite'


class Configuration:
    """
    Stores configuration options to control certain aspects of program behavior.
    """
    values = dict()

    def __init__(self):
        import os

        if not os.path.exists("configuration.txt"):
            #load no values
            pass
        else:
            with open("configuration.txt") as file:
                for f in iter(file.readline):
                    assert isinstance(f, str)
                    c = f.split(' ')
                    t = c[0]
                    n = c[1]
                    if t == 'int':
                        if len(c) == 3:
                            self.values[n] = int(c[3])
                        else:
                            self.values[n] = list()
                            for i in range(3, len(c)):
                                self.values[n].append(c[i])
                    else:
                        if t == 'string':
                            tmp = ""
                            for i in range(3, len(c)):
                                tmp += "{0} ".format(c[i])
                            self.values[n] = tmp.replace('\\n', '\n')
                            #add content to the sidebar globally in the site.
                        if t == "sidebarcontent":
                            if not "sidebar" in self.values:
                                #initialize the list
                                self.values["sidebar"] = list()
                                #format goes link-text,path
                            self.values["sidebar"].append((n, c[2]))


    def save(self):
        with open("configuration.txt") as file:
            for i in self.values:
                if isinstance(self.values[i], int):
                    file.write("int {0} {1}".format(i, self.values[i]))
                if isinstance(self.values[i], str):
                    tmp = self.values[i].replace("\n", "\\n")
                    file.write("string {0} {1}".format(i, tmp))
