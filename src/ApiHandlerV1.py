#!/usr/bin/env python

import webapp2

from webapp2_extras import json
from google.appengine.api import users

class ApiHandlerV1(webapp2.RequestHandler):

    def firstBatch(self):
        user = users.get_current_user()
        
        if user:
            response = [{
                'imageUrl': 'http://via.placeholder.com/60x60', 
                'title': 'Item 1 of user ' + user.nickname(),
                'text': 'Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante sollicitudin. Cras purus odio, vestibulum in vulputate at, tempus viverra turpis. Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia congue felis in faucibus.'
            }, {
                'imageUrl': 'http://via.placeholder.com/60x60', 
                'title': 'Item 2 of user ' + user.nickname(),
                'text': 'Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante sollicitudin. Cras purus odio, vestibulum in vulputate at, tempus viverra turpis. Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia congue felis in faucibus.'
            }]
            
            self.response.content_type = 'application/json'
            self.response.write(json.encode(response))
        else:
            self.error(403)

    def next(self, current):
        user = users.get_current_user()
        
        if user:
            response = {
                'imageUrl': 'http://via.placeholder.com/60x60', 
                'title': 'Item ' + str(int(current) + 1) + ' of user ' + user.nickname(),
                'text': 'Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante sollicitudin. Cras purus odio, vestibulum in vulputate at, tempus viverra turpis. Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia congue felis in faucibus.'
            }

            self.response.content_type = 'application/json'
            self.response.write(json.encode(response))
        else:
            self.error(403)
        
app = webapp2.WSGIApplication([
    webapp2.Route(r'/v1/api/newsletter', handler=ApiHandlerV1, handler_method='firstBatch', methods=['GET']),
    webapp2.Route(r'/v1/api/newsletter/<current>/next', handler=ApiHandlerV1, name='current', handler_method='next', methods=['GET'])
], debug=True)
