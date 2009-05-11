import models
import helper
from google.appengine.ext import db
from google.appengine.api import users

class Detail(object):
	def process(self, request, groupKey):
		group = helper.getGroup(groupKey)
		if False == group:
			self.redirect('/groups')
		members = models.GroupMember.gql('WHERE group = :1', group)
		permission = models.GroupMember.gql('WHERE group = :1 and name = :2', group, users.get_current_user())
		if 0 == permission.count():
			permission = 0
		else:
			permission = permission.get().status
		
		return {
			'group': group,
			'members': members,
			'permission': permission
		}
	