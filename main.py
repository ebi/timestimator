#!/usr/bin/env python

import os
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users

class MainPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
        path = users.create_login_url("/")
        self.redirect(path)
        return
        
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, user))


application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
