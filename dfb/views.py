from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from dfb.forms import *
from dfb.models import *
from dfb.owlbuilder import *
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponseRedirect
from .treebuilder import buildTreeJsonResponse
from ontospy import *
from rdflib.plugins.serializers.rdfxml import PrettyXMLSerializer

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
			propertyReference = response.get("propertyReference")
			context['data']=data
			f = open('dfb/static/js/data.json',"w")
			f.write("data=")
			f.write(data)
			f.close()
			s = open('dfb/static/js/classreference.json',"w")			
			s.write("classReference=")
			s.write(classReference)
			s.close()
			a = open('dfb/static/js/propreference.json',"w")			
			a.write("propertyReference=")
			a.write(json.dumps(propertyReference, indent=2))
			a.close()
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

def keyIndexAndType(key):
	key = key.replace('form_data','')
	key = key.replace(']','')
	key = key[1:]
	types = key.split('[')
	return types

@csrf_exempt
def submit(request):
	post=request.POST
	post_dict = dict(post.iterlists())
	VALUES = []
	for k in post_dict.keys():
		if len(post_dict[k])==4:
			VALUES.append({"class":post_dict[k][0].split("~~~~~")[-1],
					   "value":post_dict[k][1],
					   "property":post_dict[k][2],
					   "isProperty":post_dict[k][3],
					   "datatype":None
					  })
		elif len(post_dict[k]) == 5:
			VALUES.append({"class":post_dict[k][0].split("~~~~~")[-1],
					   "value":post_dict[k][1],
					   "property":post_dict[k][2],
					   "isProperty":post_dict[k][3],
					   "datatype":post_dict[k][4]
			})
	
	
	owlpath = OWLFile.objects.order_by('-time_added')[0].owlfile.path
	response = buildOWL(owlpath, VALUES)
	f = open('dfb/static/outputs/out.owl',"w")
	p = open(owlpath,"r")
	i=1
	for x in p.readlines():
		if i < response['num_l']:
			f.write(x)
		i+=1	
	
	f.write(response['Individual'])
	f.write(response['end'])
	f.close()
	
	return HttpResponseRedirect('/output/')			

class Output(TemplateView):
	template_name="output.html"
	def get_context_data(self, **kwargs):		
		context = super(Output, self).get_context_data(**kwargs)
		return context
