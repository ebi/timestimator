import models
from google.appengine.ext import db
from google.appengine.api import users

class Overview(object):
	def getGroups(self):
		return models.Group.all()
	
	def getOwnGroups(self):
		return models.GroupMember.gql("WHERE name = :1 ORDER BY creation DESC", users.get_current_user())
	
	def getMemberRequests(self, members):
		requests = []
		for member in members:
			if 2 == member.status :
				reqs = models.GroupMember.gql('WHERE group = :1 AND status = 0', member.group)
				for request in reqs:
					requests.append(request)
		return requests
	
	def process(self, request):
		ownGroups = self.getOwnGroups()
		return {
			'groups': self.getGroups(),
			'member': ownGroups,
			'requests': self.getMemberRequests(ownGroups)
		}
	
