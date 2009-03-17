import types
import models
from google.appengine.ext import db

def isUserInGroup(user, group):
	if types.StringType == type(user):
		user = users.User(user)
	
	if types.StringType == type(group):
		try:
			print group
			group = db.get(group)
		except:
			return False
	permissions = models.GroupMember.gql('WHERE group = :1 AND name = :2 and status > 0', group, user)
	if permissions.count() > 0:
		return True
	else:
		return False
	
