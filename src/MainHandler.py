#!/usr/bin/env python

import os

from google.appengine.api import users

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):

    def index(self):
        user = users.get_current_user()
        
        if user:
            template_values = {
                'user': user,
                'admin': users.is_current_user_admin(),
                'url': users.create_logout_url(self.request.uri),
                'url_linktext': 'Logout',
            }
        else:
            template_values = {
                'admin': False,
                'url': users.create_login_url(self.request.uri),
                'url_linktext': 'Login',
            }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=MainHandler, handler_method='index', methods=['GET'])
], debug=True)
