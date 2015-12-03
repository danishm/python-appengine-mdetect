import os
import json

import jinja2
import webapp2

from mdetect import UAgentInfo

# Declaring the path of the templates
TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), 'templates')

# Initializing the jinja2 environment
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATES_PATH),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
    """ A simple example of the mdetect capabilities. We call a few
        'detect' properties manually and display the result as a
        simple webpage
    """

    def get(self):
        user_agent = str(self.request.headers['User-Agent'])
        http_accept = str(self.request.headers['Accept'])
        ua_info = UAgentInfo(user_agent, http_accept)

        capabilities = {}
        capabilities['Is Smartphone'] = ua_info.detectSmartphone()
        capabilities['Is iOS'] = ua_info.detectIos()
        capabilities['Is IPad'] = ua_info.detectIpad()
        capabilities['Is Android'] = ua_info.detectAndroid()

        data = {}
        data['capabilities'] = capabilities
        data['user_agent'] = user_agent
        data['http_accept'] = http_accept

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(data))


class Detector(webapp2.RequestHandler):
    """ A class representing a more complex example of the mdetect
        capabilities. It uses dir to detect any property that
        begins with 'detect' and calls it to read the value
    """

    def get(self):
        user_agent = str(self.request.headers['User-Agent'])
        http_accept = str(self.request.headers['Accept'])
        ua_info = UAgentInfo(user_agent, http_accept)

        capabilities = dict()

        for obj in dir(ua_info):
            attr = getattr(ua_info, obj)
            if callable(attr) and obj.startswith('detect'):
                capabilities[obj.replace('detect', '')] = attr()

        print capabilities
        self.response.headers['Content-Type'] = 'application/json' 
        self.response.write(json.dumps(capabilities))


# Creating the actual application object
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/detect/', Detector)
], debug=True)
