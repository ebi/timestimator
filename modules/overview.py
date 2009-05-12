from google.appengine.ext import db
from google.appengine.api import users
import models
import groups.overview

__all__ = ['List']

class DisplayTask():
	key = None
	description = None
	jira = None
	jiraLink = None
	group = None
	time = None
	yourEstimation = None
	averageEstimation = None
	difference = None

class List(object):
	knownJira = {
		'LCL': 'https://jira.local.ch/browse/'
	}
	
	def getTasks(self, members):
		returnTasks = []
		for member in members:
			tasks = models.Task.gql("WHERE group = :1 ORDER BY creation DESC", member.group)
			for task in tasks:
				returnTasks.append(task)
		return returnTasks
		
	
	def process(self, request):
		returnTasks = []
		members = groups.overview.getConfirmedOwnGroups()
		tasks = self.getTasks(members)
		for task in tasks:
			displayTask = DisplayTask()
			displayTask.key = task.key()
			displayTask.group = task.group
			displayTask.description = task.description
			displayTask.time = task.time
			if None != task.jira:
				displayTask.jira = task.jira
				if task.jira[:3] in self.knownJira:
					displayTask.jiraLink = self.knownJira[task.jira[:3]]
			
			# Now do the calculations...
			estimationsCount = 0
			estimationTime = 0
			for estimation in task.estimation_set:
				estimationsCount += 1
				estimationTime += estimation.time
				if estimation.owner == users.get_current_user():
					displayTask.yourEstimation = estimation.time
			if estimationsCount > 0:
				displayTask.averageEstimation = estimationTime / estimationsCount
				if (displayTask.yourEstimation > 0) and (None != displayTask.time):
					displayTask.difference = round(displayTask.yourEstimation / (displayTask.time/100) - 100, 1) * -1
			returnTasks.append(displayTask)
		return {
			'members': members,
			'tasks': returnTasks,
		}
