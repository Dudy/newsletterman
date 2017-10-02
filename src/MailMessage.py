from google.appengine.ext import ndb

class MailMessage(ndb.Model):
    sender = ndb.StringProperty()
    mime_message = ndb.StringProperty()