#!/usr/bin/env python

import os
import urllib
import json
import dateutil.parser

from google.appengine.api import users
from google.appengine.ext import ndb

from datetime import timedelta, date

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#DEFAULT_GROUP_NAME = 'public_koerperwerte_group'

#def daterange(start_date, end_date):
#    for n in range(int ((end_date - start_date).days)):
#        yield start_date + timedelta(n)
#
#def format_weight(weight):
#    if weight == 0:
#        return '00,0'
#    else:
#        return ('0' if weight < 10 else '') + str(weight / 10.0).replace('.', ',')

# We set a parent key on the 'Weighings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

#def koerperwerte_key(group_name=DEFAULT_GROUP_NAME):
#    """Constructs a Datastore key for a Koerperwerte entity.
#
#    We use group_name as the key.
#    """
#    return ndb.Key('Koerperwerte', group_name)

#class Person(ndb.Model):
#    identity = ndb.StringProperty(indexed=False)
#    email = ndb.StringProperty(indexed=False)

#class Weighing(ndb.Model):
#    person = ndb.StructuredProperty(Person)
#    datum = ndb.DateProperty(indexed=True)
#    weight = ndb.IntegerProperty(indexed=False)
#    created = ndb.DateTimeProperty(auto_now_add=True)

#class Day:
#    def __init__(self, datum = date.today()):
#        self.datum = datum
#        self.entries = {}
#    
#    def __str__(self):
#        user_string = ''
#        for identity,value in self.users:
#            user_string = user_string + identity + ' (' + str(value) + ') '
#        
#        return 'Day(' + str(self.datum) + ', ' + user_string
#    
#    def add_entry(self, identity, weight):
#        self.entries[identity] = weight

class Newsletterman(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        
        if user:
            template_values = self.template_values_with_user(user)
        else:
            template_values = {
                'group_name': urllib.quote_plus(self.request.get('group_name', DEFAULT_GROUP_NAME)),
                'url': users.create_login_url(self.request.uri),
                'url_linktext': 'Login',
            }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
    
    def template_values_with_user(self, user):
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        
        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
        }

        return template_values
    
#class Newsletterman(webapp2.RequestHandler):
#
#    def post(self):
#        weight_request = json.loads(self.request.body)
#        datum = dateutil.parser.parse(weight_request['datum'])
#        
#        user = users.get_current_user()
#        
#        if user:
#            group_name = self.request.get('group_name', DEFAULT_GROUP_NAME)
#            weighings_query = Weighing.query().filter(Weighing.datum == datum)
#            single_weighings = weighings_query.fetch()
#            new_data = True
#            for single_weighing in single_weighings:
#                if single_weighing.person.identity == user.user_id():
#                    single_weighing.weight = int(weight_request['weight'].replace(',', ''))
#                    single_weighing.put()
#                    new_data = False
#                    break
#            
#            if new_data:
#                weighing = Weighing(parent=koerperwerte_key(group_name))
#                weighing.person = Person(identity = user.user_id(), email = user.email())
#                weighing.datum = dateutil.parser.parse(weight_request['datum'])
#                weighing.weight = int(weight_request['weight'].replace(',', ''))
#                weighing.put()
#
#JINJA_ENVIRONMENT.filters['format_weight'] = format_weight

app = webapp2.WSGIApplication([
    ('/', Newsletterman),
], debug=True)
