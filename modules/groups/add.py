import models
import re
from google.appengine.ext import db
from google.appengine.api import users

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
				group = models.Group(
					name=groupName,
					owner=users.get_current_user()
				)
				group.put()
				try:
					member = models.GroupMember(
						group = group.key(),
						name = group.owner,
						status = 2,
					)
					member.put()
					self.message = 'Group created.'
				except:
					group.delete();
					self.error = True
					self.message = 'Group creation failed'
		else:
			self.message = 'Group names can consist of 0-9, A-Z, a-z, -, . and _.'
			self.error = True
		return {
			'error': self.error,
			'message': self.message
		}
	
