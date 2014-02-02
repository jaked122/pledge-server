__author__ = 'awhite'
from string import Template

from html import escape


class HTML_Attribute:
    def __init__(self, name, va):
        self.name = name
        self.value = va


    def __str__(self):
        return Template('$name="$value"').substitute(dict(name=self.name, value=self.value))


class Attribute_Container:
    def __init__(self):
        self.attr = list()

    def append(self, attr):
        assert isinstance(attr, HTML_Attribute)
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
        """
        Add an attribute to the HTML element
        @param attr: Either a tuple with (name,value) or a HTML_Element
        @return: None
        """
        if isinstance(attr, HTML_Attribute):
            self.attr.append(attr)
        else:
            assert isinstance(attr, tuple)
            self.attr.append(HTML_Attribute(attr[0], attr[1]))

    def add_content(self, content):
        assert isinstance(content, str) or issubclass(type(content), HTML_Element)
        assert not isinstance(content, HTMLDeclr)
        self.content.append(content)

    def __str__(self):
        content = ""
        for i in self.content:
            content += str(i)
        d = dict(name=self.type, id=self.name, contents=content, style=str(self.attr))
        if self.name != "":
            return Template("<$name id=\"$id\" $style> \n$contents\n</$name>").substitute(d)
        else:
            if len(self.attr.attr) == 0:
                return Template("<$name>\n $contents \n</$name>").substitute(d)
            return Template("<$name $style>\n $contents\n</$name>").substitute(d)


class Cell(HTML_Element):
    def __init__(self):
        HTML_Element.__init__(self, t="td")


class Row(HTML_Element):
    def __init__(self):
        HTML_Element.__init__(self, t="tr")


class Table(HTML_Element):
    def __init__(self):
        HTML_Element.__init__(self, t="table")

    def add_row(self, asc):
        """
        Add a row to the table. Creates a row Object and Cell objects for all
        of the contents of the list
        @param asc: The list of things which are to be added.
        """
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
        """
        Get a cell from the table for manipulation.
        @rtype : Cell
        """
        return self.content[row].content[col]

    def setCell(self, row, col, content):
        self.content[row].content[col].content = content


class Body(HTML_Element):
    def __init__(self):
        HTML_Element.__init__(self, "body")


class Paragraph(HTML_Element):
    def __init__(self):
        HTML_Element.__init__(self, "p")


class FormattedText(HTML_Element):
    def __init__(self, fmt):
        assert isinstance(fmt, str)
        HTML_Element.__init__(self, fmt)



class Bold(FormattedText):
    def __init__(self):
        FormattedText.__init__(self, "b")



class Italic(FormattedText):
    def __init__(self):
        FormattedText.__init__(self, "i")


class Underline(FormattedText):
    def __init__(self):
        FormattedText.__init__(self, "u")


class Anchor(HTML_Element):
    def __init__(self, href):
        HTML_Element.__init__(self, "a")
        self.attr.append(HTML_Attribute("href", href))


class Header(HTML_Element):
    def __init__(self, level):
        HTML_Element.__init__(self, "h{0}".format(str(level)))


class HTMLDeclr(HTML_Element):
    def __init__(self):
        HTML_Element.__init__(self, "html")

    def add_content(self, content):
        if isinstance(content, Head):
            #The head should generally be the first element.
            self.content.insert(0, content)
        else:
            #Otherwise let the superclass handle it.
            HTML_Element.add_content(self, content)

    def get_body(self):
        """
        Get the body Element of the HTML page
        @return: the Body of the html page, or None in case it does not exist.
        """
        for i in self.content:
            if isinstance(i, Body):
                return i
        return None

    def get_head(self):
        """
        Get the head of the HTML element, or None, in case it doesn't exist.
        @return: The head, or none should it not exist.
        """
        for i in self.content:
            if isinstance(i, Head):
                return i
        return None


class Head(HTML_Element):
    def __init__(self):
        HTML_Element.__init__(self, "head")
        h = HTML_Element(t="meta")
        h.add_attribute(("http-equiv", "Content-Type"))
        h.add_attribute(("content", "text/html"))
        self.add_content(h)

    def add_content(self, content):
        super().add_content(content)


class Title(HTML_Element):
    def __init__(self):
        HTML_Element.__init__(self, t="title")

    def add_content(self, content):
        assert isinstance(content, str)
        self.content.append(content)


class Form(HTML_Element):
    def __init__(self):
        HTML_Element.__init__(self, t="form")


class Input(HTML_Element):
    def __init__(self, type, name):
        HTML_Element.__init__(self, t="text")
        assert type in ["text", "submit"]
        self.add_attribute(HTML_Attribute("name", name))


class List_Element(HTML_Element):
    def __init__(self):
        HTML_Element.__init__(self, "li")


class List(HTML_Element):
    def __init__(self, ordered=False):
        if ordered:
            HTML_Element.__init__(self, "ol")
        else:
            HTML_Element.__init__(self, "ul")

    def add_content(self, content):
        if not isinstance(content, List_Element):
            i = List_Element()
            i.add_content(content)
            self.content.append(i)
        else:
            self.content.append(content)


class Centered(HTML_Element):
    def __init__(self):
        HTML_Element.__init__(self, "center")