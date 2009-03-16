import models
import re
import pprint
from google.appengine.ext import db
from google.appengine.api import users

class Overview(object):
	def getGroups(self):
		return models.Group.all()
	
	def getOwnGroups(self):
		return models.GroupMember.gql("WHERE name = :1 ORDER BY creation DESC", users.get_current_user())
	
	def process(self, request):
		return {
			'groups': self.getGroups(),
			'member': self.getOwnGroups(),
		}

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

class Join(object):
	error = False
	message = ''

	def process(self, request, groupKey):
		try :
			group = db.get(groupKey);
		except:
			self.error = True
			self.message = 'Invalid group.'
		
		if False == self.error:
			memberName = users.User(request.get('addMember'))
			if memberName != users.get_current_user():
				# Check if the current user is an admin of the group
				admins = models.GroupMember.gql('WHERE group = :1 AND name = :2 AND status = 2', group, users.get_current_user())
				members = models.GroupMember.gql('WHERE group = :1 AND name = :2', group, memberName)
				if admins.count() > 0 and members.count() > 0:
					member = members.get()
					pprint.pprint(member)
					if 'True' == request.get('setAdmin'):
						member.status = 2
					else: 
						# member.status = 1;
						pass
					member.put()
				else:
					self.error = True
					self.message = 'Not authorized to add users to this group. '
			else:
				members = models.GroupMember.gql('WHERE group = :1 AND name = :2', group, memberName)
				if members.count() > 0:
					self.error = True
					self.message = 'Already member of this group.'
				else:
					member = models.GroupMember(
						group = group.key(),
						name = users.get_current_user(),
						status = 0,
					)
					member.put()
					self.message = 'Requested to join group.'
		overview = Overview()
		return {
			'groups': overview.getGroups(),
			'member': overview.getOwnGroups(),
			'error': self.error,
			'message': self.message
		}
