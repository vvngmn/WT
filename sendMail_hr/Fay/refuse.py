#coding: utf-8
import sendmail
import os

def send():
	sub = "感谢对我公司关注"
	try:
		filehandle = open(os.path.abspath('.')+'\\refuse\\refuse_mailto_list.txt')
		
		lines = filehandle.readlines()
		
		filehandle.close()
		
	except Exception,e:
	
		print str(e)
					
	content = '''
	<html> 
	  <head></head> 
	  <body> 
		<p>尊敬的候选人:<br> 
		   感谢您对我公司的关注，经过与用人部门的充分沟通，我们暂<br> 
		   时无法提供与您经验匹配的工作机会。但我们会把您的相关资<br>
		   料保存在我们的简历库中作为储备，预祝您未来一切顺利！<br>
		   <br>
		   <br>
		   <br>
		   再次感谢您的关注。预祝您未来一切顺利！<br>
		   <br>
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
		   <br>
		   <br>
		   <br>
		   <img src="cid:image1" title="image001"/>
		</p> 
	  </body> 
	</html> 
	''' 

	i = 1

	for email_to in lines:
		
		if sendmail.sendmail(email_to,sub,content):
		
			print 'send to the',i,"person,succcessfully!"
			
			i+=1
