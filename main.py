#main.py
import webapp2
#libraries for APIs
from google.appengine.api import urlfetch
import json


class MainPage(webapp2.RequestHandler):

    def get(self):
        global APP_ID
        APP_ID = ""
        global APP_KEY
        APP_KEY = ""
        search_endpoint_url = "https://api.edamam.com/search?q=chicken&app_id=" + APP_ID +"&app_key=" + APP_KEY
        search_response = urlfetch.fetch(search_endpoint_url).content
        print search_response
        recipes_as_json = json.loads(search_response)
        self.response.write(recipes_as_json)
    def post(self):
      
        self.response.write(correct_answer)




app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
