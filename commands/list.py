from google.appengine.ext import db

class DisplayTask():
    description = ''
    jira = ''
    jiraLink = ''
    owner = ''
    time = 0
    yourEstimation = 0
    averageEstimation = 0
    difference = 0

class List(object):
    knownJira = {
        'LCL': 'https://jira.local.ch/browse/'
    }

    def process(self, request):
        returnTasks = []
        tasks = db.GqlQuery("SELECT * FROM Task ORDER BY creation DESC")
        for task in tasks:
            displayTask = DisplayTask()
            displayTask.owner = task.owner.nickname
            displayTask.description = task.description
            displayTask.time = task.time
            if '' != task.jira:
                displayTask.jira = task.jira
                if task.jira[3] in self.knownJira:
                    displayTask.jiraLink = self.knownJira[task.jira[3]]
            
            # Now do the calculations...
            estimationsCount = 0
            estimationTime = 0
            for estimation in task.estimation_set:
                estimationsCount += 1
                estimationTime += estimation.time
                if estimation.owner == task.owner:
                    displayTask.yourEstimation = estimation.time
            displayTask.averageEstimation = estimationTime / estimationsCount
            if displayTask.yourEstimation > 0 and displayTask.time > 0:
                displayTask.difference = (displayTask.time - displayTask.yourEstimation) / displayTask.yourEstimation * 100
            returnTasks.append(displayTask)
        return {
            'tasks': returnTasks,
        }
