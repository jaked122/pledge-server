__author__ = 'awhite'
import HTML as h

c=h.HTMLSidebarGen("I'm a page")
a=h.Anchor("google.com")
a.add_content("google.com")
c.sidebar.add_content(a)
c.page_content.add_content("I'm here too.")
c.sidebar_style.content.fmts[0].add_directive(("background-color","gray"))
print(str(c))