#main.py
import webapp2
from random import shuffle
#libraries for APIs
from google.appengine.api import urlfetch
import json

class MainPage(webapp2.RequestHandler):

    def get(self):
    #     global APP_ID
    #     #APP_ID = "3d641cfc"
    #     global APP_KEY
    # #    APP_KEY = ""
    #     #APP_KEY = ""
        urlfetch.set_default_fetch_deadline(60) #this sets the deadline
        result = urlfetch.fetch( #this goes to the endpoint and grabs the json
              url="https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?ingredients=apples%2Cflour%2Csugar&number=100&ranking=1",
              headers={
        
              },)

        recipe_list = json.loads(result.content)
        print recipe_list #parses json
        self.response.write(json.loads(result.content)) #prints it to the page
        # search_endpoint_url = "http://food2fork.com/api/search?key=" + APP_KEY + "&q=avocado"
        # search_response = urlfetch.fetch(search_endpoint_url).content
        # print search_response
        # recipes_as_json = json.loads(search_response)
        # self.response.write(recipes_as_json)
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
    ('/', MainPage),
], debug=True)
