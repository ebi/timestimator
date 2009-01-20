import locale
import re
import cgi
from google.appengine.ext import db
from google.appengine.api import users

class Add(object):
    error = False
    message = ''

    def process(self, request):
        description = request.get('description')
        estimatedTime = locale.atof(request.get('estimatedTime'))
        jira = request.get('jira')
        
        # String is enough
        if '' == description:
            self.error = True
            self.message += 'Description is mandatory. '

        # Must be a proper number got converted by atof
        if estimatedTime <= 0:
            self.error = True
            self.message += 'Estimated time must be a number. '

        # jira issues look like LCL-1234
        if '' == jira or None == re.match('[A-Z]{3}-\d*', jira):
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

            # Create estimation
            estimation = Estimation()
            estimation.taskId = task.key()
            estimation.owner = users.get_current_user()
            estimation.time = estimatedTime
            estimation.put()

            # Everything worked out
            self.message += 'Created new task estimation'

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
