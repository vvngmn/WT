import urllib2, urllib, httplib
import re,os,sys, time, datetime
from xml.etree import ElementTree
# from urllib import urlencode
# from cookielib import CookieJar
# urlLink = 'http://btdantefe01.cpth.ie:8080/cp/dd' #ENV
# global CURRENT_USER # qa.596.user29@uat.cpcloud.co.uk	build768.user22@test.ie
# CURRENT_USER = '' # qa.596.user29@uat.cpcloud.co.uk	build768.user22@test.ie

# timeout = 60
# urllib2.socket.setdefaulttimeout(timeout)
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(CookieJar())) 

class Calendar():
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
		now = datetime.datetime.now()
		self.startDate = now.strftime('%Y%m%d')
		self.endDate = now.replace(year=now.year+1).strftime('%Y%m%d')
		
		self.EventListFile = os.getcwd()+'\\'+'EventList.xml' 
		self.eventsXml = open(self.EventListFile,'w')

	def loadAllEvents(self):
		localStart = self.startDate + 'T000000'
		localEnd = self.endDate + 'T000000'
		print 'post: reportEvents..'
		loadEventsXML = '''
			<request>
			<calendar action="reportEvents" eventLimit="1000"
			startTime="" endTime="" localStart="%s" localEnd="%s">
			</calendar>
			</request>
		'''%(localStart,localEnd) #  

		postdata = loadEventsXML.replace('\n','')
		# print postdata
		data = {
			'r': postdata
			}
		response = self.opener.open(urllib2.Request(self.urlLink), urllib.urlencode(data))
		self.readEvents = response.read().replace('><','>\n<')
		if 'error code' in self.readEvents:
			print 'error code:	'+ re.findall('''error code="(.*)">.*''',self.readEvents)[0]
		else:
			print 'readEvents OK!'
		self.eventsXml.write(self.readEvents)
		self.eventsXml.close()

	def clearCalendar(self):
		self.loadAllEvents()
		root = ElementTree.fromstring(self.readEvents)
		lst_node = root.getiterator("event")
		print 'post: deleteEvent.. to delete all events'
		for node in lst_node:
			eventID = node.attrib['id']
			eventCalendarID = node.attrib['calendarId']
			if '/trash'in eventCalendarID:
				pass
			else:
				clearCalendarXML = '''
					<request>
					<calendar action="deleteEvent">
					<event id="%s" calendarId="%s"/>
					</calendar>
					</request>
				'''%(eventID,eventCalendarID)
				
				postdata = clearCalendarXML.replace('\n','')
				# print postdata
				data = {
					'r': postdata
					}
				response = self.opener.open(urllib2.Request(self.urlLink), urllib.urlencode(data))
				res = response.read()
				if 'error code' in res:
					print 'error code when clearCalendar: '+ re.findall('''error code="(.*)">.*''',res)[0]
				else:
					print 'msgsend OK!'
	
	def CreateCalendar(self, calendarN=5):
		for color in range(calendarN):
			print 'post: CreateCalendar: %s '%str(color)
			xml = '''
				<calendar action="createCalendar" timezone="480"><calendar id="" name="calendar %s" color="%s"/></calendar>
				'''%(str(color),color)
			data = {
				'r': xml
				}
			response = self.opener.open(urllib2.Request(self.urlLink), urllib.urlencode(data))
			if 'error code' in response:
				print 'error code:	'+ re.findall('''error code="(.*)">.*''',res)[0]
			else:
				print 'createCalendar OK!'
	
	def CreateSingleEvent(self,categories=False, allDay=0, nextWeek=False):
		'''
			timezone="-480" GMT +8 beijing time
		'''
		now = datetime.datetime.now()
		ymd = now.strftime('%Y%m%d')
		if nextWeek:
			ymd = now.replace(day=now.day+6).strftime('%Y%m%d')
		hmsStart = now.replace(hour=now.hour+1).strftime('%H%M%S')
		hmsEnd = now.replace(hour=now.hour+2).strftime('%H%M%S')
		Start = ymd + 'T' + hmsStart
		End = ymd + 'T' + hmsEnd
		
		SingleEventL = ['general'] # create different type of events
		if categories:
			for c in ['invite', 'work', 'school', 'red', 'birthday', 'date', 'vacation', 'fun', 'bills']:
				SingleEventL.append(c)
		if allDay:
			for d in range(allDay-1): # Hardcode, create 10 all-day event type of general
				SingleEventL.append('general')
		i=0
		for ctgry in SingleEventL:
			i=i+1
			xml = '''
				<request>
				<calendar action="createEvent">
				<event calendarId="http://%s:%s/calendars/%s/" location="" summary="%s event%s start at %s" busyStatus="BUSY" localStart="%s" localEnd="%s">
				<description/>
				<categories>%s</categories>
				<xproperty name="X-EVENT-TYPE" value="%s"/>
				</event>
				</calendar>
				</request>
			'''%(self.calUrl,str(self.port),self.user, ctgry.capitalize(),str(i) ,now.replace(hour=now.hour+1).strftime('%H:%M:%S'),Start,End,ctgry,ctgry.capitalize()) # 
			
			if allDay:
				xml = xml.replace('summary="','allDay="true" summary="All-day ')
			
			postdata = xml.replace('\n','')
			data = {
				'r': postdata
				}
			response = self.opener.open(urllib2.Request(self.urlLink), urllib.urlencode(data))
			if allDay:
				print 'post: createEvent for recurring event'
			else:
				print 'post: createEvent.. for %s'%ctgry
			res = response.read()
			if 'error code' in res:
				print 'error code:	'+ re.findall('''error code="(.*)">.*''',res)[0]
			else:
				print 'createEvent OK!'
		
	def CreateRecurrentingEvent(self,freq='d'):
		now = datetime.datetime.now()
		ymd = now.strftime('%Y%m%d')
		hmsStart = now.replace(hour=now.hour+1).strftime('%H%M%S')
		hmsEnd = now.replace(hour=now.hour+2).strftime('%H%M%S')
		Start = ymd + 'T' + hmsStart
		End = ymd + 'T' + hmsEnd
		
		if freq in 'daily':
			freq = 'Daily event'
			dayList = ''
			dayList = '''"daily"'''
		if freq in 'weekly':
			freq = 'Weekly event'
			dayList = '''"weekly" dayList="MO"'''
		
		xml = '''
			<request>
			<calendar action="createEvent" timezone="-480">
			<event calendarId="http://%s:%s/calendars/%s/" location="" summary="%s repeat for 5 days" busyStatus="BUSY" localStart="%s" localEnd="%s">
			<description/>
			<categories>general</categories>
			<xproperty name="X-EVENT-TYPE" value="General"/>
			<recurrence freq=%s localUntil="" interval="1" count="5"/>
			</event>
			</calendar>
			</request>
		'''%(self.calUrl,str(self.port),self.user,freq,Start,End,dayList)
		postdata = xml.replace('\n','')
		data = {
			'r': postdata
			}
		response = self.opener.open(urllib2.Request(self.urlLink), urllib.urlencode(data))
		print 'post: createEvent..'
		res = response.read()
		if 'error code' in res:
			print 'error code:	'+ re.findall('''error code="(.*)">.*''',res)[0]
		else:
			print 'createEvent OK!'
	
	
# if __name__ == '__main__':
