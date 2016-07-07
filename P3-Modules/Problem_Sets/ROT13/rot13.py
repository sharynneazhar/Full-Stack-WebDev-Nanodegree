import os
import jinja2
import webapp2

template_dir = os.path.dirname(__file__)
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    def get(self):
        self.render("rot13.html", text="")

    def post(self):
        textToConvert = self.request.get('text')
        if textToConvert:
            rottedText = textToConvert.encode("rot13")
        self.render("rot13.html", text=rottedText)


app = webapp2.WSGIApplication([('/', MainHandler),
                              ], debug = True)
