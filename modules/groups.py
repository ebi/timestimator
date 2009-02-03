import models
import re
from google.appengine.ext import db
from google.appengine.api import users

class Overview(object):
	def process(self, request):
		return {'groups': models.Group.all()}

class Add(object):
	error = False
	message = ''
	
	def process(self, request):
		groupName = request.get('group')
		
		if groupName != '' and re.match('^[\w_\.]*$', groupName):
			unique = db.GqlQuery("SELECT * FROM Group WHERE name = :name", name=groupName)
			if unique.count() > 0:
				self.message = 'Group already exists.'
				self.error = True
			else:
				group = models.Group()
				group.name = groupName
				group.owner = users.get_current_user()
				group.put()
				self.message = 'Group created.'
		else:
			self.message = 'Group names can consist of 0-9, A-Z, a-z, -, . and _.'
			self.error = True
		return {
			'error': self.error,
			'message': self.message
		}