#coding: utf-8
import sendmail
import refuse
import position_introduction
import interview_invitation
import os

#read interview_invitation file
try:
	filehandle = open(os.path.abspath('.')+'\\interview_invitation\\user_info_interview_invitation.txt','r')
	
	list1 = filehandle.readlines()
	
	filehandle.close()
	
#execute interview_invitation
	if list1[0].find('@'):
	
		interview_invitation.send()
	
#read position_introduction file

	filehandle = open(os.path.abspath('.')+'\\position_introduction\\user_info_position_introduction.txt','r')
	
	list2 = filehandle.readlines()
	
	filehandle.close()
	
	if list2[0].find('@'):
	
		position_introduction.send()
	
#read refuse file

	filehandle = open(os.path.abspath('.')+'\\refuse\\refuse_mailto_list.txt','r')
	
	list3 = filehandle.readlines()
	
	filehandle.close()
	
	if list3[0].find('@'):

		refuse.send()
		
except Exception,e:

	print str(e)
	