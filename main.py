#main.py
import webapp2
from random import shuffle
#libraries for APIs
from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext import ndb
import json
import jinja2
import os
import urllib

jinja_current_directory  = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class WelcomePage(webapp2.RequestHandler):
    def get (self):
        welcome_template = jinja_current_directory.get_template('templates/welcome.html')
        self.response.write(welcome_template.render({'login_url': users.create_login_url('/main')}))
    def post(self):
        #continuation of login through post method
        # user = users.get_current_user()
        #
        # nickname = user.nickname()
        # logout_url = users.create_logout_url('/')
        # logout_text = "Logout"
        #recipe API
        global APP_ID
        APP_ID = ""
        global APP_KEY
        APP_KEY = ""
        urlfetch.set_default_fetch_deadline(60) #this sets the deadline
        url=("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?ingredients=" + urllib.quote(self.request.get("foodlist").replace(" ", "")) + "&number=5&ranking=2")
        print url
        result = urlfetch.fetch( #this goes to the endpoint and grabs the json
              # url="https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?ingredients=" + urllib.quote(self.request.get("foodlist")) + "&number=5&ranking=1",
              url,
              headers={
                "X-Mashape-Key": "",
              },)
        print url

        recipe_list = json.loads(result.content)
        #print recipe_list #parses json
        all_recipe_names = []
        all_recipe_images = []
        for recipenames in recipe_list:
            all_recipe_names.append(recipenames["title"])
            all_recipe_images.append(recipenames["image"])
        #print all_recipe_names[0]
        final_recipe_dict = {}

        for recipe in all_recipe_names:
            recipe = urllib.quote(recipe)
        #    print recipe
            recipe_search_info = urlfetch.fetch("https://api.edamam.com/search?q=" + recipe + "&app_id=" + APP_ID +"&app_key=" + APP_KEY + "&to=1")
            print json.loads(recipe_search_info.content)["hits"][0]["recipe"]["url"]
            final_recipe_dict[recipe] = json.loads(recipe_search_info.content)["hits"][0]["recipe"]["url"]


        tempval = 0
        for key in final_recipe_dict:
            self.response.write("<img src=" + all_recipe_images[tempval] + "> <br> " + key.replace("%20", " ") + ". Find more information at: " + final_recipe_dict[key])
            tempval += 1

        my_template = jinja_current_directory.get_template('templates/results.html')
        # self.response.write(my_template.render(template_vars))

        template_vars = {
            'input_ingredient': self.request.get('foodlist'),
        }

class MainPage(webapp2.RequestHandler):
      def get(self):
        template_var = {}
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            template_var = {
                "logout_url": logout_url,
                "nickname": nickname
            }
        else:
            self.redirect('/welcome')
        main_template = jinja_current_directory.get_template('templates/main.html')
        self.response.write(main_template.render(template_var))

        #recipe API-----------------
    #     global APP_ID
    #
    #     urlfetch.set_default_fetch_deadline(60) #this sets the deadline
    #     result = urlfetch.fetch( #this goes to the endpoint and grabs the json
    #           url="https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?ingredients=apples%2Cflour%2Csugar&number=5&ranking=1",
    #           headers={
    #                           },)
    #
    #     recipe_list = json.loads(result.content)
    #     print recipe_list #parses json
    #     all_recipe_names = []
    #     for recipe in recipe_list:
    #         all_recipe_names.append(recipe["title"])
    #     print all_recipe_names[0]
    #     final_recipe_dict = {}
    #     for recipe in all_recipe_names:
    #         recipe = urllib.quote(recipe)
    #         print recipe
    #         recipe_search_info = urlfetch.fetch("https://api.edamam.com/search?q=" + recipe + "&app_id=" + APP_ID +"&app_key=" + APP_KEY + "&to=1")
    #         print recipe_search_info.content
    #
    #     self.response.write(recipe_search_info.content)
    # def post(self):
    #     pass
    #     template_vars = {
    #         'input_ingredients': self.request.get('input_ingredients'),
    #     }

class ResultsPage(webapp2.RequestHandler):

    def post(self):
        #recipe API
        global APP_ID
        APP_ID = ""
        global APP_KEY
        APP_KEY = ""
        urlfetch.set_default_fetch_deadline(60) #this sets the deadline
        url=("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?ingredients=" + urllib.quote(self.request.get("foodlist").replace(" ", "")) + "&number=5&ranking=2")
        print url
        result = urlfetch.fetch( #this goes to the endpoint and grabs the json
              # url="https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?ingredients=" + urllib.quote(self.request.get("foodlist")) + "&number=5&ranking=1",
              url,
              headers={
                "X-Mashape-Key": "DomnZY3cOZmshkfgl4Z3KOudQ0Vnp1S2NaKjsnSZUDpWRwTxBz",
                "X-Mashape-Host": "spoonacular-crecipe-food-nutrition-v1.p.mashape.com",
              },)
        print url

        recipe_list = json.loads(result.content)
        #print recipe_list #parses json
        all_recipe_names = []
        all_recipe_images = []
        for recipenames in recipe_list:
            all_recipe_names.append(recipenames["title"])
            all_recipe_images.append(recipenames["image"])
        #print all_recipe_names[0]
        final_recipe_dict = {}

        for recipe in all_recipe_names:
            recipe = urllib.quote(recipe)
        #    print recipe
            recipe_search_info = urlfetch.fetch("https://api.edamam.com/search?q=" + recipe + "&app_id=" + APP_ID +"&app_key=" + APP_KEY + "&to=1")
            print json.loads(recipe_search_info.content)["hits"][0]["recipe"]["url"]
            final_recipe_dict[recipe] = json.loads(recipe_search_info.content)["hits"][0]["recipe"]["url"]


        tempval = 0
        for key in final_recipe_dict:
            self.response.write("<img src=" + all_recipe_images[tempval] + "> <br> " + key.replace("%20", " ") + ". Find more information at: " + final_recipe_dict[key])
            tempval += 1

        my_template = jinja_current_directory.get_template('templates/results.html')
        # self.response.write(my_template.render(template_vars))

        template_vars = {
            'input_ingredient': self.request.get('foodlist'),
        }



class ResultsPage(webapp2.RequestHandler):

        def post(self):
                #recipe API
                global APP_ID
                APP_ID = ""
                global APP_KEY
                APP_KEY = ""
                urlfetch.set_default_fetch_deadline(60) #this sets the deadline
                result = urlfetch.fetch( #this goes to the endpoint and grabs the json

                      url="https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?ingredients=" + urllib.quote(self.request.get("foodlist")) + "&number=5&ranking=1",
                      headers={
                        "X-Mashape-Key": "DomnZY3cOZmshkfgl4Z3KOudQ0Vnp1S2NaKjsnSZUDpWRwTxBz",
                        "X-Mashape-Host": "spoonacular-crecipe-food-nutrition-v1.p.mashape.com",
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

                for i in recipe_search_info.content:
                    self.response.write("<img src = " + i[uri] + "/> <br> " + i["q"] + ". Find more information at: " + i["url"])

                template_vars = {
                    'input_ingredients': self.request.get('foodlist'),
                }
                results_template = jinja_current_directory.get_template('templates/results.html')
                self.response.write(results_template.render(template_vars))

class RecipeInstructionsPage(webapp2.RequestHandler):
    def get(self):
        recipe_instructions_template = jinja_current_directory.get_template('templates/recipe-instructions.html')
        self.response.write(recipe_instructions_template.render())

app = webapp2.WSGIApplication([
    ('/', WelcomePage),
    ('/main', MainPage),
    ('/results', ResultsPage),
    ('/RecipeInstructionsPage', RecipeInstructionsPage),
], debug=True)
