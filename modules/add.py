import locale
import re
import cgi
import models
from google.appengine.ext import db
from google.appengine.api import users

__all__ = ['Add']

class Add(object):
	error = False
	message = ''


	def createTask(self):
		description = self.request.get('description')
		jira = self.request.get('jira')

		#Verify that user is member of the group
		try:
			group = db.get(self.request.get('estimationGroup'))
			member = models.GroupMember.gql('WHERE group = :1 AND name = :2 AND status > 0', group, users.get_current_user())
			if member.count() != 1:
				self.error = True
				self.message += "You're not a valid member of this group! "
		except:
			self.error = True
			self.message += 'Invalid group. '
		
		# String is enough
		if '' == description:
			self.error = True
			self.message += 'Description is mandatory. '
		else:
			unique = db.GqlQuery("SELECT * FROM Task WHERE description = :1", description)
			if unique.count() > 0:
				self.error = True
				self.message += 'Task already exists. '
		
		# jira issues look like LCL-1234
		if '' != jira and None == re.match('^[A-Z]{3}-\d+$', jira):
			self.error = True 
			self.message += 'Not a valid jira isssue. '

		if False == self.error:
			# Create task
			task = models.Task(
				owner = users.get_current_user(),
				description = cgi.escape(description),
				group = group
			)
			if '' != jira:
				task.jira = cgi.escape(jira)
			task.put()
			self.message += 'Created new task. '
			return task
		else:
			self.error = True
			self.message += 'Could not create task. '
			return False
	
	def createEstimation(self, task):
		unique = db.GqlQuery("SELECT * FROM Estimation WHERE taskId = :task AND owner = :user", task=task, user=users.get_current_user())
		if unique.count() > 0:
			self.error = True
			self.message += 'Estimation already exists. '
			return False
		
		# Must be a proper number
		estimatedTime = self.request.get('estimatedTime')
		if re.match('^\d+\.?\d*$', estimatedTime):
			estimatedTime = locale.atof(estimatedTime)
			if estimatedTime <= 0:
				self.error = True
				self.message += 'Estimated time must be positive. '
				return False
		else:
			self.error = True
			self.message += 'Estimated time must be a number. '
			return False
		
		estimation = models.Estimation(
			taskId = task,
			owner = users.get_current_user(),
			time = estimatedTime
		)
		estimation.put()
		self.message += 'Created new estimation. '
		return True
	
	def process(self, request, taskKey=None):
		self.request = request
		if None == taskKey:
			task = self.createTask()
		else:
			try:
				task = db.get(taskKey)
			except:
				self.error = True
				self.message += 'Could not get task. '
		
		if False == self.error:
			self.createEstimation(task)
		
		# Everything worked out
		return {
			'error': self.error,
			'message': self.message,
		}
