import locale
import re
import cgi
from google.appengine.ext import db
from google.appengine.api import users

class Add(object):
    error = False
    message = ''


    def createTask(self):
        description = self.request.get('description')
        jira = self.request.get('jira')
        
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
            task = Task()
            task.owner = users.get_current_user()
            task.description = cgi.escape(description)
            if '' != jira:
                task.jira = cgi.escape(jira)
            task.put()
            self.message += 'Created new task. '
            return task
        else:
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
        
        estimation = Estimation()
        estimation.taskId = task
        estimation.owner = users.get_current_user()
        estimation.time = estimatedTime
        estimation.put()
        self.message += 'Created new estimation. '
        return True
    
    def process(self, request, taskKey=None):
        self.request = request
        if None == taskKey:
            task = self.createTask()
        else:
            task = db.get(taskKey)
        
        if not task:
            self.error = True
            self.message += 'Could not get or create task. '
        else:
            self.createEstimation(task)
        
        # Everything worked out
        return {
            'error': self.error,
            'message': self.message,
        }

class Task(db.Model):
    owner = db.UserProperty()
    creation = db.DateTimeProperty(auto_now_add=True)
    description = db.StringProperty()
    jira = db.StringProperty()
    time = db.FloatProperty()

class Estimation(db.Model):
    taskId = db.ReferenceProperty(Task)
    owner = db.UserProperty()
    creation = db.DateTimeProperty(auto_now_add=True)
    time = db.FloatProperty()
