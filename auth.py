# coding=UTF-8

# Tornado modules.
import tornado.auth
import tornado.web
import tornado.escape

# Import application modules.
from base import BaseHandler

# General modules.
import logging



class LoginHandler(BaseHandler, tornado.auth.GoogleOAuth2Mixin):
    """
    Handler for logins with Google Open ID / OAuth
    http://www.tornadoweb.org/documentation/auth.html#google
    """
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        elif self.get_argument("start_google_oauth", None):
            # Set users attributes to ask for.
            ax_attrs = ['name', 'email', 'language', 'username']
            self.authenticate_redirect(ax_attrs=ax_attrs)
        elif self.get_argument("start_direct_auth", None):
            # Get form inputs.
            try:
                user = dict()
                user["email"] = self.get_argument("email", default="")
                user["name"] = self.get_argument("name", default="")
            except:
                # Send an error back to client.
                content = "<p>There was an input error. Fill in all fields!</p>"
                self.render_default("index.html", content=content)
            # If user has not filled in all fields.
            if not user["email"] or not user["name"]:
                content = ('<h2>2. Direct Login</h2>' 
                + '<p>Fill in both fields!</p>'
                + '<form class="form-inline" action="/login" method="get"> '
                + '<input type="hidden" name="start_direct_auth" value="1">'
                + '<input class="form-control" type="text" name="name" placeholder="Your Name" value="' + str(user["name"]) + '"> '
                + '<input class="form-control" type="text" name="email" placeholder="Your Email" value="' + str(user["email"]) + '"> '
                + '<input type="submit" class="btn btn-default" value="Sign in">'
                + '</form>')
                self.render_default("index.html", content=content)
            elif str(user.get("name")) == "Bot":
                content = ('<h2>2. Direct Login</h2>' 
                + '<p>Incorrect name Bot, write another!</p>'
                + '<form class="form-inline" action="/login" method="get"> '
                + '<input type="hidden" name="start_direct_auth" value="1">'
                + '<input class="form-control" type="text" name="name" placeholder="Your Name" value="' + str(user["name"]) + '"> '
                + '<input class="form-control" type="text" name="email" placeholder="Your Email" value="' + str(user["email"]) + '"> '
                + '<input type="submit" class="btn btn-default" value="Sign in">'
                + '</form>')
                self.render_default("index.html", content=content)                
            # All data given. Log user in!
            else:
                self._on_auth(user)
            
        else:
            # Logins.
            content = '<div class="page-header"><h1>Login</h1></div>'
            content += ('<h2>1. Google Login</h2>' 
            + '<form action="/login" method="get">' 
            + '<input type="hidden" name="start_google_oauth" value="1">'
            + '<input type="submit" class="btn" value="Sign in with Google">'
            + '</form>')
            content += ('<h2>2. Direct Login</h2>' 
            + '<form class="form-inline" action="/login" method="get"> '
            + '<input type="hidden" name="start_direct_auth" value="1">'
            + '<input class="form-control" type="text" name="name" placeholder="Your Name"> '
            + '<input class="form-control" type="text" name="email" placeholder="Your Email"> '
            + '<input type="submit" class="btn btn-default" value="Sign in">'
            + '</form>')
            content += ('<h2>Instructions</h2>' 
            + '<div>' 
            + '<p>There are 3 base rooms in Chat: Main, Rooms, Help. You can`t write in Rooms and Help.</p>'
            + '<p>If you want to change/create room you have to change url in your browser, after "http..../room/newroom"</p>'
            + '<p>There is command Bot in Chat.  You can`t take name "Bot" but can give him commands.</p>'
            + '<p>!news - Bot will write 10 last news from news.ycombinator.com</p>'
            + '<p>!duck word - write 10 search resuts this word by duckduckgo</p>'
            + '<p>!sum numb1 numb2 ... - write sum=numb1+numb2...</p>'
            + '<p>!mean numb1 numb2 ... - write mean of this numbers</p>'
            + '</div>')            
            self.render_default("index.html", content=content)

    def _on_auth(self, user):
        """
        Callback for third party authentication (last step).
        """
        if not user:
            content = ('<div class="page-header"><h1>Login</h1></div>'
            + '<div class="alert alert-error">' 
            + '<button class="close" data-dismiss="alert">×</button>'
            + '<h3>Authentication failed</h3>'
            + '<p>This might be due to a problem in Tornados GoogleMixin.</p>'
            + '</div>')
            self.render_default("index.html", content=content)
            return None
        
        # @todo: Validate user data.
        # Save user when authentication was successful.
        def on_user_find(result, user=user):
            #@todo: We should check if email is given even though we can assume.
            if result == "null" or not result:
                # If user does not exist, create a new entry.
                self.application.client.set("user:" + user["email"], tornado.escape.json_encode(user))
            else:
                # Update existing user.
                # @todo: Should use $set to update only needed attributes?
                dbuser = tornado.escape.json_decode(result)
                dbuser.update(user)
                user = dbuser
                self.application.client.set("user:" + user["email"], tornado.escape.json_encode(user))
            
            # Save user id in cookie.
            self.set_secure_cookie("user", user["email"])
            self.application.usernames[user["email"]] = user.get("name") or user["email"]
            # Closed client connection
            if self.request.connection.stream.closed():
                logging.warning("Waiter disappeared")
                return
            self.redirect("/")
        
        dbuser = self.application.client.get("user:" + user["email"], on_user_find)
        
        


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect("/")
        
    
