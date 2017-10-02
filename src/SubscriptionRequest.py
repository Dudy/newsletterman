from google.appengine.ext import ndb

class SubscriptionRequest(ndb.Model):
    serviceUrl = ndb.StringProperty()
