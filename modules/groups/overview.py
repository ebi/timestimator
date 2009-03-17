import models
from google.appengine.ext import db
from google.appengine.api import users

def getGroups():
	return models.Group.all()

def getOwnGroups():
	return models.GroupMember.gql("WHERE name = :1 ORDER BY creation DESC", users.get_current_user())

def getConfirmedOwnGroups():
	return models.GroupMember.gql("WHERE name = :1 AND status > 0", users.get_current_user())

def getMemberRequests(members):
	requests = []
	for member in members:
		if 2 == member.status :
			reqs = models.GroupMember.gql('WHERE group = :1 AND status = 0', member.group)
			for request in reqs:
				requests.append(request)
	return requests

class Overview(object):
	def process(self, request):
		ownGroups = getOwnGroups()
		return {
			'groups': getGroups(),
			'member': ownGroups,
			'requests': getMemberRequests(ownGroups)
		}
	
