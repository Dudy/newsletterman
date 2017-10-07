from google.appengine.ext import ndb

class MailMessage(ndb.Model):
    mime_message = ndb.TextProperty()
    create_date = ndb.DateTimeProperty(auto_now=True)
