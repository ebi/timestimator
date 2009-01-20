from google.appengine.api import users
from google.appengine.ext import db


class Detail(object):
    error = False
    message = ''
    
    def addMessage(self, message):
        self.message += message + ' '
    
    def addError(self, message):
        self.error = True
        self.addMessage(message)
    
    def checkAuthorization(self, task):
        if task.owner != users.get_current_user():
            self.addError('Acced denied.')
    
    def process(self, request, taskKey):
        try:
            task = db.get(taskKey)
        except:
            self.addError('Could not get task.')
        
        self.checkAuthorization(task);
        
        retVal = {
            'error': self.error,
            'message': self.message,
        }
        if self.error:
            return retVal
        else:
            retVal['task'] = task
            retVal['estimations'] = task.estimation_set
            return retVal
