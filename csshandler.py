__author__ = 'awhite'
import PledgeServer.GenericPageGenerator


class Handler(PledgeServer.GenericPageGenerator.GenericPage):
    content_type = "text/css"

    def retrieve(self, title=""):
        import HTML.Css as css

        body = css.CSSClass("body")
        body.add_directive(css.CSS_Property("background-color", "#A0A000"))
        return body
