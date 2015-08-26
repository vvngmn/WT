import urllib2,urllib,re,os,sys, httplib
import sqlite3, cookielib, time, datetime, os
import Calendar, Mail, Contact, Task, Settings
from urllib import urlencode
from cookielib import CookieJar
global CURRENT_USER 
CURRENT_USER = '' 
timeout = 60
urllib2.socket.setdefaulttimeout(timeout)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(CookieJar())) 

def login(usr):
	password = 'p'
	# if 'dom' in dom:
		# user = '%s.user%s@%s'%(build,usr,dom)
	# if 'uat' in dom:
		# user = 'qa.%s.user%s@%s'%(build,usr,dom)
	# if 'opal' in dom:
		# user = 'mr1.rc6.user%s@%s'%(usr,dom) 
		# password = 'p'
	global CURRENT_USER
	CURRENT_USER = 'u11@test2.com'
	print 'testing..' + user
	
	try:
		data = {
			'r':'<request><user action="login" username="%s" password="%s" rememberme="false"></user></request>'%(user,password)
			}
		response = opener.open(urllib2.Request(urlLink), urllib.urlencode(data))
		res = response.read()
		if 'error code' in res:
			print 'error code:	'+ re.findall('''error code="(.*)">.*''',res)[0]
		else:
			print 'Login OK!'
	except Exception,e:
		print (e)

def testSetting(usersN=[40],gmt=0,aliasAmount=False):
	try:
		for usr in usersN:
			login(usr)
			settings = Settings.Settings(opener,urlLink,CURRENT_USER)
			if gmt+1:
				# print 'gmt'+CURRENT_USER
				settings.setGMT(gmt)
			if aliasAmount:
				# print 'alias'+CURRENT_USER
				settings.createMailAlias(int(aliasAmount))
			
	
	except Exception,e:
		print (e)
		
def testContact(usersN=[1, 6, 11, 16, 21], simpleContacts=10, fullInfoCntcts=2, groups = 10):	
	for usr in usersN:
		login(usr)
		contact = Contact.Contact(opener,urlLink,CURRENT_USER)
		contact.CreateSimpleContacts(contactsN = simpleContacts)
		contact.CreateContactsFullInfo(contactsN = fullInfoCntcts)
		contact.CreateContactGroup(groupN = groups)
		# print contact.getNextContact()

def testCalendar(allDay,usersN=[16]):
	for usr in usersN:
		login(usr)
		calendar = Calendar.Calendar(opener,urlLink,CURRENT_USER)
		# calendar.clearCalendar()
		calendar.CreateSingleEvent(categories=True)
		calendar.CreateSingleEvent(categories=False,allDay=1,nextWeek=True)
		calendar.CreateRecurrentingEvent(freq='d') # freq='d' or freq='w' means for daily/weekly
		calendar.CreateRecurrentingEvent(freq='w') # freq='d' or freq='w' means for daily/weekly
		calendar.CreateCalendar(calendarN=5)
	
def testTask(usersN, dueTime=False, amount=2, clearup=False):
	for usr in usersN:
		login(usr)
		task = Task.Task(opener,urlLink,CURRENT_USER)
		if not clearup:
			task.CreateTask(dueTime, amount)
		# else:
			# if 'id' in task._taskList():
				# print 'find id!!!'
	
def testMail(usersN=[1, 6, 11, 16, 21 ],amount = 20):
	'''
		usersN is also receive user accounts
	'''
	for usr in usersN:
		login(usr)
		mail = Mail.Mail(opener,urlLink,CURRENT_USER)
		mail.sendMail(amount)
	
def config():
	# configFile = os.getcwd()+'\\'+conF+'.txt' #Hardcode, windows path
	# configFile = './'+conF+'.txt' #Hardcode, linux path
	conf = open(configFile,'r')
	params = {}
	for line in conf.readlines():
		param = line.split(':')[0]
		params[param] = line.split(':')[1].split('#')[0]
		# print params
	
	global params,urlLink, build, dom, usersN, simpleContacts, fullInfoCntcts, groups, amount, allDay, feature, setting, taskAmount, aliasAmount
	# global params
	if 'btdante' in params['env']:
		urlLink = 'http://btdantefe01.cpth.ie:%s/cp/dd'%params['port']
		dom = 'qa.dom' #	uat.cpcloud.co.uk	qa.dom
	elif 'staging' in params['env']:
		urlLink = 'http://http.btstaging.cpcloud.co.uk/cp/dd'
		dom = 'uat.cpcloud.co.uk'
	elif 'saphire' in params['env']:	
		urlLink = 'http://saphire.qa.laszlosystems.com:6020/cp/dd'
		dom = 'opal.qa.laszlosystems.com'
	else:
		print 'env value wrong!!!!!!!!!'
		print 'please check your env in config: %s'%params['env']
	build = params['build']
	usersN = params['uid'].split(' ')
	simpleContacts = int(params['simpleContacts'])
	fullInfoCntcts = int(params['fullInfoCntcts'])
	groups = int(params['groups'])
	amount = int(params['amount'])
	allDay = int(params['allDay'])
	feature = params['feature']
	setting = params['setting']
	taskAmount = int(params['taskAmount'])
	aliasAmount = params['aliasAmount']
	
if __name__ == '__main__':
	global configFile
	try: # for run by command line with config file
		configFile = './'+sys.argv[1]+'.txt' 
		config()
		if 'setGmt8' in setting:
			testSetting(usersN,gmt=8)
		if 'contact' in feature:
			testContact(usersN,simpleContacts, fullInfoCntcts, groups)
		if 'calendar' in feature:	
			testCalendar(allDay,usersN)
		if 'mail' in feature:
			testMail(usersN,amount)
		if 'task' in feature:
			testTask(usersN,amount=taskAmount)
		if 'addAlias' in setting:
			testSetting(usersN,gmt=-1,aliasAmount=params['aliasAmount']) # -1 -> not to set gmt(0)
			
		print 'Server run completed!'
	except Exception,e:	# for my local test by direct run
		print e
		global urlLink, build, dom, usersN, simpleContacts, fullInfoCntcts, groups, amount, allDay, feature, setting,aliasAmount
		urlLink = 'http://172.20.1.179:8080/kiwi/dd' #ENV	http://btdantefe01.cpth.ie:8080/cp/dd	http://btdantefe01.cpth.ie:6030/cp/dd   http://http.btstaging.cpcloud.co.uk/cp/dd
		# build = '2754'
		# if 'btdante' in urlLink:
			# dom = 'qa.dom' #	uat.cpcloud.co.uk	qa.dom
		# elif 'btstaging' in urlLink:
			# dom = 'uat.cpcloud.co.uk'
		# elif 'saphire' in urlLink:
			# dom = 'opal.qa.laszlosystems.com'
		# else:
			# print 'Please check local urlLink'
		
		# testSetting(usersN=[11],gmt=8,aliasAmount=1)
		# testMail(usersN=[40],amount=20)
		# testContact(usersN=[40],simpleContacts=1, fullInfoCntcts=10, groups=1)
		testCalendar(usersN=[40],allDay=1)
		# testTask(usersN=[40],dueTime=True, amount=1)
		# testTask(usersN=[41],clearup=True)
		
		print 'Local run completed!'
	