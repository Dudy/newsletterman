from google.appengine.ext import ndb

class UserSubscription(ndb.Model):
    userId = ndb.StringProperty()
    serviceUrl = ndb.StringProperty()
