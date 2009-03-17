import models
from google.appengine.ext import db
from google.appengine.api import users


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
					if 'True' == request.get('setAdmin'):
						self.message = 'Admin privileges granted.'
						member.status = 2
					else: 
						self.message = 'Join request accepted.'
						member.status = 1;
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
		return {
			'error': self.error,
			'message': self.message
		}
	
