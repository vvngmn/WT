from xml.dom.minidom import Document
import urllib2,urllib,re,os,sys, httplib, httplib2
import sqlite3, cookielib, time, datetime
from urllib import urlencode
from cookielib import CookieJar

URLLINK = 'http://http.btstaging.cpcloud.co.uk/cp/dd' #ENV	http://btdantefe01.cpth.ie:8080/cp/dd	
# global CURRENT_USER # qa.596.user29@uat.cpcloud.co.uk	build768.user22@test.ie
CURRENT_USER = 'build768.user22@test.ie' # qa.596.user29@uat.cpcloud.co.uk	
timeout = 60
urllib2.socket.setdefaulttimeout(timeout)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(CookieJar())) 

class xmlHandler():
	def __init__(self,actionName):
		'''
			param:
				actionName - node name of action in xml model (eg.'contacts' in <request><contacts action="update_contact" ...)
				actionName treat like Root name of this xml, all child nodes should belong to this node, because:
					1: Python not allow 2 childs belong to real root 'request'
					2: One request only need one node by name of action
		'''
		self.doc = Document()
		self.request = self.doc.createElement('request')
		self.doc.appendChild(self.request)
		
		self.actionName = self.doc.createElement(actionName)
		self.request.appendChild(self.actionName)
	
	def addNode(self,newNode,parent=False):
		'''
			params:
				newNode (String) - child node name.
				parent (Node)- parent node. DEFAULT: parent will be the root (eg. parent is 'contacts')
		'''
		if not parent:
			parent = self.actionName
		self.child = self.doc.createElement(newNode)
		parent.appendChild(self.child)
		return self.child
		
	def addAttri(self,attrHash={'action':'hah'},tarNode=False):
		'''
			params:
				attrHash - all attributes needed to add by the type of hash.
				tarNode (Node) - The one Node need to add attributes.
					DEFAULT: add attribute for the root node name (eg. attributes for 'contacts')
		'''
		if not tarNode:
			tarNode = self.actionName
		for attribute in attrHash.items():
			# print 'adding '+ attribute[0]+' , '+attribute[1]
			tarNode.setAttribute(attribute[0],attribute[1])
			# print self.doc.toxml().replace('<?xml version="1.0" ?>','')
			# print '=============='
	
	def toxml(self):
		return self.doc.toxml().replace('<?xml version="1.0" ?>','')
 
class initHandler():
	def login(self,user=CURRENT_USER,urlLink=URLLINK):
		try:
			data = {
				'r':'<request><user action="login" username="%s" password="password" rememberme="false"></user></request>'%user
				}
			response = opener.open(urllib2.Request(urlLink), urllib.urlencode(data))
			res = response.read()
			if 'error code' in res:
				print 'error code:	'+ re.findall('''error code="(.*)">.*''',res)[0]
			else:
				print 'Login OK!'
			return opener
		except Exception,e:
			print (e)
	 
		
if __name__ == '__main__':
	xml = xmlHandler(actionName='contacts')
	
	contactsHash={'action':'update_contact','addressBookId':'PAB://uat.cpcloud.co.uk/qa.793.user40/main'}
	xml.addAttri(contactsHash)
	
	contactNode = xml.addNode(newNode='contact')
	contactHash = {'fistName':'firstNamehahahah','lastName':'lastNamelolol'}
	xml.addAttri(tarNode=contactNode,attrHash=contactHash)
	
	contactfield  = xml.addNode(newNode='contactfield',parent=contactNode)
	contactfieldHash = {'value':"5middlename", 'primary':"false", 'type':"lzHeader", 'label':"middlename"}
	xml.addAttri(tarNode=contactfield,attrHash=contactfieldHash)
	
	print xml.toxml()
	