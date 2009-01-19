#!/usr/bin/env python

import os
import wsgiref.handlers
import locale

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users
from commands import *

class MainHandler(webapp.RequestHandler):
    "Verify request and authentication call the appropriate template"
    getUrl = {
        '/': {'template':'index.html'},
    }
    
    postUrl = {
        '/add': {'template':'add.html','command':Add},
    }

    def render(self, urlMap):
        if self.request.path in urlMap:
            route = urlMap[self.request.path]
            
            if 'command' in route:
                command = route['command']()
                templateVars = command.process(self.request)
            else:
                templateVars = {}
            templateVars['request'] = self.request
            templateVars['user'] = users.get_current_user()
            templateVars['logout'] = users.create_logout_url('/')
            
            path = os.path.join(os.path.dirname(__file__), 'templates', route['template'])
            self.response.out.write(template.render(path, templateVars))
            return True
        else:
            self.redirect('/')
            return False

    def get(self):
        self.render(self.getUrl);

    def post(self):
        self.render(self.postUrl)

application = webapp.WSGIApplication(
                                     [(r'.*', MainHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
