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
                    assert isinstance(t,tuple)
                    #Then it should be a tuple
                    p.add_attribute(HTML.HTML_Attribute(t[0], t[1]))
    p.add_content(kwargs["content"])
    return p