import types
import models
from google.appengine.ext import db
from google.appengine.api import users

def getGroup(group):
	if types.StringType == type(group):
		try:
			return db.get(group)
		except:
			return False
	else:
		return group

def getUser(user):
	if types.UnicodeType == type(user):
		return users.User(user)
	else:
		return user
	

def isUserInGroup(user, group):
	user = getUser(user)
	group = getGroup(group)
		
	permissions = models.GroupMember.gql('WHERE group = :1 AND name = :2 and status > 0', group, user)
	if permissions.count() > 0:
		return True
	else:
		return False
		
def isUserAdmin(user, group):
	user = getUser(user)
	group = getGroup(group)
	
	permissions = models.GroupMember.gql('WHERE group = :1 AND name = :2 and status = 2', group, user)
	if permissions.count() > 0:
		return True
	else:
		return False

def groupeStateWritePermission(user, group):
	user = getUser(user)
	group = getGroup(group)
	
	if isUserInGroup(user, group):
		return True
	else:
		return isUserAdmin(user, group)
	
