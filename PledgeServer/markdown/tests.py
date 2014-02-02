__author__ = 'awhite'

import PledgeServer.markdown as markdown

g = markdown.MarkdownParser()
h = g.parse("""I wonder

If *this* is |real|.""")
print(h)
for i in h:
    print(str(i))