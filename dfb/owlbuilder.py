#######################################################################################################
#  OWLBuilder Entities																					  #
#  Code written by: Sahal Sajjad, email:sahalsajjad@gmail.com										  #
#  Copyright: 																						  #
#		You are free to modify this code and use for any non-commercial use, provided that the author #
#		Sahal Sajjad is acknowledged. Under no circumstances shall the name of the author be used for #
#     any kind of promotion for the modified code without prior permission.							  #
#######################################################################################################
from rdflib import Graph
from rdflib.plugins.serializers.rdfxml import PrettyXMLSerializer

class Individual:
	thing = ""
	namespaces=""
	def __complex__(self, datatype, Property, property_value):
		'''
		<hasBase rdf:datatype=xsd_something>value</hasBase>
		'''
		thing_extension="<"+Property+" rdf:datatype=\"&amp;"+datatype+"\" >"+property_value+"</"+Property+">"
		return thing_extension
	
	def beautify(self, params):
		D= dict()
		for p in params:
			if p['class'] not in D.keys():
				D[p['class']]=dict()
				print p['class']
				D[p['class']]["Class"]=p['class']
			if p['isProperty'] == "True":
				print "Accesssing Property",p['property']
				if "property_list" in D[p['class']].keys():
					print "in keys"
					D[p['class']]["property_list"].append(tuple([p['datatype'],p['property'] ,p['value']]))
				else:
					print "not in keys"
					D[p['class']]["property_list"]=list()
					D[p['class']]["property_list"].append(tuple([ p['datatype'],p['property'],p['value']]))
			else:
				D[p['class']]['instance']=p['value']

		return D

	def build(self, params):
		task_list = self.beautify(params)

		thing=""
		for _t in task_list.keys():
			t = task_list[_t]
			print t
			instance = t.get('instance')

			Class = t.get('Class')
			property_list = t.get('property_list')
			
			thing+="<owl:Thing rdf:about=\"#"+instance+"\">\n<rdf:type rdf:resource=\"#"+Class+"\"/>\n"
			for p in property_list:
				dt= p[0]
				pp= p[1]
				pv= p[2]
				thing+= self.__complex__(dt, pp, pv)
			thing+="\n</owl:Thing>\n"	
		return thing			
	def namespaces(self):
		return self.namespaces
	def __set_namespaces__(self, namespaces):
		self.namespaces = namespaces
	
def buildOWL(path, individual_params):
	individual = Individual()
	write_content = individual.build(individual_params)
	end="\n</rdf:RDF>"
	
	with open(path) as g:
		num_l = sum(1 for _ in g)
	return {"Individual":write_content, "end":end, "num_l":num_l}
	
