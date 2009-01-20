from google.appengine.ext import db
from google.appengine.api import users

class DisplayTask():
    key = None
    description = None
    jira = None
    jiraLink = None
    owner = None
    time = None
    yourEstimation = None
    averageEstimation = None
    difference = None

class List(object):
    knownJira = {
        'LCL': 'https://jira.local.ch/browse/'
    }

    def process(self, request):
        returnTasks = []
        tasks = db.GqlQuery("SELECT * FROM Task ORDER BY creation DESC")
        for task in tasks:
            displayTask = DisplayTask()
            displayTask.key = task.key()
            displayTask.owner = task.owner.nickname
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
            displayTask.averageEstimation = estimationTime / estimationsCount
            if (displayTask.yourEstimation > 0) and (None != displayTask.time):
                displayTask.difference = (displayTask.time - displayTask.yourEstimation) / displayTask.yourEstimation * 100
            returnTasks.append(displayTask)
        return {
            'tasks': returnTasks,
        }
