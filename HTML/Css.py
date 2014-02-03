__author__ = 'awhite'


class CSS_Property:
    def __init__(self, name, value):
        assert isinstance(name, str)
        assert isinstance(value, str)
        self.name = name
        self.value = value

    def __lt__(self, other):
        assert isinstance(other, CSS_Property)
        return self.name<other.name

    def __str__(self):
        from string import Template

        d = dict(name=self.name, value=self.value)
        return Template('\t$name : $value; \n').substitute(d)


class CSSClass:
    def __init__(self, name):
        self.name = name
        self.directives = list()

    def addDirective(self, dir):
        assert isinstance(dir, CSS_Property)
        self.directives.append(dir)
        self.directives.sort()

    def __str__(self):
        from string import Template

        a = ""
        for i in self.directives:
            a += str(i)
        d = dict(name=self.name, content=a)
        return Template("$name{ \n$content\n}").substitute(d)


class Stylesheet:
    def __init__(self):
        self.fmts = list()

    def add_class(self, css):
        assert isinstance(css, CSSClass)
        self.fmts.append(css)

    def __str__(self):
        s = ""
        for i in self.fmts:
            s += u"{0}\n".format(str(i))
        return s