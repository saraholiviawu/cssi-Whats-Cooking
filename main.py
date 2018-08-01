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
import user_models

jinja_current_directory  = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

my_file = open('app-secrets.json')
my_secrets = my_file.read()
SECRETS_DICT = json.loads(my_secrets)
my_file.close()

class WelcomePage(webapp2.RequestHandler):
    def get(self):
        welcome_template = jinja_current_directory.get_template('templates/welcome.html')
        self.response.write(welcome_template.render({'login_url': users.create_login_url('/main')}))
    def post(self):
        self.redirect("/main")



class MainPage(webapp2.RequestHandler):
    def get(self):
        template_var = {}
        global user
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            user_id = str(user.user_id())
            logout_url = users.create_logout_url('/')
            template_var = {
                "logout_url": logout_url,
                "nickname": nickname
            }
            # if (user_models.User.query().filter(user_models.User.nickname == nickname).fetch()[0] == nickname):
            #     pass
            # else: WIP MAKING SURE YOU CANT REGISTER TWICE BC RN YOU CAN
            global current_user_key
            current_user_key = user_models.User(user_id=user_id, nickname=nickname, recipes=[]).put()
        else:
            self.redirect('/welcome')
        main_template = jinja_current_directory.get_template('templates/main.html')
        self.response.write(main_template.render(template_var))
    def post(self):
        #recipe API
        global APP_ID
        APP_ID = SECRETS_DICT['api-id1']
        global APP_KEY
        APP_KEY = "84103e81ef614ae430c3bc458d36ff16"
        urlfetch.set_default_fetch_deadline(60) #this sets the deadline
        url=("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?ingredients=" + urllib.quote(self.request.get("foodlist").replace(" ", "")) + "&number=5&ranking=2")
        print url
        result = urlfetch.fetch( #this goes to the endpoint and grabs the json
              # url="https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?ingredients=" + urllib.quote(self.request.get("foodlist")) + "&number=5&ranking=1",
              url,
              headers={
                "X-Mashape-Key": SECRETS_DICT['mashape-key'],
                "X-Mashape-Host": SECRETS_DICT['mashape-host'],
              },)
        print url

        recipe_list = json.loads(result.content)
        #print recipe_list #parses json
        all_recipe_names = []
        all_recipe_images = []
        for recipenames in recipe_list:
            all_recipe_names.append(recipenames["title"])

        #print all_recipe_names[0]
        final_recipe_dict = {}

        final_recipe_list= []

        for recipe in all_recipe_names:
            quoted_recipe = urllib.quote(recipe)
        #    print recipe
            recipe_search_info = urlfetch.fetch("https://api.edamam.com/search?q=" + quoted_recipe + "&app_id=" + APP_ID +"&app_key=" + APP_KEY + "&to=1")
            print json.loads(recipe_search_info.content)["hits"][0]["recipe"]["url"]
            results_dict= json.loads(recipe_search_info.content)
            final_recipe_list.append( {
                'name': recipe,
                'img_url': results_dict["hits"][0]["recipe"]["image"],
                'recipe_url': results_dict["hits"][0]["recipe"]["url"],
            })

        template_vars = {
            'input_ingredient': self.request.get('foodlist'),
            'recipes': final_recipe_list,
        }
        welcome_template = jinja_current_directory.get_template('templates/results.html')
        self.response.write(welcome_template.render(template_vars))

class FavoritesPage(webapp2.RequestHandler):
    def get(self):
        recipe_instructions_template = jinja_current_directory.get_template('templates/favorites.html')
        self.response.write(recipe_instructions_template.render())

    def post(self):
        global APP_ID
        APP_ID = SECRETS_DICT['api-id1']
        global APP_KEY
        APP_KEY = "84103e81ef614ae430c3bc458d36ff16"
        final_recipe_list= []
        urlfetch.set_default_fetch_deadline(60) #this sets the deadline
        quoted_recipe = urllib.quote(self.request.get("favoritesearch"))
        recipe_search_info = urlfetch.fetch("https://api.edamam.com/search?q=" + quoted_recipe + "&app_id=" + APP_ID +"&app_key=" + APP_KEY + "&to=1")
        print json.loads(recipe_search_info.content)["hits"][0]["recipe"]["url"]
        results_dict= json.loads(recipe_search_info.content)
        #print results_dict
        final_recipe_list.append( {
            'name': results_dict["q"],
            'img_url': results_dict["hits"][0]["recipe"]["image"],
            'recipe_url': results_dict["hits"][0]["recipe"]["url"],
        })
        user_model_key = user_models.Recipe(
            title=final_recipe_list[0]['name'], image=final_recipe_list[0]['img_url'],
            url=final_recipe_list[0]['recipe_url']).put()
        current_user = user_models.User.query().filter(user_models.User.user_id == users.get_current_user().user_id()).get()
        current_user.recipes.append(user_model_key)
        current_user.put()
        print user_models.User.query().filter(user_models.User.user_id == users.get_current_user().user_id()).get()
        recipe_instructions_template = jinja_current_directory.get_template('templates/favorites.html')
        self.response.write(recipe_instructions_template.render())
        # user_models.User.query().filter(user_models.User.user_id == self.request.get("key")).get().recipes = (user_model_key,)



app = webapp2.WSGIApplication([
    ('/', WelcomePage),
    ('/main', MainPage),
    ('/favorites', FavoritesPage),
], debug=True)
