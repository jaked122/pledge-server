__author__ = 'awhite'


class MarkdownParser:
    """
    Simplistic Markdown support for people who like it.
    """
    bold_char = '|'
    italic_char = '*'
    underline_char = '_'
    reserved_characters = ['\n', italic_char, bold_char, underline_char]

    def __init__(self, options=(True, True, True, True)):
        assert isinstance(options, tuple)
        self.allow_headers = options[0]
        self.allow_emphasis = options[1]
        self.allow_underline = options[2]

    def parse(self, s):
        """
        Parse markdown.
        @param s: A string consisting entirely out of markdown
        @return: a collection of HTML objects.
        @rtype:list
        """
        import HTML
        #The content that is probably going to be output.
        content = list()
        underline = False
        bold = False
        italic = False
        consecutive_newlines = 0
        buffer = ""
        #Stack containing objects that it might need to reference
        lastobject = list()
        for i in s:
            if not i in self.reserved_characters:
                #Reset the newline count
                consecutive_newlines = 0
                #Simply add to the buffer. Nothing more.
                buffer += i
            else:
                if i == self.bold_char:
                    if len(lastobject) == 0:
                        lastobject.append(HTML.Paragraph())
                        lastobject[len(lastobject) - 1].add_content(buffer)
                    if not bold:
                        bold = True
                        #add the content to the last object
                        lastobject[len(lastobject) - 1].add_content(buffer)
                        #Create a new Bold statement and add to the stack
                        lastobject.append(HTML.Bold())
                        buffer = ""
                    else:
                        bold = False
                        lastobject[len(lastobject) - 1].add_content(buffer)
                        lastobject[len(lastobject) - 2].add_content(lastobject.pop())
                        #reset the buffer once again.
                        buffer = ""
                if i == self.italic_char:
                    if len(lastobject) == 0:
                        lastobject.append(HTML.Paragraph())
                        lastobject[len(lastobject) - 1].add_content(buffer)
                    if not italic:
                        italic = True
                        lastobject.append(HTML.Italic())
                        buffer = ""
                    else:
                        italic = False
                        lastobject[len(lastobject) - 1].add_content(buffer)
                        lastobject[len(lastobject) - 2].add_content(lastobject.pop())
                        buffer = ""
                if i == '\n':
                    consecutive_newlines += 1
                    if consecutive_newlines >= 2:
                        if len(lastobject) == 0:
                            lastobject.append(HTML.Paragraph())
                        lastobject[0].add_content(buffer)
                        buffer = ""
                        content.append(lastobject[0])
                        lastobject.clear()
        if len(lastobject) != 0:
            lastobject[0].add_content(buffer)
            content.append(lastobject[0])
        return content