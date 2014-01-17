__author__ = 'awhite'
from string import Template

from html import escape


class HTML_Attribute:
    def __init__(self, name, va):
        self.name = name
        self.value = va

    @property
    def __str__(self):
        if not self is None:
            return Template("$name=\"$value\"").substitute(dict(name=self.name, value=self.value))
        return ""


class Attribute_Container:
    def __init__(self):
        self.attr = list()

    def append(self, attr):
        assert issubclass(HTML_Attribute)
        self.attr.append(attr)

    def __str__(self):
        s = ""
        for i in self.attr:
            #add a space because HTML works best that way
            s += str(i) + " "
        return s


class HTML_Element:
    def __init__(self, t="", name=""):
        self.type = t
        self.attr = Attribute_Container()
        self.name = name
        self.content = list()

    def add_attribute(self, attr):
        self.attr.append(attr)

    def add_content(self, content):
        assert isinstance(content, str) or issubclass(content, HTML_Element)
        self.content.append(content)

    def __str__(self):
        content = ""
        for i in self.content:
            content += str(i)
        d = dict(name=self.type, id=self.name, contents=content, style=str(self.attr))
        return Template("<$name id=\"$id\" $style> $contents</$name>").substitute(d)


class Cell(HTML_Element):
    def __init__(self):
        HTML_Element.__init__(self, t="td")


class Row(HTML_Element):
    def __init__(self):
        HTML_Element.__init__(self, t="tr")

    def __str__(self):
        return super().__str__()


class Table(HTML_Element):
    def __init__(self):
        HTML_Element.__init__(self, t="Table")

    def add_row(self, asc):
        #List for storing the "Corrected" contents
        c = list()
        #Check that the elements of the list are HTML elements or strings
        d = Row()
        for i in asc:

            q = i
            if isinstance(i, str):
                q = Cell()
                q.add_content(escape(i))
            else:
                q = Cell()
                q.add_content(i)
            c.append(q)

            d.content.append(q)
        self.content.append(d)


    def getCell(self, row, col):
        return self.rows[row][col]

    def setCell(self, row, col, content):
        self.content[row].content[col].content = content

class Body(HTML_Element):
    def __init__(self):
        HTML_Element.__init__(self,"body")

class Paragraph(HTML_Element):
    def __init__(self):
        HTML_Element.__init__(self,"p")

class Title(HTML_Element):
    def __init__(self):
        HTML_Element.__init__(self,t="title")

    def add_content(self,content):
        assert isinstance(content,str)
        self.content.append(content)