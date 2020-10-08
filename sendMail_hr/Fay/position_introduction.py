#coding: utf-8
#import codecs
import sys
from email.mime.base import MIMEBase 
import smtplib  
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage 
from email.header import Header 
import os

def send():
	#user info
	mail_host="smtp.owmessaging.com"

	mail_user="fay.wang"

	mail_pass="Welcome876!"

	mail_postfix="owmessaging.com"  

	me = mail_user + "<" + mail_user + "@" + mail_postfix + ">"


	#read file
	filehandle = open(os.path.abspath('.')+'\\position_introduction\\user_info_position_introduction.txt','r')

	list = filehandle.readlines()

	filehandle.close()

	i = 0

	for person in list:

		name = person.split()[0]
			
		#name=name.encode('utf-8')
			
		position = person.split()[1]
			
		#position = position.encode('utf-8')
			
		print name,position
		
		email_to = person.split()[2]
		
		attachment = person.split()[3]
		
		#position = position.encode('utf-8')
		
		#name=name.encode('utf-8')
			
		sub = "美国莱思龙-职位介绍-"+position
						
		content = '''\
			<html> 
			  <head></head> 
			  <body> 
				<p>%s你好<br>
				查收附件为我公司职务说明书，若对此职位有兴趣，请回复邮件安排后续面试事宜.<br>
				<br>
				<br>
				<br>
				<br>
				Denise Kong<br>
				HR Officer<br>
				T:(8610)6269 1018-107<br>
				Email: denise.kong@owmessaging.com<br>
				Website: www.owmessaging.com<br>
				Suite 2609, Block B, Eagle Plaza, No.26 Xiaoyun Road, Chaoyang District,<br>
				Beijing China 100016<br>
				<img src="cid:image1" title="image001"/>
				</p>
			   </body>
			</html>
			'''%name
			
		#message info 
		msgRoot = MIMEMultipart('related')   

		msgText = MIMEText(content,"html",'utf-8')  

		msgRoot['Subject'] = Header(sub,'utf-8')  

		msgRoot['to'] = email_to

		msgRoot['From'] = me 

		msgRoot.attach(msgText)
		
		#construct image
		fp = open('E:\\Python27\\image001.png','rb')

		msgImage = MIMEImage(fp.read())

		fp.close()

		msgImage.add_header('Content-ID','<image1>')

		msgRoot.attach(msgImage)
		
		#attachment
		att = MIMEText(open(os.path.abspath('.')+'\\position_introduction\\'+attachment, 'rb').read(), 'base64', 'utf-8') 
		
		att["Content-Type"] = 'application/octet-stream'
		
		att["Content-Disposition"] = 'attachment; filename=%s' %attachment
		
		msgRoot.attach(att)
		
		try:
			s = smtplib.SMTP()
			
			s.connect(mail_host)
			
			s.login(mail_user,mail_pass)
			
			s.sendmail(me,email_to,msgRoot.as_string())
			
			s.close()
			
		except Exception,e:
		
			print str(e)
			
			print 'send email failed'
			

		d = i + 1
		
		print "send email to the",d,"person,successfully!"
					
		i+=1
		
	
		
		
