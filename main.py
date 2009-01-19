#!/usr/bin/env python

import os
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users

class MainHandler(webapp.RequestHandler):
    "Verify request and authentication call the appropriate template"
    getUrl = {
        '/': {'template':'index.html'},
    }
    
    postUrl = {
        '/add': {'template':'add.html','command':'add'},
    }

    def checkauth(self):
        if not users.get_current_user():
            path = users.create_login_url("/")
            self.redirect(path)
            return

    def render(self, urlMap):
        if self.request.path in urlMap:
            route = urlMap[self.request.path]
            
            if 'command' in route:
                commandPath = os.path.join(os.path.dirname(__file__), 'commands', route['command'] + '.py')
                execfile(commandPath)
                command = locals().get(route['command'])()
                templateVars = command.process(self.request)
            else:
                templateVars = self.request
            
            path = os.path.join(os.path.dirname(__file__), 'templates', route['template'])
            self.response.out.write(template.render(path, templateVars))
            return True
        else:
            self.redirect('/')
            return False

    def get(self):
        self.checkauth()
        self.render(self.getUrl);

    def post(self):
        self.checkauth()
        self.render(self.postUrl)

application = webapp.WSGIApplication(
                                     [(r'.*', MainHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
