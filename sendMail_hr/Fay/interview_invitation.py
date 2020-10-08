#coding: utf-8
import sendmail
#import codecs
import sys
import os

def send():
	#read files
	try:
		filehandle = open(os.path.abspath('.')+'\\interview_invitation\\user_info_interview_invitation.txt','r')
		
		list = filehandle.readlines()
		
		filehandle.close()
		
	except Exception,e:

		print str(e)
		
	i = 1	
		
	for person in list:
		
		name = person.split()[0]
		
		position = person.split()[1]
		
		print name,position
		
		email_to = person.split()[2]
		
		time = person.split()[3]
		
		#name=name.encode('utf-8')
		
		#position = position.encode('utf-8')
		
		#time = time.encode('utf-8')
		
		sub = "美国莱思龙邀您面试-" +position + '-' +name
		
		content = '''\
		<html> 
			<head></head> 
			<body> 
			<p>%s你好<br>
			职位: %s<br>
			%s<br>
			地址：朝阳区霄云路26号 鹏润大厦B座2609<br>
			建议路线： 10号线亮马桥站C口 出，燕莎桥南乘坐516,707 二站 莱太花卉下车，步行即<br>
			到；405,421,416两站麦子店西街下车，步行即到<br>
			时间确认请回复<br>
			<br>
			<br>
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
		</html>'''%(name,position,time)
		
		if sendmail.sendmail(email_to,sub,content):
		
			print 'send to the',i,'person successfully!'
			
			i+=1
	
	