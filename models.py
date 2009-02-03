from google.appengine.ext import db

class Group(db.Model):
	name = db.StringProperty()
	creation = db.DateTimeProperty(auto_now_add=True)
	owner = db.UserProperty()

class GroupMember(db.Model):
	group = db.ReferenceProperty(Group,required=True)
	member = db.UserProperty(required=True)
	state = db.IntegerProperty(required=True)
	creation = db.DateTimeProperty(auto_now_add=True, required=True)

class Task(db.Model):
	owner = db.UserProperty(required=True)
	creation = db.DateTimeProperty(auto_now_add=True, required=True)
	description = db.StringProperty(required=True)
	jira = db.StringProperty()
	time = db.FloatProperty()
	estimateCount = db.IntegerProperty()
	estimateAverage = db.FloatProperty()
	group = db.ReferenceProperty(Group,required=True)

class Estimation(db.Model):
	taskId = db.ReferenceProperty(Task, required=True)
	owner = db.UserProperty(required=True)
	creation = db.DateTimeProperty(auto_now_add=True, required=True)
	time = db.FloatProperty(required=True)

