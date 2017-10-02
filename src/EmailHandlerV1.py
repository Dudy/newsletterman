#!/usr/bin/env python

import webapp2
import logging

from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

class EmailHandlerV1(InboundMailHandler):

    def receive(self, mail_message):
        logging.info(mail_message)
        logging.info("Received a message from: " + mail_message.sender)
        logging.info("Subject: " + mail_message.subject)
        logging.info(mail_message.original)
        
        plaintext_bodies = mail_message.bodies('text/plain')
        html_bodies = mail_message.bodies('text/html')

        for content_type, body in html_bodies:
            decoded_html = body.decode()
            logging.info(decoded_html)
        for content_type, body in plaintext_bodies:
            decoded_text = body.decode()
            logging.info(decoded_text)
        logging.info("=========================================================================")
        
app = webapp2.WSGIApplication([EmailHandlerV1.mapping()], debug=True)
