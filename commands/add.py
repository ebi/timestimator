class add(object):
    error = False
    message = 'Added new task estimation'
    knownJira = {
        'LCL': 'https://jira.local.ch/browse/'
    }
    
    def process(self, request):
        description = request.get('description')
        estimatedTime = locale.atof(request.get('estimatedTime'))
        print estimatedTime
        if '' == description:
            self.error = True
            self.message = 'Description is mandatory.'
        if estimatedTime <= 0:
            self.error = True
            self.message = 'Estimated time must be a number.'
        
        return {
            'error': self.error,
            'message': self.message,
        }
    