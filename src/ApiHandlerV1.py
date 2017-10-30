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
                mails = mailQuery.fetch(limit = 2)
                
                for mail in mails:
                    mime_message_text = mail.mime_message
                    mime_message = InboundEmailMessage(mime_message = mime_message_text)
                    
                    plaintext_bodies = mime_message.bodies('text/plain')
                    #html_bodies = mime_message.bodies('text/html')

                    for content_type, body in plaintext_bodies:
                        decoded_body = body.decode()
                    #for content_type, body in html_bodies:
                    #    decoded_body = body.decode()
                    
                    text = decoded_body[:160]
                    if len(text) < len(decoded_body):
                        text += '...'
                    
                    message_array.append({
                        'imageUrl': 'https://via.placeholder.com/60x60', 
                        'title': 'message from ' + str(mail.create_date),
                        'text': text,
                        'body': decoded_body
                    })
            
            self.response.content_type = 'application/json'
            self.response.write(json.encode(message_array))
        else:
            self.error(403)

    def getNext(self, current):
        user = users.get_current_user()
        
        if user:
            message = None
            query = UserSubscription.query(UserSubscription.userId == user.user_id())
            for userSubscription in query.iter():
                key = ndb.Key(MailMessage, userSubscription.serviceId)
                mailQuery = MailMessage.query(ancestor = key).order(-MailMessage.create_date)
                mails = mailQuery.fetch(offset = int(current), limit = 1)
                
                if len(mails) > 0:
                    mail = mails[0]
                    mime_message_text = mail.mime_message
                    mime_message = InboundEmailMessage(mime_message = mime_message_text)

                    plaintext_bodies = mime_message.bodies('text/plain')
                    #html_bodies = mime_message.bodies('text/html')

                    for content_type, body in plaintext_bodies:
                        decoded_body = body.decode()
                    #for content_type, body in html_bodies:
                    #    decoded_body = body.decode()

                    text = decoded_body[:160]
                    if len(text) < len(decoded_body):
                        text += '...'

                    message = {
                        'imageUrl': 'https://via.placeholder.com/60x60', 
                        'title': 'message from ' + str(mail.create_date),
                        'text': text,
                        'body': decoded_body
                    }
            if message:
                self.response.content_type = 'application/json'
                self.response.write(json.encode(message))
            else:
                self.error(404)
        else:
            self.error(403)
    
    def postNewSubscriptionRequest(self):
        user = users.get_current_user()
        
        if user:
            requestObject = json.decode(self.request.body)
            
            if isinstance(requestObject, list):
                for serviceId in requestObject:
                    userSubscription = UserSubscription(userId = user.user_id(), serviceId = serviceId)
                    userSubscription.put()
            else:
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
    
    def getExistingSubscriptions(self):
        user = users.get_current_user()
        
        if user:
            existingSubscriptions = []
            serviceIdsQuery = UserSubscription.query(projection = [UserSubscription.serviceId], distinct = True)
            for projectedUserSubscription in serviceIdsQuery.iter():
                existingSubscriptions.append({ 'serviceId': projectedUserSubscription.serviceId })
            self.response.content_type = 'application/json'
            self.response.write(json.encode(existingSubscriptions))
        else:
            self.error(403)

app = webapp2.WSGIApplication([
    webapp2.Route(r'/v1/api/newsletter', handler=ApiHandlerV1, handler_method='getFirstBatch', methods=['GET']),
    webapp2.Route(r'/v1/api/newsletter/<current>/next', handler=ApiHandlerV1, name='current', handler_method='getNext', methods=['GET']),
    webapp2.Route(r'/v1/api/newsletter/subscription', handler=ApiHandlerV1, handler_method='postNewSubscriptionRequest', methods=['POST']),
    webapp2.Route(r'/v1/api/subscriptionRequests', handler=ApiHandlerV1, handler_method='getSubscriptionRequests', methods=['GET']),
    webapp2.Route(r'/v1/api/subscriptionRequests', handler=ApiHandlerV1, handler_method='postSubscriptionRequests', methods=['POST']),
    webapp2.Route(r'/v1/api/existingSubscriptions', handler=ApiHandlerV1, handler_method='getExistingSubscriptions', methods=['GET'])
], debug=True)
