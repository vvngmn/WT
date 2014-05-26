#!/usr/bin/python
# encoding: utf-8
import re
import os
import urllib2	
import datetime
import logging
import logging.handlers
import sys
import smtplib
from email.MIMEText import MIMEText

# set up email account
mail_host="imap.gmail.com" #   smtp.163.com  btdantefe01.cpth.ie smtp.163.com
mail_user="vivianw0608" #    qa.user16@test.ie  laszlo_v
mail_pass="Vivian-1234567" #   p  laszlo
mail_postfix="gmail.com" #   163.com test.ie
to_list = ["testtuchui@gmail.com"] #   u13@pk1.dom  Boboom_v@163.com

startTime=datetime.datetime.now()
# set up logger
logger = logging.getLogger("ServiceStatusReport")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s',) 
loggerFolder = os.getcwd()+'\\serverTestLog\\'+startTime.strftime('%Y-%m-%d')+'\\'  # windows path
# loggerFolder = '/log/'+startTime.strftime('%Y-%m-%d')+'/' # linux path
if not os.path.exists(loggerFolder):
	os.makedirs(loggerFolder)

file_name = loggerFolder + startTime.strftime('%H-%M') + ".log"
file_error_name = loggerFolder + startTime.strftime('%H-%M_') + 'Error.log'

file_handler = logging.FileHandler(file_name, mode='w')
file_handler.setFormatter(formatter)  
file_handler.setLevel(logging.DEBUG)
error_file_handler =logging.FileHandler(file_error_name, mode='w')
error_file_handler.setFormatter(formatter)	
error_file_handler.setLevel(logging.ERROR)
stream_handler = logging.StreamHandler(sys.stderr) 
stream_handler.setLevel(logging.ERROR)

logger.addHandler(file_handler)	 
logger.addHandler(error_file_handler) 
logger.addHandler(stream_handler) 

	
def sendMail(mailNumber):
	endTime=datetime.datetime.now()	 #Log end time
	me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
	sub = "TestMail_" + mailNumber + '_' + startTime.strftime('%Y-%m-%d_%H:%M')
	
	try:
		msg = MIMEText('This is a plain text')	 #str(mailContent).decode('utf-8')
		msg['Subject'] = sub
		msg['From'] = me
		msg['To'] = ";".join(to_list)
		s = smtplib.SMTP()
		s.connect(mail_host)
		s.login(mail_user,mail_pass)
	
		s.sendmail(me, to_list, msg.as_string()) #	  msg.as_string()
		s.close()
		
	except Exception, e:
		logger.error("Error in constructing email number %s with %s"%(mailNumber,e))


		
if __name__ == '__main__':
	for i in range(2):
		sendMail(str(i))
		print "Sending No.%s mail to %s"%(str(i),to_list)
	print '\n You can also find error log in:\n' + file_error_name
	