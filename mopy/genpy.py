#!/usr/bin/env python
# encoding: utf-8
"""
genpy.py

Generate model.py, which defines a Python class for each class in the Music Ontology.

Created by Chris Sutton on 2007-08-10.
Copyright (c) 2007 Chris Sutton. All rights reserved.
"""

import sys
import time
import os
from os import mkdir
import rdflib; from rdflib import RDF, RDFS, BNode
from rdflib.Collection import Collection

OWL = rdflib.Namespace("http://www.w3.org/2002/07/owl#")

class Generator:
	def __init__(self, graph, target_class):
		self.graph = graph
		self.c = target_class
		[self.ns, self.name] = self.graph.qname(self.c).split(":")
		self.filename = "model.py"
		self.out = []
		self.write = self.out.append
		self.hdr = ""
		self.classDef=""
		self.init ="\tdef __init__(self,URI=None):\n"
		self.props = ""
		self.utils = ""

		# Do we have any non-inherited properties ?
		self.properties = self.getProperties()
		self.haveProperties = len(self.properties) > 0

	def printAll(self):
		self.addHeader()
		self.addClassDef()
		self.addInit()
		self.addProperties()
		self.addUtils()
		self.write(self.classDef)
		self.write(self.hdr)
		self.write(self.init)
		self.write(self.props)
		self.write(self.utils)
		self.out = "".join(self.out)


	def addHeader(self):
		self.hdr = '\t"""\n'
		self.hdr+="\t"+self.ns+":"+self.name+"\n"
		for comment in self.graph.objects(self.c, RDFS.comment):
			self.hdr+="\t"+comment+"\n"
		self.hdr+= '\t"""\n'

	def addClassDef(self):
		cd=""
		parentURIs = self.getParents()
		parentqnames = [self.graph.qname(p) for p in parentURIs]
		parentpynames = [ClassQNameToPyClassName(q) for q in parentqnames]
		parentpynames.sort() # For consistency across runs
		self.classDef+="\nclass "+self.name+"("
		if len(parentpynames)==0:
			cd+="object"
		else:
			cd+=", ".join(parentpynames)
		cd+="):\n"
		self.classDef += cd
		

	def addInit(self):
		parentURIs = self.getParents()
		parentqnames = [self.graph.qname(p) for p in parentURIs]
		parentpynames = [ClassQNameToPyClassName(q) for q in parentqnames]
		if len(parentpynames)>0:
			self.init+="\t\t# Initialise parents\n"
		for p in parentpynames:
			self.init+="\t\t"+p+".__init__(self)\n"
		
		self.init+="\t\tself._initialised = False\n"
		self.init+="\t\tself.shortname = \""+self.name+"\"\n"
		self.init+="\t\tself.URI = URI\n"
		if self.haveProperties:
			self.init+="\t\tself._props = getattr(self,\"_props\",{}) # Initialise if a parent class hasn't already\n"

			
	def addProperties(self):
		self.props+="\tclassURI = \""+str(self.c)+"\"\n"
		if self.haveProperties:
			self.props+="\n\n\t# Python class properties to wrap the PropertySet objects\n"
		for prop in self.properties:
				propname = PropQNameToPyName(self.graph.qname(prop))
				URIstr = str(prop)
				validTypes = ""
				rTypes = self.graph.objects(prop, RDFS.range)
				rTypeNames = []
				allowLits=False
				for rT in rTypes:
					if isinstance(rT, BNode):
						try:
							un = (self.graph.objects(rT,OWL["unionOf"])).next()
							col = Collection(self.graph, un)
							for c in col:
								rTypeNames.append(ClassQNameToPyClassName(self.graph.qname(c)))
						except StopIteration:
							print "Unhandled Blind Node in addProperties ! No unionOf found. Triples :"
							print "\n".join(list(self.graph.triples(rT,None,None)))
							raise Exception("Unhandled Blind Node in addProperties !")
					else:
						rTypeNames.append(ClassQNameToPyClassName(self.graph.qname(rT)))
				if "Literal" in rTypeNames:
					allowLits=True
					rTypeNames.remove("Literal")
				if len(rTypeNames) > 1:
					validTypes="("+",".join(rTypeNames)+")"
				elif len(rTypeNames) == 1:
					validTypes=rTypeNames[0]
				else:
					validTypes="None"

				self.init+="\t\tself._props[\""+propname+"\"] = PropertySet(\""+propname+"\",\""+URIstr+"\", "+validTypes
				self.init+=", "+str(allowLits)+")\n"
				# Wrap the PropertySet up to be usable and protected :
				self.props+="\t" + propname + " = property(fget=lambda x: x._props[\"" + propname + "\"].get()"\
														", fset=lambda x,y : x._props[\"" + propname + "\"].set(y)"\
														", fdel=None, doc=propDocs[\""+propname+"\"])\n"
		self.init+="\t\tself._initialised = True\n"
		
	def addUtils(self):
		self.utils+="\n\t# Utility methods\n" # TODO : serialisation routine here ?
		self.utils+="\t__setattr__ = protector\n"
		self.utils+="\t__str__ = objToStr\n"
#		self.utils+="\tpass\n\n"
	
	def getProperties(self):
		props=[]
		for prop in self.graph.subjects(RDF.type, RDF.Property):
			# Simple case : Named explicitly in property's domain
			if len(list(self.graph.triples((prop,RDFS.domain,self.c)))) > 0:
				props.append(prop)
			# Harder case : Named in a collection in property's domain
			for bn in (o for (s,p,o) in self.graph.triples((prop,RDFS.domain,None)) if isinstance(o, BNode)):
				try:
					un = (self.graph.objects(bn,OWL["unionOf"])).next()
					domain = Collection(self.graph, un)
					if self.c in domain:
						props.append(prop)
				except StopIteration:
					print "Unhandled Blind Node in getProperties ! No unionOf found. Triples :"
					print "\n".join(list(self.graph.triples(bn,None,None)))
					raise Exception("Unhandled Blind Node in getProperties")
		props.sort() # Aid consistency of generated code
		return props

	def getParents(self):
		p = list(self.graph.objects(self.c, RDFS.subClassOf))
		if (self.c != OWL.Thing) and (len(p) == 0):
			if self.c == RDFS.Resource:
				p.append(OWL.Thing)
			else:
				p.append(RDFS.Resource)
		p.sort()
		return p

def PropQNameToPyName(qname):
#	return qname.replace(":","_") # Probably don't need namespace in property names
	return qname.split(":")[1]
	
def ClassQNameToPyModuleName(qname):
	return qname.replace(":",".")
def ClassQNameToPyClassName(qname):
	return qname.split(":")[1]


def main():
	spec_g = rdflib.ConjunctiveGraph()
	print "Loading ontology documents..."
	spec_g.load("../mo/rdf/musicontology.rdfs")
	spec_g.load("extras.rdfs")

	model = open("model.py", "w")
	model.write("""
# ===================================================================
# = model.py - Core and External Classes of the Music Ontology 
# =            Generated automatically on """+time.asctime()+"""
# ===================================================================\n\n\n""")

	model.write("from PropertySet import PropertySet, protector\n\n")
	classes = list(s for s in spec_g.subjects(RDF.type, OWL.Class) if type(s) != BNode) # rdflib says rdfs:Class is a subClass of owl:Class - check !
	classtxt = {}
	parents = {}
	
	#
	# Generate text
	#

	objToStr = """
def objToStr(c):
	s = "-- "+c.shortname
	if c.URI != None :
		s+=" @ "+str(c.URI)
	s+=" --\\n"
	for p in c._props.keys():
		for v in c._props[p]:
			s+=c._props[p].shortname + " : "
			if isinstance(v, c._props[p].Lits):
				s+=str(v)
			else:
				s+=str(type(v))
				if hasattr(v,"URI"):
					s+=" @ "+v.URI
			s +="\\n"
	return s
"""
	model.write(objToStr)
	model.write("\n# ======================== Property Docstrings ====================== \n\n")
	model.write("propDocs = {}\n")
	props = list(spec_g.subjects(RDF.type, RDF.Property))
	for p in props:
		doc = "".join(spec_g.objects(p, RDFS.comment))
		if len(doc) > 0:
			model.write("propDocs[\""+PropQNameToPyName(spec_g.qname(p))+"\"]=\\\n\"\"\""+doc.strip()+"\"\"\"\n")
		else:
			model.write("propDocs[\""+PropQNameToPyName(spec_g.qname(p))+"\"]=\"\"\n")
		
	model.write("\n\n\n\n# ========================  Class Definitions  ====================== \n")
	for c in classes:
		print "processing " + str(c)
		g = Generator(spec_g, c)
		g.printAll()
		classtxt[str(c)] = g.out
		parents[str(c)] = [str(p) for p in g.getParents()]

	#
	# Serialise classes in an appropriate order
	#
	classes = [str(c) for c in classes]
	classes.sort() # Ensure serialisation order is reasonably consistent across runs
	n=1; lastlen = len(classes)+1
	while (len(classes) > 0) and len(classes) < lastlen:
		lastlen = len(classes)
		print("pass "+ str(n))
		for c in classes:
			if len(parents[c]) == 0: # Write out orphans immediately
				model.write(classtxt[c])
				print(" wrote "+c)
				classes.remove(c)
				for k in classes:    # And abandon any classes who were waiting for us
					if c in parents[k]:
						parents[k].remove(c)
		n+=1

	if len(classes) > 0:
		print "Couldn't find a serialisation order ! Remaining classes : " + "\n".join(classes)

	model.close()

if __name__ == '__main__':
	main()

