import re,sys,os
from xml.etree import ElementTree

try:
	f = open(os.getcwd()+'\\'+'s.xml','r')
	root = ElementTree.fromstring(f.read())
	lst_node = root.getiterator("contacts")
	result=[]
	name=[]
	for node in lst_node:
		print node.getchildren()
		# eventID = node.attrib['firstName']
		# eventCalendarID = node.attrib['lastName']
		# name.append(eventID)
		# name.append(eventCalendarID)
		# result.append(name)
	# print result
	f.close()
except Exception,e:
	print (e)	
