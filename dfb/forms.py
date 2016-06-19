from __future__ import unicode_literals
from django.forms import ModelForm, FileInput
from dfb.models import OWLFile
class UploadOWLFileForm(ModelForm):
	class Meta:
		model = OWLFile
		fields = ('owlfile',)
		widgets = {'owlfile':FileInput(attrs={'class':'form-control'})}
		

