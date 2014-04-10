import urllib2, urllib, httplib
import re,os,sys, time, datetime
from xml.etree import ElementTree

class Task():
	def __init__(self,opener,urlLink,user):
		self.opener = opener
		self.urlLink = urlLink
		self.user = user
		
		if 'qa.dom' in self.user:
			self.calUrl = 'btdantebe.cpth.ie'
		elif 'uat' in self.user:
			self.calUrl = 'be02.btstaging.int.cpcloud.co.uk'	# hardcode
		elif 'opal' in self.user:
			self.calUrl = 'opal.qa.laszlosystems.com'
		else:
			print 'No calendar request url set to request, "opal" is missing from user account'
		
		self.port = 5229
		
	def _taskList(self):
		xml = '''
			<request><calendar action="reportToDos" calendarId="http://%s:5229/calendars/%s/"></calendar></request>
			'''%(self.calUrl,self.user)
		data = {
				'r': xml
				}
		response = self.opener.open(urllib2.Request(self.urlLink), urllib.urlencode(data))
		if 'error code' in response.read():
			print 'error code:	'+ re.findall('''error code="(.*)">.*''',res)[0]
		else:
			print 'reportToDos %s OK!'%'to find all tasks'
			print response.read()
		return response.read()
	
	
	def CreateTask(self, dueTime=False, amount=2):
		for task in range(amount):
			now = datetime.datetime.now()
			ymd = now.strftime('%Y%m%d')
			hmsStart = now.replace(hour=now.hour+task+1).strftime('%H%M%S')
			localDue = ymd + 'T' + hmsStart
			if dueTime:
				taskTitle = 'DueDate '+now.replace(hour=now.hour+task+1).strftime('%H:%M:%S')+' '
				due= 'localDue="%s"'%localDue
			else:
				taskTitle = 'Task '
				due = ''
		
			for pr in [9,5,3]:
				if pr==9:
					priority = 'Low priority'
				elif pr==5:
					priority = 'Normal priority'
				else:
					priority = 'High priority'
				for status in ['IN-PROCESS','COMPLETED','NEEDS-ACTION']:
					
					print 'post:createToDo %s %s %s'%(str(task+1),priority,status)
					xml = '''
						<request>
						<calendar action="createToDo">
						<todo calendarId="http://%s:5229/calendars/%s/" summary="%s" priority="%s" status="%s" url="" %s>
						<xproperty name="X-CP-TASKLIST" value="Default"/>
						<description/>
						</todo>
						</calendar>
						</request>
						'''%(self.calUrl,self.user,str(task+1)+taskTitle+priority,pr,status,due)
					data = {
						'r': xml
						}
					response = self.opener.open(urllib2.Request(self.urlLink), urllib.urlencode(data))
					if 'error code' in response.read():
						print 'error code:	'+ re.findall('''error code="(.*)">.*''',res)[0]
					else:
						print 'create %s OK!'%taskTitle
	
	
	
# if __name__ == '__main__':
