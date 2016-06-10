import os
import re
import jinja2
import webapp2

from string import letters
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(template_dir),
    autoescape=True
)

def blog_key(name="default"):
    return db.Key.from_path('blogs', name)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

class BlogFront(Handler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY last_modified DESC LIMIT 10")
        self.render("front.html", posts=posts)

class BlogPostPage(Handler):
    def get(self, post_id):
        key = db.Key.from_path("Post", int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("blogpost.html", post=post)

class NewPostPage(Handler):
    def render_new(self, subject="", content="", error=""):
        self.render("newpost.html", subject=subject, content=content, error=error)

    def get(self):
        self.render("newpost.html")

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            p = Post(parent=blog_key(), subject=subject, content=content)
            p.put()
            self.redirect("/%s" % str(p.key().id()))
        else:
            error = "Please fill out all the fields"
            self.render("newpost.html", subject=subject, content=content, error=error)

app = webapp2.WSGIApplication([
    ('/?', BlogFront),
    ('/([0-9]+)', BlogPostPage),
    ('/newpost', NewPostPage)
], debug = True)
