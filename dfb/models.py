from __future__ import unicode_literals

from django.db import models

class OWLFile(models.Model):
	time_added = models.DateTimeField(auto_now_add=True)
	owlfile = models.FileField(upload_to='')
	
