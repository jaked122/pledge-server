__author__ = 'awhite'
import HTML


def create_message(**kwargs):
    """
    Create a paragraph with desired style and content.
    @param style: An object or type HTML.Attribute_Container,HTML.HTML_Attribute, or a tuple of
     stylename, and value
    @param content: The text or other HTML objects to be ensconced
    @return: the paragraph styled to order.
    """
    fullpage = False
    p = HTML.Paragraph()
    if "style" in kwargs:
        t = kwargs["style"]
        if isinstance(t, HTML.Attribute_Container):
            p.attr = t
        else:
            if isinstance(t, HTML.HTML_Attribute):
                p.add_attribute(t)
            else:
                if isinstance(t, list):
                    for i in t:
                        #Then it is a list of tuples.
                        p.add_attribute(HTML.HTML_Attribute(i[0], i[1]))
                else:
                    assert isinstance(t, tuple)
                    #Then it should be a tuple
                    p.add_attribute(HTML.HTML_Attribute(t[0], t[1]))
    p.add_content(kwargs["content"])
    if "fullpage" in kwargs and kwargs["fullpage"]:
        title = ""
        if "error" in kwargs:
            title = kwargs["error"]
        else:
            title = "Error"
        h = HTML.HTMLSidebarGen(title=title)
        h.content.append(p)
        return h
    else:
        return p


def generate_forms(*args, **kwargs):
    """
    Generate a form with various elements.
    @param args: various fields in tuple form with expectation (field-name,type)
    @return: an HTML.Form object with the requested objects
    @rtype:HTML.Form
    """
    f = HTML.Form()
    p = HTML.Paragraph()
    pagebreak = False
    if "action" in kwargs:
        f.add_attribute(("action", kwargs["action"]))
    if "method" in kwargs:
        f.add_attribute(("method", kwargs["method"]))
    else:
        #I should expect that most forms will use HTTP post
        f.add_attribute(("method", "post"))
    if "pagebreak" in kwargs:
        pagebreak = kwargs['pagebreak']
    for i in args:
        c = HTML.Input(i[1], i[0])
        d = HTML.Label(i[0], i[0])
        #add label followed by its corresponding input.
        p.add_content(d)
        p.add_content(c)
        if pagebreak:
            f.add_content(p)
            p = HTML.Paragraph()
    p.add_content(HTML.Input("submit", "submitbutton"))
    f.add_content(p)
    return f