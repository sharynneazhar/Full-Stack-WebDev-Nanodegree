import os
import re
import jinja2
import webapp2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(template_dir),
    autoescape=True
)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Blog(db.Model):
    created = db.DateProperty(auto_now_add = True)
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)

class NewPostHandler(Handler):
    def render_new(self, subject="", content="", error=""):
        self.render("newpost.html", subject=subject, content=content, error=error)

    def get(self):
        self.render_new()

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            b = Blog(subject=subject, content=content)
            b.put()
            self.redirect("/");
        else:
            error = "Please fill out all the fields"
            self.render_new(subject, content, error=error)

class BlogPostHandler(Handler):
    def get(self):
        blog_id = self.request.get('q')
        blog = Blog.get_by_id(blog_id)
        self.render("blogpost.html", blog=blog)

class MainHandler(Handler):
    def render_front(self, subject="", content="", created=""):
        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
        self.render("front.html", subject=subject, content=content, created=created, blogs=blogs)

    def get(self):
        self.render_front()


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/newpost', NewPostHandler),
    ('/(\d+)', BlogPostHandler)
], debug = True)
