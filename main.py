#main.py
import webapp2
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
#
class Event(ndb.Model):
    organizer = ndb.StringProperty(required=True)
    title = ndb.StringProperty(required=True)

class WelcomePage(webapp2.RequestHandler):

    def get(self):
        logout_link = users.create_logout_url('/')
        start_template = jinja_current_directory.get_template('templates/welcome.html')
        self.response.write(start_template.render({
            'logout_link': logout_link
        }))

    def post(self):
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            greeting = 'Welcome, %s! (<a href="%s">sign out</a>)'.format(
                nickname, logout_url)
            add_template = jinja_current_directory.get_template('templates/welcome.html')
            self.response.write(add_template.render({'templates': templates}))
        else:
            login_prompt_template = jinja_current_directory.get_template('templates/login-please.html')
            self.response.write(login_prompt_template.render({
                'login_link': users.create_login_url('/')
                }))

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
