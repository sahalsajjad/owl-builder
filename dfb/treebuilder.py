#######################################################################################################
#  OWL Tree Builder																					  #
#  Code written by: Sahal Sajjad, email:sahalsajjad@gmail.com										  #
#  Copyright: 																						  #
#		You are free to modify this code and use for any non-commercial use, provided that the author #
#		Sahal Sajjad is acknowledged. Under no circumstances shall the name of the author be used for #
#     any kind of promotion for the modified code without prior permission.							  #
#######################################################################################################
'''
	Dependencies: 
			1. ontospy
'''
from ontospy import *
import json

def getChildren(classReference, classes):
	L = list()
	for c in classes:
		L.append(classReference[c.locale]["id"])
	return L

def assignClassIds(classes):
	classReference = dict()
	classReference["null"]="null"
	for x in range(len(classes)):
		classReference[classes[x].locale] = dict()
		classReference[classes[x].locale]["id"] = x
		

	return classReference	

def assignChildren(classReference, classes):
	for x in classes:
		classReference[x.locale]["children"] = getChildren(classReference, x.children())
	return classReference
		
def buildTree(classes, Warehouse, depth, classReference, parent):
	for r in classes:
		if depth not in Warehouse.keys():
			Warehouse[depth] = list()
			
		if len(r.children()) > 0:
			buildTree(r.children(), Warehouse, depth+1, classReference, classReference[r.locale])
		class_id = classReference[r.locale]["id"]	
		Warehouse[depth].append({
			"id":class_id,
			"class":r.locale,
			"children":getChildren(classReference, r.children()),
			"parent":parent
			})	
	return Warehouse

def buildTreeJsonResponse(graph):
	'''
	Interface method for serializing an owl with classes and properties as an editable Tree.
	'''
	Warehouse = dict()
	classes = graph.classes
	properties = graph.properties
	ROOTCLASSES = list()
	for i in range(len(classes)):
		c = classes[i]
		children = c.children()
		parents = c.parents()
		if len(parents) == 0:
			ROOTCLASSES.append(c)
	classReference = assignClassIds(graph.classes)
	classReferenceWithChildren = assignChildren(classReference, graph.classes)		
	data = json.dumps(buildTree(ROOTCLASSES, Warehouse, 0, classReferenceWithChildren, "null"),indent=2)
	
	return {"data":data, "classReference": json.dumps(classReference, indent=2) }	
			


