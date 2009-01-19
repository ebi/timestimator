import locale
import re

class Add(object):
    error = False
    message = ''
    knownJira = {
        'LCL': 'https://jira.local.ch/browse/'
    }
    
    def process(self, request):
        description = request.get('description')
        estimatedTime = locale.atof(request.get('estimatedTime'))
        jira = request.get('jira')
        
        if '' == description:
            self.error = True
            self.message += 'Description is mandatory. '
        if estimatedTime <= 0:
            self.error = True
            self.message += 'Estimated time must be a number. '
        if None == re.match('[A-Z]{3}-\d*', jira):
            self.error = True 
            self.message += 'Not a valid jira isssue. '
            
        if False == self.error:
            self.message += 'Created new task estimation'
        
        return {
            'error': self.error,
            'message': self.message,
        }
    