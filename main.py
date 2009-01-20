#!/usr/bin/env python

import os
import wsgiref.handlers
import locale
import pprint

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users
from commands import *

class MainHandler(webapp.RequestHandler):
    "Verify request and authentication call the appropriate template"
    getUrl = {
        '/': {'template':'list.html','commands':[List]},
    }
    
    postUrl = {
        '/add': {'template':'add.html','commands':[Add,List]},
    }

    def render(self, urlMap):
        if self.request.path in urlMap:
            route = urlMap[self.request.path]
            templateVars = {}
            for command in route['commands']:
                commandName = command.__name__.lower()
                command = command()
                templateVars[commandName] = command.process(self.request)
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
