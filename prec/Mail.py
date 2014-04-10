import urllib2, urllib, httplib
import re,os,sys, time, datetime
import smtplib
from email.MIMEText import MIMEText

class Mail():
	def __init__(self,opener,urlLink,user):		#	
		# # set up email account
		# self.mail_host="smtp.163.com" 				#   smtp.163.com  btdantefe01.cpth.ie smtp.163.com  mail.criticalpath.net  imap.gmail.com
		# self.mail_user="laszlo_v" 						#    qa.user16@test.ie  laszlo_v  testtouchui
		# self.mail_pass="laszlo" 						#     laszlo
		# self.mail_postfix="163.com" 						#   163.com test.ie
		# self.to_list = ["build783.user23@test.ie"] 		#   u13@pk1.dom  Boboom_v@163.com  qa.713.user17@uat.cpcloud.co.uk  testtouchui@gmail.com
		self.opener = opener
		self.urlLink = urlLink
		self.user = user
		
	def sendMail(self, amount=5):
		try:
			for n in range(amount):
				now = datetime.datetime.now().strftime('%Y/%m/%d_%H:%M')
				print 'post: msgsend..No. '+ str(n+1)
				msgsendXML = '''
					<request>
					<mail action="msgsend" accountId="" windowId="1" 
					to="%s" cc="%s" bcc="%s" subject="%s" saveinsent="true" 
					returnReceipt="false" rootMessageUID="" priority="3" from="%s" 
					bodytype="plain"><body>test content
					</body></mail></request>
				'''%(self.user,self.user,self.user,'Precon-mail No.'+str(n+1)+' at '+now,self.user) #  

				postdata = msgsendXML.replace('\n','')
				
				data = {
					'r': postdata
					}
				response = self.opener.open(urllib2.Request(self.urlLink), urllib.urlencode(data))
				res = response.read().replace('><','>\n<')
				if 'error code' in res:
					print 'error code when sendMail: '+ re.findall('''error code="(.*)">.*''',res)[0]
				else:
					print 'msgsend OK!'
			
		except Exception, e:
			print (e)
	
if __name__ == '__main__':
	mail = Mail()
	mail.sendMail(2)
