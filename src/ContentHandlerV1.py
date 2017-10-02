#!/usr/bin/env python

import os

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class ContentHandlerV1(webapp2.RequestHandler):

    def content(self, item):
        template = JINJA_ENVIRONMENT.get_template(item + ".html")
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    webapp2.Route(r'/v1/content/<item>', handler=ContentHandlerV1, name='item', handler_method='content', methods=['GET'])
], debug=True)
