__author__ = 'awhite'


class CSS_Property:
    def __init__(self, name, value):
        assert isinstance(name, str)
        assert isinstance(value, str)
        self.name = name
        self.value = value

    def __str__(self):
        from string import Template

        d = dict(name=self.name, value=self.value)
        return Template("$name = $value \n").substitute(d)


class CSS_Class:
    def __init__(self, name):
        self.name = name
        self.directives = list()

    def addDirective(self, dir):
        assert isinstance(dir, CSS_Property)
        self.directives.append(dir)

    def __str__(self):
        from string import Template

        a = ""
        for i in self.directives:
            a += str(i)
        d = dict(name=self.name, content=a)
        return Template("$name{ \n $content \n }").substitute(d)


class Stylesheet:
    def __init__(self):
        self.fmts = list()

    def add_class(self, css):
        assert isinstance(css, CSS_Class)
        self.fmts.append(css)