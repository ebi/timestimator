from google.appengine.ext import db

class Group(db.Model):
	name = db.StringProperty()
	creation = db.DateTimeProperty(auto_now_add=True)
	owner = db.UserProperty()

class GroupMember(db.Model):
	group = db.ReferenceProperty(Group)
	member = db.UserProperty()
	creation = db.DateTimeProperty(auto_now_add=True)

class Task(db.Model):
	owner = db.UserProperty()
	creation = db.DateTimeProperty(auto_now_add=True)
	description = db.StringProperty()
	jira = db.StringProperty()
	time = db.FloatProperty()
	estimateCount = db.IntegerProperty()
	estimateAverage = db.FloatProperty()
	group = db.ReferenceProperty(Group)

class Estimation(db.Model):
	taskId = db.ReferenceProperty(Task)
	owner = db.UserProperty()
	creation = db.DateTimeProperty(auto_now_add=True)
	time = db.FloatProperty()

