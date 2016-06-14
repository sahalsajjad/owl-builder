from django.shortcuts import render, render_to_response
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from dfb.forms import *
from dfb.models import *
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponseRedirect
from treebuilder import buildTreeJsonResponse
from ontospy import *

class Run(TemplateView):
	template_name='run.html'
	def get_context_data(self, **kwargs):
		context = super(Run, self).get_context_data(**kwargs)
		uploadedowl = OWLFile.objects.order_by('-time_added')
		try:
			upload = uploadedowl[0]
			graph = Graph(str(upload.owlfile.path))
			response = buildTreeJsonResponse(graph)
			data = response.get("data")
			classReference = response.get("classReference")
			context['data']=data
			f = open('dfb/static/js/data.json',"w")
			s = open('dfb/static/js/serialize.json',"w")
			
			f.write("data=")
			f.write(data)
			
			s.write("classReference=")
			s.write(classReference)
			context['status']=200
		except IndexError:
			donothing = True
			context['status']=500
		return context

class Upload(FormView):
	template_name = 'index.html'
	form_class = UploadOWLFileForm
	success_url = '/build-form/'
	def get_context_data(self, **kwargs):
		context = super(Upload, self).get_context_data(**kwargs)
		context['form'] = UploadOWLFileForm(self.request.POST, self.request.FILES)
		return context
	def form_valid(self, form):
		form.save()
		return HttpResponseRedirect(self.success_url)
	def form_invalid(self, form):
		return super(Upload, self).form_invalid(form)

@csrf_exempt
def submit(request):
	KEYS = request.GET.keys()
	DATA = [];
	for k in range(0,len(KEYS),2):
		DATA.append({"classes":request.GET.get(KEYS[k]),"value": request.GET.get(KEYS[k+1])})
	print DATA	
	return HttpResponseRedirect('/')			
		

