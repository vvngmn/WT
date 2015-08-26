import urllib2, urllib, httplib
import re,os,sys, time, datetime,random

class Settings():
	def __init__(self,opener,urlLink,user):
		self.opener = opener
		self.urlLink = urlLink
		self.user = user
		self.dom = user.split('@')[1]

	def setGMT(self,gmtNum=8):
		print 'Set GMT: '+str(gmtNum)
		if gmtNum==8:
			zone = 'Asia/Hong_Kong'
		elif gmtNum==0:
			zone = 'Europe/London'
		else:
			print 'Please give a valid GMT number for zone'
		xml = '''
			<request><timezone action="set" zoneId="%s"></timezone></request>
			'''%zone
		postData = {'r':xml}		
		response = self.opener.open(urllib2.Request(self.urlLink), urllib.urlencode(postData))
		res = response.read()
		if 'error code' in res:
			print 'timezone set in testSetting error:	'+ re.findall('''error code="(.*)">.*''',res)[0]
		else:
			print 'timezone set in testSetting OK!'
			
	def createMailAlias(self,num,verify=True):
		for n in range(num):
			print 'create mail alias No.'+str(n+1)
			print self.user
			suffix = random.randint(1,1000) # make sure not to duplicate the name
			xml = '''
				<request><mailAlias action="create"><mailalias name="MyAlias%s(%s)@%s" address="%s" accountName="DefaultMailAccount"/></mailAlias></request>
				'''%(str(n+1),suffix,'devmybtinternet.com',self.user)
			postData = {'r':xml}		
			response = self.opener.open(urllib2.Request(self.urlLink), urllib.urlencode(postData))
			res = response.read()
			if 'error code' in res:
				print 'create mailAlias action error:	'+ re.findall('''error code="(.*)">.*''',res)[0]
			else:
				print 'create mailAlias action OK!'
			if verify:
				self.checkAliasList()
	
	def checkAliasList(self):
		xml = '''<request><mailAlias action="list" accountName="DefaultMailAccount"/></request>'''
		postData = {'r':xml}		
		response = self.opener.open(urllib2.Request(self.urlLink), urllib.urlencode(postData))
		res = response.read()
		if 'error code' in res:
			print 'check mailAlias list error:	'+ re.findall('''error code="(.*)">.*''',res)[0]
		else:
			print 'check mailAlias list action OK!'
	