#!/usr/bin/env python

import webapp2
import logging

from webapp2_extras import json
from google.appengine.api import users
from google.appengine.api.mail import InboundEmailMessage
from google.appengine.ext import ndb

from SubscriptionRequest import SubscriptionRequest
from UserSubscription import UserSubscription
from MailMessage import MailMessage

class ApiHandlerV1(webapp2.RequestHandler):

    def getFirstBatch(self):
        user = users.get_current_user()
        
        if user:
            message_array = []
            
            query = UserSubscription.query(UserSubscription.userId == user.user_id())
            for userSubscription in query.iter():
                key = ndb.Key(MailMessage, userSubscription.serviceId)
                mailQuery = MailMessage.query(ancestor = key).order(-MailMessage.create_date)
                mails = mailQuery.fetch(limit = 5)
                
                for mail in mails:
                    mime_message_text = mail.mime_message
                    mime_message = InboundEmailMessage(mime_message = mime_message_text)
                    
                    plaintext_bodies = mime_message.bodies('text/plain')
                    #html_bodies = mime_message.bodies('text/html')

                    for content_type, body in plaintext_bodies:
                        decoded_html = body.decode()
                    #for content_type, body in html_bodies:
                    #    decoded_html = body.decode()
                    
                    message_array.append({
                        'imageUrl': 'http://via.placeholder.com/60x60', 
                        'title': 'message from ' + str(mail.create_date),
                        'text': decoded_html[:160] + '...'
                    })
            
            self.response.content_type = 'application/json'
            self.response.write(json.encode(message_array))
        else:
            self.error(403)

    def getNext(self, current):
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
    
    def postNewSubscriptionRequest(self):
        user = users.get_current_user()
        
        if user:
            requestObject = json.decode(self.request.body)
            serviceUrl = requestObject['serviceUrl']
            subscriptionRequest = SubscriptionRequest(serviceUrl = serviceUrl)
            subscriptionRequest.put()
            userSubscription = UserSubscription(userId = user.user_id(), serviceId = serviceUrl)
            userSubscription.put()
        else:
            self.error(403)
    
    def getSubscriptionRequests(self):
        if users.is_current_user_admin():
            subscriptionRequests = []
            subscriptionRequestQuery = SubscriptionRequest.query()
            for subscriptionRequest in subscriptionRequestQuery.iter():
                subscriptionRequests.append({ 'serviceUrl': subscriptionRequest.serviceUrl })
            self.response.content_type = 'application/json'
            self.response.write(json.encode(subscriptionRequests))
        else:
            self.error(403)
    
    def postSubscriptionRequests(self):
        if users.is_current_user_admin():
            subscriptionRequests = json.decode(self.request.body)
            for subscriptionRequest in subscriptionRequests:
                serviceUrl = subscriptionRequest['serviceUrl']
                serviceId = subscriptionRequest['serviceId']
                query = UserSubscription.query(UserSubscription.serviceId == serviceUrl)
                for userSubscription in query.iter():
                    userSubscription.serviceId = serviceId
                    userSubscription.put()
                query = SubscriptionRequest.query(SubscriptionRequest.serviceUrl == serviceUrl)
                list_of_keys = ndb.put_multi(query.fetch())
                ndb.delete_multi(list_of_keys)
                    
        else:
            self.error(403)
        
app = webapp2.WSGIApplication([
    webapp2.Route(r'/v1/api/newsletter', handler=ApiHandlerV1, handler_method='getFirstBatch', methods=['GET']),
    webapp2.Route(r'/v1/api/newsletter/<current>/next', handler=ApiHandlerV1, name='current', handler_method='getNext', methods=['GET']),
    webapp2.Route(r'/v1/api/newsletter/subscription', handler=ApiHandlerV1, handler_method='postNewSubscriptionRequest', methods=['POST']),
    webapp2.Route(r'/v1/api/subscriptionRequests', handler=ApiHandlerV1, handler_method='getSubscriptionRequests', methods=['GET']),
    webapp2.Route(r'/v1/api/subscriptionRequests', handler=ApiHandlerV1, handler_method='postSubscriptionRequests', methods=['POST'])
], debug=True)
