#!/usr/bin/env python

import webapp2
import logging

from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.ext import ndb

from MailMessage import MailMessage

# the email domain of this app is @pomis-newsletterman.appspotmail.com

class EmailHandlerV1(InboundMailHandler):

    def receive(self, mail_message):
        logging.info(mail_message.to_mime_message())

        # store message
        service_id = mail_message.to.split('@')[0]
        mime_message = str(mail_message.to_mime_message())
        service_key = ndb.Key(MailMessage, service_id)
        new_id = ndb.Model.allocate_ids(size = 1, parent = service_key)[0]
        mail_message_key = ndb.Key(MailMessage, new_id, parent = service_key)
        persistent_mail_message = MailMessage(parent = mail_message_key, mime_message = mime_message)
        persistent_mail_message.put()
        
app = webapp2.WSGIApplication([EmailHandlerV1.mapping()], debug=True)
