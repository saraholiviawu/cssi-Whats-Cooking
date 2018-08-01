from google.appengine.ext import ndb

class Recipe(ndb.Model):
    title = ndb.StringProperty(required=True)
    image = ndb.StringProperty(required=False)
    url = ndb.StringProperty(required=True)

class User(ndb.Model):
    user_id =  ndb.StringProperty(required=True)
    nickname =  ndb.GenericProperty(required=True)
    recipes =  ndb.KeyProperty(Recipe, repeated=True)
