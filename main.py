#!/usr/bin/env python

import os
import wsgiref.handlers
import locale

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users
from commands import *

templateVars = {
    'user':users.get_current_user(),
    'logout':users.create_logout_url('/'),
}

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
            for command in route['commands']:
                commandName = command.__name__.lower()
                command = command()
                templateVars[commandName] = command.process(self.request)
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
    

class AddEstimationHandler(webapp.RequestHandler):
    def get(self, taskKey):
        self.redirect('/')
    
    def post(self, taskKey):
        add = Add()
        templateVars['add'] = add.process(self.request, taskKey)
        list = List()
        templateVars['list'] = list.process(self.request)
        path = os.path.join(os.path.dirname(__file__), 'templates/add.html')
        self.response.out.write(template.render(path, templateVars))
    

application = webapp.WSGIApplication(
                                     [(r'/add/(.*)', AddEstimationHandler),
                                      (r'.*', MainHandler),
                                     ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
