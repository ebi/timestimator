import models
import helper
from google.appengine.ext import db
from google.appengine.api import users

class Delete(object):
	error = False
	message = ''
	
	def setError(self, msg):
		self.error = True
		self.message += msg 
	
	def process(self, request, groupKey):
		if request.get('delete') != groupKey:
			self.setError("GroupId in body doesn't match URL")
			
		group = helper.getGroup(groupKey)
		if False == group:
			self.error = True
			self.message = 'Invalid group. '
		
		if request.get('delMember'):
			user = helper.getUser(request.get('delMember'))
		else:
			user = helper.getUser(users.get_current_user())
		
		if False == user:
			self.setError('User not found')
		
		if users.get_current_user() != user and not helper.groupeStateWritePermission(users.get_current_user(), group):
			self.setError('No permission to change this group. ')
			
		if False == self.error:
			members = models.GroupMember.gql('WHERE name = :1 and group = :2', user, group)
			if 0 == members.count():
				self.setError("Can't find group membership. ")
			else:
				member = members.get();
				member.delete();
				self.message = 'Successfully deleted group membership. '
			
			# If that was the last member kill the group
			members = models.GroupMember.gql('WHERE group = :1', group)
			if 0 == members.count():
				group.delete()
			
		
		return {
			'error': self.error,
			'message': self.message,
		}
	
