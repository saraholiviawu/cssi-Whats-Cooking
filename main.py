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

jinja_current_directory  = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# class Event(ndb.Model):
#     organizer = ndb.StringProperty(required=True)
#     title = ndb.StringProperty(required=True)

class WelcomePage(webapp2.RequestHandler):

    def get(self):
        #login
        logout_link = users.create_logout_url('/')
        start_template = jinja_current_directory.get_template('templates/welcome.html')
        self.response.write(start_template.render({
            'logout_link': logout_link
        }))

        #recipe API
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
        #continuation of login through post method
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            logout_text = "Logout"
            # greeting = 'Welcome, %s! (<a href="%s">sign out</a>)'.format(
                # nickname, logout_url)
            # add_template = jinja_current_directory.get_template('templates/welcome.html')
            # self.response.write(add_template.render({'templates': templates}))
            # self.response.write(greeting)
        else:
            login_prompt_template = jinja_current_directory.get_template('templates/login-please.html')
            self.response.write(login_prompt_template.render({
                'login_link': users.create_login_url('/')
                }))
        template_vars = {
            'nickname': nickname,
            'logout_url': logout_url,
            'logout_text': logout_text,
        }
        my_template = jinja_current_directory.get_template('/')
        self.response.write(my_template.render(template_vars))

        template_vars = {
            'input_ingredients': self.request.get('input_ingredients'),
        }

class ResultsPage(webapp2.RequestHandler):

    def post(self):
        template_vars = {
            'input_ingredients': self.request.get('input_ingredients'),
        }
        results_template = jinja_current_directory.get_template('templates/results.html')
        self.response.write(results_template.render(template_vars))

class RecipeInstructionsPage(webapp2.RequestHandler):
    def get(self):
        recipe_instructions_template = jinja_current_directory.get_template('templates/recipe-instructions.html')
        self.response.write(recipe_instructions_template.render())

class LoginPlease(webapp2.RequestHandler):
    def get(self):
        login_prompt_template = jinja_current_directory.get_template('templates/login-please.html')
        self.response.write(login_prompt_template.render({
            'login_link': users.create_login_url('/')
            }))

app = webapp2.WSGIApplication([
    ('/', WelcomePage),
    ('/results', ResultsPage),
    ('/RecipeInstructionsPage', RecipeInstructionsPage),
    ('/LoginPlease', LoginPlease)
], debug=True)
