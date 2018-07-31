#main.py
import webapp2
from random import shuffle
#libraries for APIs
from google.appengine.api import urlfetch
import json
import urllib

class WelcomePage(webapp2.RequestHandler):

    def get(self):
        global APP_ID
        APP_ID = 
        global APP_KEY
        APP_KEY = "
        urlfetch.set_default_fetch_deadline(60) #this sets the deadline
        result = urlfetch.fetch( #this goes to the endpoint and grabs the json
              url="https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?ingredients=apples%2Cflour%2Csugar&number=5&ranking=1",
              headers={
                              },)

        recipe_list = json.loads(result.content)
        print recipe_list #parses json
        all_recipe_names = []
        for recipe in recipe_list:
            all_recipe_names.append(recipe["title"])
        print all_recipe_names[0]
        final_recipe_dict = {}
        for recipe in all_recipe_names:
            recipe = urllib.quote(recipe)
            print recipe
            recipe_search_info = urlfetch.fetch("https://api.edamam.com/search?q=" + recipe + "&app_id=" + APP_ID +"&app_key=" + APP_KEY + "&to=1")
            print recipe_search_info.content
           
        self.response.write(recipe_search_info.content)
    def post(self):
       
        self.response.write(correct_answer)




app = webapp2.WSGIApplication([
    ('/', WelcomePage),
], debug=True)
