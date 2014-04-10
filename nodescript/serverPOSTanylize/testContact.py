import Handler, ContactModel
import ContactModel
import urllib2,urllib,re,os,sys, httplib, httplib2
import sqlite3, cookielib, time, datetime
from urllib import urlencode
from cookielib import CookieJar
URLLINK = 'http://btdantefe01.cpth.ie:6030/cp/dd' #ENV	http://http.btstaging.cpcloud.co.uk/cp/dd	
# global CURRENT_USER # qa.596.user29@uat.cpcloud.co.uk	build768.user22@test.ie
CURRENT_USER = 'build859.user40@qa.dom' # qa.596.user29@uat.cpcloud.co.uk	
timeout = 60
urllib2.socket.setdefaulttimeout(timeout)
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(CookieJar())) 


class contactSets():
	def __init__(self):
		self.fName='testF'
		self.lName='testL'
		self.mName='testM'
		self.dom = CURRENT_USER.split('@')[1]
		self.username = CURRENT_USER.split('@')[0]
	
		self.initHandler = Handler.initHandler()
		self.opener = self.initHandler.login(CURRENT_USER,URLLINK)
		self.contactModle = ContactModel.ContactModel(dom=self.dom, username=self.username)
		
	def testCreateContacts(self):
		'''
			# TO BE REMOVED
			param:
				contactInfo[] : [firstname, middlename, lastname, email]
		'''
		# print contactInfo
		try:
			print 'create_contact'
			postData = {
				'r':self.contactModle.saveSimpleContact(action='create_contact',fName=self.fName, lName=self.lName, mName=self.mName)
				}
			# print postData
			response = self.opener.open(urllib2.Request(URLLINK), urllib.urlencode(postData))
			res = response.read()
			if 'error code' in res:
				print 'error code in create simple contact:	'+ re.findall('''error code="(.*)">.*''',res)[0]
				return True
			else:
				print 'create_contact simple contact OK!'
			
		except Exception,e:
			print (e)
			
if __name__ == '__main__':
	contactSets = contactSets()
	contactSets.testCreateContacts()

