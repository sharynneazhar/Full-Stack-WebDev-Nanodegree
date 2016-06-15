import os
import re
import random
import hashlib
import hmac
import jinja2
import webapp2

from string import letters
from google.appengine.ext import db

# sets the home path to the templates folder
template_dir = os.path.join(os.path.dirname(__file__), 'templates')

# points jinja2 environment to the templates directory with XML/HMTL escape
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(template_dir),
    autoescape=True)

# variables constants
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
SECRET_COOKIE = 'TKLTerO42XkHJ8c'


###################################
#######  GENERAL FUNCTIONS  #######
###################################
def render_env(template, **params):
    """ Gets the project templates and render with props to environment """
    t = jinja_env.get_template(template)
    return t.render(params)


###################################
###### ENCRYPTION FUNCTIONS #######
###################################

def make_secure_val(val):
    """ Pairs the cookie with secret string """
    return '%s|%s' % (val, hmac.new(SECRET_COOKIE, val).hexdigest())

def check_secure_val(secure_val):
    """ Make sure the cookie is valid """
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

def make_salt(length = 5):
    """ Generates a salt to pair with hash keys """
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    """ Salt password if none exist, otherwise create hash """
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    """ Checks if a password is valid """
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)


###################################
######## TEMPLATE HANDLER  ########
###################################

class TemplateHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_tmpl(self, template, **params):
        """ Passes the template and its parameters to jinja environment """
        params['user'] = self.user
        return render_env(template, **params)

    def render(self, template, **kw):
        """ Calls render_templ and render the jinja environment """
        self.write(self.render_tmpl(template, **kw))

    def set_secure_cookie(self, name, val):
        """ Creates a cookie based on a given name and value """
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, cookie):
        """ Returns the value of the cookie itself """
        cookie_val = self.request.cookies.get(cookie)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

class MainPageHandler(TemplateHandler):
    """ Shows all the posts sorted from latest modified first """
    def get(self):
        posts = Post.all().order('-modified')

        if self.user:
            login = '<a href="/logout">hi ' + self.user.name + ', logout</a>'
        else:
            login = '<a href="/login">login</a>'

        self.render('front.html', posts = posts, login = login)

class WelcomePageHandler(TemplateHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', username = self.user.name)
        else:
            self.redirect('/signup')

###################################
########  BLOG MANAGEMENT  ########
###################################

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class Post(db.Model):
    """ Creates an entity to store blog post data in the GAE datastore """
    author = db.StringProperty()
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateProperty(auto_now_add = True)
    modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        """
        Renders blog post to environment
        _render_text replaces return characters with HTML breaks so that
        it renders properly in the browser
        """
        self._render_text = self.content.replace('\n', '<br>')
        return render_env("post.html", p=self)

class Comment(db.Model):
    """ Creates an entity to store comments in the GAE datastore """
    author = db.StringProperty()
    post_id = db.StringProperty(required = True)
    comment = db.TextProperty(required = True)
    created = db.DateProperty(auto_now_add = True)

class NewPostHandler(TemplateHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            self.redirect('/')

        author = self.user.name
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = blog_key(),
                     author = author,
                     subject = subject,
                     content = content)
            p.put()
            post_id = str(p.key().id())
            self.key = post_id
            self.redirect('/%s' % post_id)
        else:
            error = "Please fill in all fields."
            self.render("newpost.html",
                        author = author,
                        subject = subject,
                        content = content,
                        error = error)

class PermalinkHandler(TemplateHandler):
    """ Sends user to the permalink page upon successful post submission """
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        comments = db.GqlQuery("SELECT * FROM Comment "
                               + "WHERE post_id = :1 "
                               + "ORDER BY created DESC",
                               post_id)

        self.render("permalink.html", post = post, comments = comments)

    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(key)

        author = self.user.name
        comment = self.request.get('comment')

        if comment:
            c = Comment(author = author,
                        post_id = post_id,
                        comment = comment)
            c.put()

        # TODO fix the redirect to stay on same page
        # TODO figure out how to refresh the page after post
        self.redirect('/')


class EditPostHandler(TemplateHandler):
    """ Edits blog post """
    def get(self):
        post_id = self.request.get('id')
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(key)

        if self.user.name == post.author:
            self.render('editpost.html', p = post)
        else:
            msg = "You are not authorized to edit this post."
            self.render('message.html', msg = msg)

    def post(self):
        post_id = self.request.get('id')
        new_content = self.request.get('editpost')
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        p = db.get(key)

        if new_content:
            p.content = new_content
            p.put()
            self.redirect('/%s' % post_id)
        else:
            error = "Content cannot be empty."
            self.render("editpost.html", p = p, error = error)

class DeletePostHandler(TemplateHandler):
    """ Delete blog post """
    def get(self):
        post_id = self.request.get('id')
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(key)

        if self.user.name == post.author:
            db.delete(key)
            self.render("message.html", msg = "Post deleted.")
        else:
            msg = "You are not authorized to delete this post."
            self.render('message.html', msg = msg)

###################################
########  USER MANAGEMENT  ########
###################################

def users_key(group = 'default'):
    return db.Key.from_path('users', group)

class User(db.Model):
    """ Creates an entity to store user data in the GAE datastore """
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u

class LoginHandler(TemplateHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/')
        else:
            msg = "Invalid login"
            self.render('login-form.html', error = msg)

class LogoutHandler(TemplateHandler):
    def get(self):
        self.logout()
        self.redirect('/login')


###################################
######## USER REGISTRATION ########
###################################
def valid_username(username):
    return username and USER_RE.match(username)

def valid_password(password):
    return password and PASS_RE.match(password)

def valid_email(email):
    return not email or EMAIL_RE.match(email)

class RegistrationHandler(TemplateHandler):
    """
    Fist validates user information by REGEX
    Then registers user to website
    """

    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username,
                      email = self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError

class SignUpHandler(RegistrationHandler):
    def done(self):
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/welcome')


# GAE app configs
app = webapp2.WSGIApplication([('/?', MainPageHandler),
                               ('/([0-9]+)', PermalinkHandler),
                               ('/newpost', NewPostHandler),
                               ('/edit', EditPostHandler),
                               ('/delete', DeletePostHandler),
                               ('/signup', SignUpHandler),
                               ('/login', LoginHandler),
                               ('/logout', LogoutHandler),
                               ('/welcome', WelcomePageHandler),
                               ], debug = True)
