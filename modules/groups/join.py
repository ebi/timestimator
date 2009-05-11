import models
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import mail

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
						user = users.get_current_user()
						sender_address = user.email()
						subject = '[timestimator] request accepted'
						body = """%s has accepted your request to join the group %s.""" % (user.nickname(), group.name)
						mail.send_mail(sender_address, member.name.email(), subject, body)
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
					user = users.get_current_user()
					member = models.GroupMember(
						group = group.key(),
						name = user,
						status = 0,
					)
					member.put()
					sender_address = user.email()
					subject = '[timestimator] ' + user.nickname() + 'requested to join ' + group.name
					body = """%s requested to join your group %s.
Visit http://timestimator.gorn.ch/groups to accept or deny the request.
					""" % (user.nickname(), group.name)
					mail.send_mail(sender_address, group.owner.email(), subject, body)
					self.message = 'Requested to join group.'
		return {
			'error': self.error,
			'message': self.message
		}
	
