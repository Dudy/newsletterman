#!/usr/bin/env python

import webapp2
import logging

from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

from MailMessage import MailMessage

class EmailHandlerV1(InboundMailHandler):

    def receive(self, mail_message):
        logging.info(mail_message.to_mime_message())

        # store message
        service_id = mail_message.to.split('@')[0]
        mime_message = str(mail_message.to_mime_message())
        persistent_mail_message = MailMessage(service_id = service_id, mime_message = mime_message)
        persistent_mail_message.put()
        
app = webapp2.WSGIApplication([EmailHandlerV1.mapping()], debug=True)
