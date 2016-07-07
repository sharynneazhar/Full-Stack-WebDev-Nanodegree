import os
import re
import jinja2
import webapp2

template_dir = os.path.dirname(__file__)
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

def escape_html(s):
    return cgi.escape(s, quote = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PWD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PWD_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)

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
        self.render("signup.html", error="", username="",
                    password="", verify="", email="")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        v_username = valid_username(username);
        v_password = valid_password(password);
        v_email = valid_email(email);

        if not (username and password and verify):
            self.render("signup.html", error="Missing required fields")
        elif not v_username:
            self.render("signup.html", usernameError="That wasn't a valid username")
        elif not v_password:
            self.render("signup.html", passwordError="That wasn't a valid password")
        elif verify != password:
            self.render("signup.html", verifyError="Passwords do not match")
        elif email and (not v_email):
            self.render("signup.html", emailError="That wasn't a valid email")
        else:
            self.redirect("/welcome?username=" + username)

class WelcomeHandler(Handler):
    def get(self):
        username = self.request.get('username')
        self.render("welcome.html", username=username.capitalize())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler),
], debug = True)
