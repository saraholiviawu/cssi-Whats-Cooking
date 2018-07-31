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
            #final_recipe_dict[recipe] = recipe_search_info.recipe["url"]
            #final_recipe_dict[recipe] = json.loads(recipe_search_info)[0].url
            #search_response = urlfetch.fetch(search_endpoint_url).content
            #print search_response
            #recipes_as_json = json.loads(search_response)
        #self.response.write(final_recipe_dict) #prints it to the page
        # search_endpoint_url = "http://food2fork.com/api/search?key=" + APP_KEY + "&q=avocado"
        # search_response = urlfetch.fetch(search_endpoint_url).content
        # print search_response
        # recipes_as_json = json.loads(search_response)
        self.response.write(recipe_search_info.content)
    def post(self):
        # trivia_endpoint_url = "https://opentdb.com/api.php?amount=1&category=10&difficulty=easy&type=multiple"
        # trivia_response= urlfetch.fetch(trivia_endpoint_url).content
        # trivia_as_json = json.loads(trivia_response)
        # first_result = trivia_as_json['results'][0]
        # trivia_question = first_result['question']
        # correct_answer = first_result['correct_answer']
        # incorrect_answers = first_result['incorrect_answers']
        self.response.write(correct_answer)




app = webapp2.WSGIApplication([
    ('/', WelcomePage),
], debug=True)
