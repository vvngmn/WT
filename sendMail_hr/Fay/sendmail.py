#coding: utf-8  
import smtplib  
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage 
from email.header import Header 

def sendmail(email_to,sub,content):
	
	mail_host="smtp.owmessaging.com"

	mail_user="fay.wang"

	mail_pass="Welcome876!"

	mail_postfix="owmessaging.com"  

	me = mail_user + "<" + mail_user + "@" + mail_postfix + ">"

	  
	  
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

	try:
		s = smtplib.SMTP()
		
		s.connect(mail_host)
		
		s.login(mail_user,mail_pass)
		
		s.sendmail(me,email_to,msgRoot.as_string())
		
		s.close()
		
		return True
	except Exception,e:
	
		print str(e)
		
		return False
			
if __name__ == "__main__":
	email_to = ["test35@opal.qa.laszlosystems.com"]
	sub = 'this is' 
	if sendmail(email_to,sub,content):
		print 'successful!'
	else:
		print 'Fail!'	

		
	
  
  
