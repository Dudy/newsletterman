from google.appengine.ext import ndb

class MailMessage(ndb.Model):
    service_id = ndb.StringProperty()
    mime_message = ndb.StringProperty()