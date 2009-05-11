#!/usr/bin/env python

import os
import wsgiref.handlers
import locale
import models
import pprint

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users
from modules import add, detail, overview, groups


def getBaseTemplateVars():
	return {
		'user':users.get_current_user(),
		'logout':users.create_logout_url('/'),
	}

class MainHandler(webapp.RequestHandler):
	"Verify request and authentication call the appropriate template"
	getUrl = {
		'/groups': {'template':'groups.html','commands':[groups.overview.Overview]},
		'/': {'template':'overview.html','commands':[overview.List]},
	}
	
	postUrl = {
		'/add': {'template':'add.html','commands':[add.Add,overview.List]},
		'/groups': {'template':'groups.html','commands':[groups.add.Add,groups.overview.Overview]},
	}
	
	def render(self, urlMap):
		if self.request.path in urlMap:
			route = urlMap[self.request.path]
			templateVars = getBaseTemplateVars()
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
	

class DetailTaskHandler(webapp.RequestHandler):
	def get(self, taskKey):
		details = detail.Detail()
		templateVars = getBaseTemplateVars()
		templateVars['detail'] = details.process(self.request, taskKey)
		path = os.path.join(os.path.dirname(__file__), 'templates/detail.html')
		self.response.out.write(template.render(path, templateVars))
	
	def post(self, taskKey):
		self.get(taskKey)
	

class AddEstimationHandler(webapp.RequestHandler):
	def get(self, taskKey):
		self.redirect('/')
	
	def post(self, taskKey):
		templateVars = getBaseTemplateVars()
		adder = add.Add()
		templateVars['add'] = adder.process(self.request, taskKey)
		list = overview.List()
		templateVars['list'] = list.process(self.request)
		path = os.path.join(os.path.dirname(__file__), 'templates/add.html')
		self.response.out.write(template.render(path, templateVars))

class GroupsTaskHandler(webapp.RequestHandler):
	def get(self, groupKey):
		self.redirect('/groups')

	def post(self, groupKey):
		templateVars = getBaseTemplateVars()
		if self.request.get('delete'):
			taskName = 'delete'
			group = groups.delete.Delete()
		else:
			taskName = 'join'
			group = groups.join.Join()
		templateVars[taskName] = group.process(self.request, groupKey)
		group = groups.overview.Overview()
		templateVars['overview'] = group.process(self.request)
		path = os.path.join(os.path.dirname(__file__), 'templates/groups.html')
		self.response.out.write(template.render(path, templateVars))

application = webapp.WSGIApplication(
									 [(r'/add/(.*)', AddEstimationHandler),
									  (r'/detail/(.*)', DetailTaskHandler),
									  (r'/groups/(.*)', GroupsTaskHandler),
									  (r'.*', MainHandler),
									 ],
									 debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
