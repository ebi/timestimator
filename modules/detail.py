import re
import locale

from google.appengine.api import users
from google.appengine.ext import db

__all__ = ['Detail']

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
            return False
        else:
            return True
    
    def process(self, request, taskKey):
        try:
            task = db.get(taskKey)
        except:
            self.addError('Could not get task.')
        
        authorized = self.checkAuthorization(task);
        if authorized and 'POST' == request.method:
            time = request.get('time')
            if time:
                if re.match('^\d+\.?\d*$', time):
                    if task.time:
                        self.addError('Time already set.')
                    else:
                        time = locale.atof(time)
                        task.time = time
                        task.put()
                else:
                    self.addError('Time must be a number.')
        
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
