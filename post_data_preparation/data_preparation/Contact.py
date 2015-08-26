import urllib2, urllib, httplib
import re,os,sys, time, datetime
from xml.etree import ElementTree
import smtplib

class Contact():
	def __init__(self,opener,urlLink,user):		#	
		self.opener = opener
		self.urlLink = urlLink
		self.user = user
		# self.ContactsInfo = os.getcwd()+'\\'+'ContactsInfo.txt' #Hardcode, for windows path
		self.ContactsInfo = './'+'ContactsInfo.txt' #Hardcode, for windows path
			
	def postSaveContacts(self,contactNumber=1,contactInfo=['first']):
		'''
			# TO BE REMOVED
			param:
				contactInfo[] : [firstname, middlename, lastname, email]
		'''
		# print contactInfo
		try:
			postData = {
				'r':'''<request>
					<contacts action="create_contact" addressBookId="PAB://%s/%s/main">
					<contact firstName="%s" lastName="%s">
					<contactfield value="%s" primary="false" type="lzHeader" label="middlename"/>
					<contactfield value="nickname" primary="false" type="lzHeader" label="nickname"/>
					<contactfield value="%s" primary="false" type="lzPhone_mobile" label="home"/>
					<contactfield value="%s" primary="false" type="lzEmail" label="home"/>
					</contact>
					</contacts>
					</request>'''
				%(self.user.split('@')[1],self.user.split('@')[0],contactInfo[0],contactInfo[2],contactInfo[1],contactNumber+'000123456',self.user),
				}
				
			response = self.opener.open(urllib2.Request(self.urlLink), urllib.urlencode(postData))
			res = response.read()
			if 'error code' in res:
				print 'error code in create simple contact:	'+ re.findall('''error code="(.*)">.*''',res)[0]
			else:
				print 'create_contact simple contact OK!'
			
		except Exception,e:
			print (e)	

	def getNextContact(self,addressBookId=['main','trash']):
		'''
			
			'''
		# try:
		contactListStr = ''
		for pab in addressBookId:
			postData = {
				'r':'''<request>
				<contacts action="list" pageSize="300" addressBookId="PAB://%s/%s/%s" offset="0" typeFilter="contact">
				</contacts>
				</request>'''
				%(self.user.split('@')[1],self.user.split('@')[0],pab),
				}
				
			response = self.opener.open(urllib2.Request(self.urlLink), urllib.urlencode(postData))
			contactListStr = contactListStr + response.read().replace('><','>\n<')	# to be finished - save res xml or find the max number for CONTACT
			
		f = open(os.getcwd()+'\\'+'s.xml','w')
		f.write(contactListStr)
		f.close()
		
		p = re.compile(r'/CONTACT_(.*)" first')
		reStrL = re.findall(p,contactListStr)
		print reStrL # reStrL = ['3', '10', '11', '12', '13', '14', '15', '6', '7', '8', '9', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '1', '16', '4', '17', '5']
		
		cn=[]
		for i in reStrL:
			cn.append(int(i))
		return max(cn)+1
		
			
		# except Exception,e:
			# print (e)

	def postImg(self):
		pass

	
	def CreateSimpleContacts(self,contactsN):
		'''
			# TO BE REMOVED
			Create a bunch of contacts with [firstname, middlename, lastname, email]
		'''
		for n in range(contactsN):
			contactInfo = ['simpleFirst','simpleMiddle','simpleLast']
			for i in range(len(contactInfo)):
				contactInfo[i] = contactInfo[i] + str(n+1)
			self.postSaveContacts(str(n+1),contactInfo)
		
	def CreateContactsFullInfo(self,contactsN,addImg=False):
		'''
			Params: num -> how many contacts you want to add for one user
			Varias: realContactInfo1, realContactInfo2
		'''
		birthdayDay = datetime.datetime.now().strftime('%m/%d')
		birthdayHour = datetime.datetime.now().strftime('%H:%M')
		realContactInfo1 = '''
			<contacts action="create_contact" addressBookId="PAB://%s/%s/main"> 
			<contact firstName="first_%s" lastName="last_%s">
		'''	%(self.user.split('@')[1],self.user.split('@')[0],birthdayDay, birthdayHour)  #ENV   PAB://test.ie/%s/main   PAB://uat.cpcloud.co.uk/%s/main
			
		workMail = self.user.replace(self.user.split('user')[1].split('@')[0],str(int(self.user.split('user')[1].split('@')[0])+1))
		otherMail = self.user.replace(self.user.split('user')[1].split('@')[0],str(int(self.user.split('user')[1].split('@')[0])+2))
		birthday = datetime.datetime.now().strftime('%Y%m%d')
		realContactInfo2 = '''
			<contactfield value="%s" primary="false" type="lzEmail" label="home"/>
			<contactfield value="%s" primary="false" type="lzEmail" label="work"/>
			<contactfield value="%s" primary="false" type="lzEmail" label="other"/>
			<contactfield value="Wangfujing" primary="false" type="lzAddress_home" label="street"/>
			<contactfield value="" primary="false" type="lzAddress_home" label="street2"/>
			<contactfield value="" primary="false" type="lzAddress_home" label="street3"/>
			<contactfield value="Beijing" primary="false" type="lzAddress_home" label="city"/>
			<contactfield value="China" primary="false" type="lzAddress_home" label="state"/>
			<contactfield value="10016" primary="false" type="lzAddress_home" label="zip"/>
			<contactfield value="China" primary="false" type="lzAddress_home" label="country"/>
			<contactfield value="%s" primary="false" type="lzPersonal" label="birthday"/>
		'''%(self.user,workMail,otherMail,birthday)
		
		
		dataStr = open(self.ContactsInfo,'r').readlines()
		for i in range(contactsN):
			dataN = []
			for line in dataStr:
				data = line.replace('value="','value="'+str(i+1))
				data = data.replace('Name="','Name="'+str(i+1))
				data = data.replace('\n','')
				dataN.append(data)
			readdata = str(dataN).split('[')[1].split(']')[0].split("'")[1].split("'")[0]
			postdata = '<request>' + realContactInfo1.replace('\n','') + readdata.replace('\n','') + realContactInfo2.replace('\n','') +'''</contact></contacts></request>'''
			# print 'post: create_contact..'
			data = {
				'r': postdata
				}
				
			response = self.opener.open(urllib2.Request(self.urlLink), urllib.urlencode(data))
			if addImg:
				self.postImg()
			
			res = response.read()
			if 'error code' in res:
				print 'error code with full info:	'+ re.findall('''error code="(.*)">.*''',res)[0]
			else:
				print 'create_contact with full info OK!'

	def CreateContactGroup(self,groupN):
		for i in range(groupN):
			postdata = '''
				<request>
				<contacts action="create_group" addressBook="" addressBookId="PAB://%s/%s/main">
				<contactgroup name="My Group %s"/>
				</contacts>
				</request>
				'''%(self.user.split('@')[1],self.user.split('@')[0],str(i+1))
			# print postdata
			data = {
				'r': postdata
				}
			response = self.opener.open(urllib2.Request(self.urlLink), urllib.urlencode(data))
			
			res = response.read()
			if 'error code' in res:
				print 'error code with create group:	'+ re.findall('''error code="(.*)">.*''',res)[0]
			else:
				print 'create_group with create group OK!'


	
if __name__ == '__main__':
	pass
