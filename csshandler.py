__author__ = 'awhite'


class Handler:
    def retrieve(self):
        import HTML.Css as css

        body = css.CSSClass("body")
        body.add_directive(css.CSS_Property("background-color", "#A0A000"))
        return body
