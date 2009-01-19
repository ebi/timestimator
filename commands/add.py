class add(object):
    error = False
    message = 'Added new task estimation'
    def process(self, request):
        description = request.get('description')
        if '' == description:
            self.error = True
            self.message = 'Description is mandatory'
        return {
            'error': self.error,
            'message': self.message,
        }
    