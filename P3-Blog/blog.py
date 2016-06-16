from lib.base import *

class MainPageHandler(BaseHandler):
    """ Shows all the posts sorted from latest modified first """
    def get(self):
        posts = Post.all().order('-modified')

        if self.user:
            login = '<a href="/logout">hi ' + self.user.name + ', logout</a>'
        else:
            login = '<a href="/login">login</a>'

        self.render('front.html', posts = posts, login = login)

class WelcomePageHandler(BaseHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', username = self.user.name)
        else:
            self.redirect('/signup')

###################################
########  BLOG MANAGEMENT  ########
###################################
class NewPostHandler(BaseHandler):
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

class PermalinkHandler(BaseHandler):
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
        # self.redirect('/%s' % post_id)
        self.redirect('/')

class EditPostHandler(BaseHandler):
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

class DeletePostHandler(BaseHandler):
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
class LoginHandler(BaseHandler):
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

class LogoutHandler(BaseHandler):
    def get(self):
        self.logout()
        self.redirect('/login')

class RegistrationHandler(BaseHandler):
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


url_map = [
    ('/?', MainPageHandler),
    ('/([0-9]+)', PermalinkHandler),
    ('/newpost', NewPostHandler),
    ('/edit', EditPostHandler),
    ('/delete', DeletePostHandler),
    ('/signup', SignUpHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/welcome', WelcomePageHandler),
]

app = webapp2.WSGIApplication(url_map, debug = True)
