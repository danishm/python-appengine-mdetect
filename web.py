import os

import jinja2
import webapp2

# Declaring the path of the templates
TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), 'templates')

# Initializing the jinja2 environment
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATES_PATH),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
	''' A class to handle requests for the main page '''

    def get(self):
        data = {'greeting': 'Hello World!'}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(data))


# Creating the actual application object
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)