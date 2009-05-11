import models
import helper
from google.appengine.ext import db
from google.appengine.api import users

class Delete(object):
	error = False
	message = ''
	
	def process(self, request, groupKey):
		if request.get('delete') != groupKey:
			self.error = True
			self.message = "GroupId in body doesn't match URL"
			
		group = helper.getGroup(groupKey)
		if False == group:
			self.error = True
			self.message = 'Invalid group. '
		
		user = helper.getUser(user)
		if False == user:
			self. error = True
			self.message = 'User not found'
		
		if not helper.groupeStateWritePermission(user, group):
			self.error = True
			self.message = 'No permission to change this group. '
			
		return {
			'error': self.error,
			'message': self.message,
		}
	
