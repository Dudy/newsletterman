from google.appengine.ext import ndb

class MailMessage(ndb.Model):
    mime_message = ndb.StringProperty()
