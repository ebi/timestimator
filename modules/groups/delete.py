import models
from google.appengine.ext import db
from google.appengine.api import users

class Delete(object):
	error = False
	message = ''
	
	def process(self):
		return {
			'error': self.error,
			'message': self.message,
		}
	
