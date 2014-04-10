#!/usr/bin/python
# encoding: utf-8

import re
import os
import urllib2	
import urllib
import urlparse

from threading import Thread, Lock
from threading import stack_size
from Queue import Queue

import logging
import logging.handlers
import sys

import smtplib
from email.MIMEText import MIMEText

import datetime
import socket

# 纪录开始时间
startTime=datetime.datetime.now()

# 设置超时
timeout = 60
urllib2.socket.setdefaulttimeout(timeout)

# set up email account
mail_host="smtp.oupeng.com"
mail_user="v-xiaochuanw"
mail_pass="VIVIAN1234"
mail_postfix="oupeng.com"
mergeContent=''
to_list = ["v-xiaochuanw@oupeng.com"] #,"congcongk@oupeng.com","yanzih@oupeng.com","fangp@oupeng.com"
# ,'qingqingj@oupeng.com','xuw@oupeng.com','v-jiaruiw@oupeng.com'

# 设置logger
logger = logging.getLogger("ServiceStatusReport")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s',) 
loggerFolder = os.getcwd()+'\\log\\'+startTime.strftime('%Y-%m-%d')+'\\'  # windows path
# loggerFolder = '/nh/appdir/qatest/linkchecker_v2/log/'+startTime.strftime('%Y-%m-%d')+'/' # linux path
if not os.path.exists(loggerFolder):
	os.makedirs(loggerFolder)

def defineLogger(service_name):
    file_name = loggerFolder + service_name + startTime.strftime('_%H-%M') + ".log"
    file_error_name = loggerFolder + service_name + startTime.strftime('_%H-%M_') + 'Error.log'

    # RotatingFileHandler，设置文件大小最大为10M,编码为utf-8，最大文件个数为100个，如果日志文件超过100，则会覆盖最早的日志 
    #file_handler = logging.handlers.RotatingFileHandler(file_name,mode='w', maxBytes=1024*1024*10, backupCount=100, encoding="utf-8") 
    file_handler = logging.FileHandler(file_name, mode='w')
    file_handler.setFormatter(formatter)  
    file_handler.setLevel(logging.DEBUG)

    #error_file_handler = logging.handlers.RotatingFileHandler("Error"+file_name,mode='w', maxBytes=1024*1024*10, backupCount=100, encoding="utf-8") 
    error_file_handler =logging.FileHandler(file_error_name, mode='w')
    error_file_handler.setFormatter(formatter)	
    error_file_handler.setLevel(logging.ERROR)

    stream_handler = logging.StreamHandler(sys.stderr) 
    stream_handler.setLevel(logging.ERROR)

    logger.addHandler(file_handler)	 
    logger.addHandler(error_file_handler) 
    logger.addHandler(stream_handler) 

def sendMailwithLog(service_name, mergeMails=False):
	endTime=datetime.datetime.now()  #Log end time
	me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
	
	file_name = loggerFolder + service_name + startTime.strftime('_%H-%M') + ".log"
	file_error_name = loggerFolder + service_name + startTime.strftime('_%H-%M_') + 'Error.log'
	
	sub = "LinkChecker_" + service_name + '_' + startTime.strftime('%Y-%m-%d_%H:%M')
	content = "Executed time in seconds:" + str((endTime-startTime).total_seconds()) +".\n"
	content += "Socket Timeout Setting: %s.\n \n"%timeout

	# write email content
	warning = '\n Time out errors----------\n'
	try:
		num = 0
		tmot = 0
		f = open(file_error_name,'rU')
		for line in f:
			if 'Error:' in line:
				num+=1
				if "timed out" in line:
					warning += line
					tmot+=1
				else:
					content += line
			else:
				continue
		content += warning
		content += '\n ---------------------------------\nTotal Urls in Error File: ' + str(num) +'(including %s time out).'%tmot
		content += '\n You can also find error log in server:\n' + file_error_name

		if not mergeMails:
			msg = MIMEText(content)	 #
			msg['Subject'] = sub
			msg['From'] = me
			msg['To'] = ";".join(to_list)
			s = smtplib.SMTP()
			s.connect(mail_host)
			s.login(mail_user,mail_pass)
		
			s.sendmail(me, to_list, msg.as_string())
			s.close()
		else:
			mergeContent = '\n\n' + '%s preview: ------------------------------------------------------------------\n\n'%service_name + content
			mergeContent += '\n---------------------------------\n'
			return mergeContent
		
	except Exception, e:
		logger.error("Error in contructing email content: %s",e)

# Multithread to enhance the performance 
class CheckUrlThread():
	def __init__(self,threads):
		#self.opener = urllib2.build_opener(urllib2.HTTPHandler)
		self.lock = Lock() #线程锁
		self.q_req = Queue() #任务队列
		self.q_ans = Queue() #完成队列
		self.threads = threads
		for i in range(threads):
			t = Thread(target=self.threadget)
			t.setDaemon(True)
			t.start()
		self.running = 0
 
	def __del__(self): #解构时需等待两个队列完成
		time.sleep(0.5)
		self.q_req.join()
		self.q_ans.join()
 
	def taskleft(self):
		return self.q_req.qsize()+self.q_ans.qsize()+self.running
 
	def push(self,req,position,platform,readless):
		self.q_req.put((req,position,platform,readless))
 
	def pop(self):
		return self.q_ans.get()
 
	def threadget(self):
		while True:
			url,position,platform,readless = self.q_req.get()
			with self.lock: #要保证该操作的原子性，进入critical area
				self.running += 1
			try:
				ans = PageJob(url,position,platform,readless).check_url() #self.opener.open(req).read()			   
			except Exception, e:
				ans = False
				# to do 
			self.q_ans.put((url,ans,position))
			with self.lock:
				self.running -= 1
			self.q_req.task_done()

# 设置多线程池
pool = CheckUrlThread(threads=20)  # 公司网络用20，其他网络可用100	
#stack_size(32768*16)

# 定义基本页面类
class PageJob(object):
	'''
	Basice HTML Page Handling:
	1. check_url: check accessible	
	2. get_htmlsource: get page html source
	3. debug: print out return code and htmlsource 
	4. check page images
	5. check page titles 
	'''
			 
	HREF_RE = r'<a\s*href="([^"]*?)"'
	IMAGE_RE = r'<img\s.*?src="([^"]*?)"'
	TITLE_RE = r'<title>([^<]*?)</title>'

	def __init__(self,url,uPosition=u"",platform="android",readless=False):
		# class variable 
		self.url = url
		self.uPosition = uPosition
		self.platform = platform
		self.code = 0
		self.htmlsource = "" 
		self.title = ""
		self.readless=readless
	
		try:
			req = urllib2.Request(url)

			# add header to access url
			if platform=="android":
				req.add_header('X-OperaMini-Platform', 'Android')
				req.add_header('User-Agent', 'Opera/9.80 (Android; Opera Mini/6.1.26730/26.1005; U; zh)	 Presto/2.8.119 Version/10.54')
				req.add_header('X-OperaMini-Phone-UA', 'Mozilla/5.0 (Linux; U; Android 2.3.4; zh-cn; TCL A906 Build/FSR) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')		
			elif platform=="s60":	   
				req.add_header('X-OperaMini-Platform', 'Series 60')
				req.add_header('User-Agent', 'Opera/9.80 (Series 60; Opera Mini/6.1.22827/26.1006; U; zh) Presto/2.8.119 Version/10.54')
				req.add_header('X-OperaMini-Phone-UA', 'NokiaC6-01/012.002 (Symbian/3; Series60/5.2 Mozilla/5.0; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/525 (KHTML, like Gecko) Version/3.0 BrowserNG/7.2.7.3')
			elif platform=="j2me":
				req.add_header('X-OperaMini-Platform', 'J2ME/MIDP')
				req.add_header('User-Agent', 'Opera/9.80 (J2ME/MIDP; Opera Mini/6.5.28117/26.1341; U; zh) Presto/2.8.119 Version/10.54')
				req.add_header('X-OperaMini-Phone-UA', 'NokiaC6-01/012.002 (Symbian/3; Series60/5.2 Mozilla/5.0; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/525 (KHTML, like Gecko) Version/3.0 BrowserNG/7.2.7.3')
			else:
				req.add_header('X-OperaMini-Platform', platform[0])
				req.add_header('User-Agent',platform[1])
				req.add_header('X-OperaMini-Phone-UA',platform[2])

			req.add_header('X-OperaMini-Screen-Width', '320')
			req.add_header('X-OperaMini-Screen-Height', '480')
			req.add_header('X-OperaMini-ID', 'testuid')
		
			req.add_header('Accept','text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1')
			req.add_header('Connection','Keep-Alive')
			#req.add_header('Accept-Encoding','gzip,deflate')
			req.add_header('Accept-Language','zh-cn,en;q=0.9')
 
			sock = urllib2.urlopen(req)		
			self.code = sock.code
			if readless:
				self.htmlsource = sock.read(10)	 
			else:
				self.htmlsource = sock.read() 
				
			sock.close()		

		except urllib2.HTTPError,e:
			self.code = e.code
			logger.error(u"Error: (" + unicode(str(e),'utf-8') + u") (" + uPosition + u") " + unicode(url,'utf-8'))									  
		except urllib2.URLError,e:
			logger.error(u"Error: (" + unicode(str(e),'utf-8') + u") (" + uPosition + u") " + unicode(url,'utf-8'))								   
		except Exception,e: 
			logger.error(u"Error: (" + unicode(str(e),'utf-8') + u") (" + uPosition + u") " + unicode(url,'utf-8'))							  
			
	# check url code		
	def check_url(self):
		if self.code ==0 or self.code/100 >= 4:
			return False  
		else:
			return True	 

	# get html source		
	def get_htmlsource(self):
		"""get htmlsource"""
		return self.htmlsource 
		
	# only for search page, when <form> tag needs to be extracted separately	 
	def set_htmlsource(self,partofhtml):
		"""set attribute htmlsource as partofhtml """
		self.htmlsource=partofhtml
	  
	# extract link from htmlSource when it matches Regular Expression reStr; When more is True, reStr includes Group for 2 elements							
	def extract_urls(self,reStr,more=False):
		"""extract url from page source, return absolute path by joining domain with relative path"""
		hrefList=[]
		# apply re to fetch matched regular expression 'str'
		channelstrings = re.findall(reStr, self.htmlsource,re.S|re.I)
		
		for channel in channelstrings:
			if more and (len(channel)==2):		  
				hrefList.append((urlparse.urljoin(self.url, channel[0]),channel[1]))
			else:
				hrefList.append(urlparse.urljoin(self.url, channel))
		return hrefList	 

	# return strings which match reStr, for checking title 
	def extract_strings(self,reStr):
		"""extract strings from page source"""
		strings = re.findall(reStr, self.htmlsource,re.S|re.I)
		return strings	
  
	# extract first match of reStr
	def extract_first_match(self,reStr):
		"""extract first match string"""
		match = re.search(reStr,self.htmlsource,re.S|re.I) 
		if match:
			return match.group(1)
		else:
			return ""	
	
	# check page images are accessible
	def check_imgs(self,utempPosition=u""):
		imgsLink = self.extract_urls(self.IMAGE_RE)	 
		for img in imgsLink:
			pool.push(img,utempPosition + u"->Img access",self.platform,self.readless)			  

	def check_title(self,uTitle):
		match = re.search(self.TITLE_RE,self.get_htmlsource(),re.S|re.I)  
		if match:
			self.title = unicode(match.group(1), 'utf-8')
			if self.title == uTitle:
				logger.debug(u"Success: (Title Matched: " + self.title + u" == " + uTitle + u")(" + self.uPosition + u") " + unicode(self.url,'utf-8'))										
				return True 
			else:
				logger.error(u"Error: (Title Not Matched: " + self.title + u" != " + uTitle + u")(" + self.uPosition + u") " + unicode(self.url,'utf-8'))									 
				return False
		else:
			logger.error(u"Error: (Title Not Found: " + self.title + u" != " + uTitle + u")(" + self.uPosition + u") " + unicode(self.url,'utf-8'))								
			return False
			 
	# print debug info 
	def debug(self):
		# print url return code and html source
		print "=================="
		print "URL access:",self.check_url()
		print "htmlsource", self.get_htmlsource()
		print "uPosition",self.uPosition
		print "url",self.url
		print "================="
	
	# for error message setting position  
	def get_uPosition(self):
		return self.uPosition
		
	def run(self,title):
		self.check_imgs(self.uPosition)
		self.check_title(title)
		
		while pool.taskleft():
			url,ans,position = pool.pop()
			if ans == False:
				pass # already pop error in __init method

			else:
				logger.debug(u"Success: (url check True: " + position + u")( " + unicode(url,'utf-8'))
				
# 定义列表页面类
class ListPageJob(PageJob):

	page = 0
	MAX_PAGE=2	# supposed to be 4
		
	def __init__(self,url,uPosition,platform="android",readless=False):
		super(ListPageJob,self).__init__(url,uPosition,platform,readless)
		self.readless = readless
		
	def extract_list(self,reStr):
		# return list has 1 or 2 elements depending on 'more'
		self.list = self.extract_urls(reStr,more=True)
		#for item in self.list:
		#	 if len(item)!=2:
		#		 logger.debug(u"Info: (List page extracts item: " + unicode(item,'utf-8') + u") " )
		#	 else:
		#		 logger.debug(u"Info: (List page extracts item: " + unicode(item[0],'utf-8') + u") " )				
		return self.list		
		
	def get_listno(self):
		if self.list:
			return len(self.list)
	
	def check_list_item(self):
		for item in self.list:
			if len(item)!=2:
				pool.push(item,self.uPosition + u"->Page " + unicode(str(self.page),'utf-8') +u"->Item access",self.platform,self.readless)
			else:
				pool.push(item[0],self.uPosition + u"->Page " + unicode(str(self.page),'utf-8') + u"->Item access ->"+unicode(item[1],'utf-8'),self.platform,self.readless)
	
	def has_next(self,nextRestr): 
		if nextRestr:
			list = self.extract_urls(nextRestr,more=False)
			try:
				self.nextListPage = list[0]
				#logger.debug(u"Info: (Next Page of list page "+ unicode(str(self.page),'utf-8') +") "+ unicode(self.nextListPage,'utf-8'))			   
				if self.nextListPage:				 
					return True
				else:
					return False
			except Exception,e:
				return False 
		else:			
			return False
	
	def get_next_listpage(self):
		return self.nextListPage		   
	
	def set_max_page(self,num):
		self.MAX_PAGE=num
					
	def run(self,restr,nextRestr="",path=''):
		if self.page!=0:
			self.check_imgs(self.uPosition + u"->Page " + unicode(str(self.page),'utf-8'))
		else:
			self.check_imgs(self.uPosition)
			
		#logger.debug(u"Info: (List Page "+ unicode(str(self.page),'utf-8') +" handle starts: " + self.uPosition + u") " + unicode(self.url,'utf-8'))
		self.extract_list(restr)
		self.check_list_item()
		#logger.debug(u"Info: (List Page "+ unicode(str(self.page),'utf-8') +" handle ends: " + unicode(str(self.get_listno()),'utf-8') + u" items extracted) " + unicode(self.url,'utf-8'))
		
		if self.has_next(nextRestr) and self.page < self.MAX_PAGE-1:
			self.page +=1
			newPage = ListPageJob(path+nextRestr,uPosition=self.uPosition + u"->Page " + unicode(str(self.page),'utf-8'))
			logger.debug(u"~~~~~~~~~~~~next page: "+ path+nextRestr,'utf-8') +" position: " + self.uPosition + u"->Page " + unicode(str(self.page))
			newPage.run(restr,nextRestr)	 
			
		while pool.taskleft():
			url,ans,position = pool.pop()
			if ans == False:

				pass # already pop error in __init method

			else:
				logger.debug(u"Success: (url check True: " + position + u") " + unicode(url,'utf-8'))

# 定义模块分级页面类, 针对有submenu的页面
class MixPageJob(ListPageJob):
	"""Module: Read, Game, Apps Index Page"""
	def __init__(self,url,uPosition,platform="android",readless=False):
		super(MixPageJob,self).__init__(url,uPosition,platform,readless)
		self.menuUrls=[]
		
	def extract_menu(self,restrList):
		for restr in restrList:	   
			try:		  
				self.menuUrls.append(self.extract_urls(restr)[0])
			except Exception,e:
				logger.error(u"Error:Extract menu failed! ("+self.get_uPosition()+u")"+ unicode(self.url,'utf-8'))
		return	self.menuUrls
	
	def has_submenu(self,submenuRestr,isGroup):
		if submenuRestr:
			self.submenus = self.extract_urls(submenuRestr,isGroup) 
			if(len(self.submenus)!=0):
				return True
			else:
				return False
		else:
			return False 
		  
	def extract_sub_menus(self):
		return self.submenus

# 定义搜索页面类
class SearchPagejob(ListPageJob):

	#FORM_RE = r'<form\s*action="([^"]*?)"\s*method="get">(.*?)</form>'
	FORM_RE = r'<form.*?action="([^"]*?)"[^>]*?>(.*?)</form>'
	INPUT_RE = r'<input.*?name="([^"]*?)"\s*value="([^"]*?)"\s*/>'
	SEARCH_RE = r'<a\s*href="(/search/list[^"]*?)"'
	
	def __init__(self,url,uPosition,platform="android",readless=False):
		super(SearchPagejob,self).__init__(url,uPosition,platform,readless)
		self.searchurls = []
		self.defaultsearchurl = ""
	  
	def extract_form(self):
		dict = {}
		searchlist = self.extract_urls(self.FORM_RE,more=True)
		for search in searchlist:
			# hack to change htmlsource to part of form strings 
			self.set_htmlsource(search[1])		  
			
			inputlist = self.extract_strings(self.INPUT_RE)
			
			for input in inputlist:
				dict[input[0]]=input[1]
	  
			self.defaultsearchurl = search[0]+'?'+ urllib.urlencode(dict)  
			
		return self.defaultsearchurl + urllib.urlencode(dict)
	
	def get_searchurls(self):
		searchlist = self.extract_urls(self.SEARCH_RE,False)
		for item in searchlist:
			self.searchurls.append(item)
		
		self.searchurls.append(self.extract_form())		
		return self.searchurls
	
				
	def run(self,more=True):
		# check form extracted url first as the default one will change htmlsource 
		if more:			
			searchlist = self.extract_urls(self.SEARCH_RE,False)

			for item in searchlist:
				pool.push(item,self.uPosition,self.platform,self.readless)
		
		pool.push(self.extract_form(),self.uPosition+u"->Default Search",self.platform,self.readless)
					
		while pool.taskleft():
			url,ans,position = pool.pop()
			if ans == False:

				pass # already pop error in __init method

			else:
				logger.debug(u"Success: (url check True: " + position + u") " + unicode(url,'utf-8'))
				#print u"Success: (search url check True: " + position + u")( " + unicode(url,'utf-8')
					
# Ezine Module 
class EzineListPageJob(ListPageJob):

	def __init__(self,url,uPosition,platform="android",readless=False):
		super(EzineListPageJob,self).__init__(url,uPosition,platform,readless)
		self.list = []
			
	# add '&trace=autotest'
	def extract_list(self,reStr):
		templist = super(ListPageJob,self).extract_urls(reStr,more=True)
		for item in templist:
			if len(item)!=2:
				if item.find("&trace=")!=-1:
					autotestLink = item[:item.index("&trace=")] + '&trace=autotest'
					item= autotestLink						  
				#logger.debug(u"Info: (List page extracts item: " + unicode(item,'utf-8') + u") " )				  
			else:
				if item[0].find("&trace=")!=-1:
					autotestLink = item[0][:item[0].index("&trace=")] + '&trace=autotest'
					item= (autotestLink,item[1])
				#logger.debug(u"Info: (List page extracts item: " + unicode(item[0],'utf-8') + u") " )	  
			self.list.append(item)			
		return self.list		

	# check latest post time   
	def check_latest_post(self,reStr):
		str = self.extract_first_match(reStr)
		if str.find("分钟前") != -1:
			if int(str[:str.index("分钟前")]) > 59:
				logger.error(u"Error: (Check latest post: " + unicode(str,'utf-8') + u">59分钟前)(" + self.uPosition +u") "+unicode(self.url,'utf-8'))
			else:
				logger.debug(u"Success: (Check latest post: " + unicode(str,'utf-8') + u"<59分钟前)(" + self.uPosition +u") "+unicode(self.url,'utf-8'))
		elif str.find("小时前") != -1:
			if int(str[:str.index("小时前")]) > 3:
				logger.error(u"Error: (Check latest post: " + unicode(str,'utf-8') + u">3小时前)(" + self.uPosition +u") "+unicode(self.url,'utf-8'))
			else:
				logger.debug(u"Success: (Check latest post: " + unicode(str,'utf-8') + u"<3小时前)(" + self.uPosition +u") "+unicode(self.url,'utf-8'))
		else:
			if str=="":
				pass
			else:
				logger.error(u"Error: (Check latest post: " + unicode(str,'utf-8') + u" is unexpected)(" + self.uPosition +u") "+unicode(self.url,'utf-8'))
	
	# run list check
	def run(self,listRestr,nextRestr,lastestRestr):
		
		# check list page images 
		if self.page!=0:  
			self.check_imgs(self.uPosition + u"->Page " + unicode(str(self.page),'utf-8'))
		else:
			self.check_imgs(self.uPosition)
		
		# check list items 
		#logger.debug(u"Info: (List Page "+ unicode(str(self.page),'utf-8') +" handle starts: " + self.uPosition + u") " + unicode(self.url,'utf-8'))
		self.extract_list(listRestr)
		self.check_list_item()
		#logger.debug(u"Info: (List Page "+ unicode(str(self.page),'utf-8') +" handle ends: " + unicode(str(self.get_listno()),'utf-8') + u" items extracted) " + unicode(self.url,'utf-8'))
		
		# check latest post
		if self.page ==0:
			self.check_latest_post(lastestRestr)
		
		# check next page
		if self.has_next(nextRestr) and self.page < self.MAX_PAGE-1:
			self.page +=1
			self.run(listRestr,nextRestr,lastestRestr)		 
		 
		# thread run   
		while pool.taskleft():
			url,ans,position = pool.pop()
			if ans == False:

				pass # already pop error in __init method

			else:
				logger.debug(u"Success: (url check True: " + position + u") " + unicode(url,'utf-8'))
						 
class EzineJob():
	"""Summary of class here.
	1.从ezine首页自动抓取频道list
	2.遍历每个频道以及下一页直到结束 or 最多遍历5页
	3.从每个频道列表页返回首页
	4.抓取每个频道列表页所有图片
	5.每个频道第一条消息的更新时间,通过的条件为xx分钟前(x小于等于59)或者x小时前(x小于等于3)
	6.[TODO]详情页微博评论，转发，收藏接口
	7.autotest参数跟挺松沟通过之后可以继续使用，不影响运营统计 for advItem, trace=autotest is added at the end of url
	"""
	DOMAIN = 'http://ezine.oupeng.com/'
   
	CHANNEL_URL_RE = r'<a.*?href="(.*?)&trace=index"' 
	CHANNEL_NAME_RE = r'<div\s*class="channel-name">([^<]*?)</div>'
	
	ITEM_HREF_RE = r'<a\s*href="(.*?)"\s*class="(.*?)".*?>'
	NEXT_HREF_RE = r'<a\s*href="([^"]*?)"\s*class="next"[^>]*?>' 
	LATESTNEWS_RE =r'<span\s*class="time">(.*?)</span>'
	   
	channelDict = {}
	
	def __init__(self):
		try:
			# Ezine index page is a ListPageJob	 
			self.ezine = ListPageJob("http://ezine.oupeng.com/",u"EZINE")	
		except Exception,e:
			logger.error(u"Error in initiating EzineJob ("+unicode(str(e),'utf-8')+u")")   
		
		
	def extract_channel(self):
		channelUrls = self.ezine.extract_list(self.CHANNEL_URL_RE)
		channelNames = self.ezine.extract_strings(self.CHANNEL_NAME_RE)
	   
		if len(channelUrls) == len(channelNames) and len(channelUrls)!=0:
			for i in range(len(channelNames)):	  
				self.channelDict[channelNames[i]] = channelUrls[i]+"&trace=autotest"
			logger.debug("Success: 从ezine首页自动抓取频道list")	  
			return True			
		else:
			logger.error("Error: 从ezine首页自动抓取频道list (频道链接数目和名称数目不匹配)") 
			return False  
		
	def run(self):
		try:
			if self.extract_channel():
				for k,v in self.channelDict.items():
					EzineListPageJob(v,u"Ezine->"+unicode(k,'utf-8')).run(self.ITEM_HREF_RE,self.NEXT_HREF_RE,self.LATESTNEWS_RE)
			else:
				pass
		except Exception,e:
			logger.error(u"Error in EZINE module run ("+unicode(str(e),'utf-8')+u")")				
						
# Read Module 
class ReadJob(object):
	"""
	1.首页20本书可以点进相应cp网站，20本书的书名需要判断显示与否
	2.广告链接检查-运营提供list,CCK负责更新 [TODO - not fetching all adv items]
	3.分类/排行/书单页需要判断页面是否有相应内容 [TODO - 只检查200，没有检查是否有相关内容？]
	4.书单链接提供，见附件shudan 12.17.txt
	5.分类页面点击全部页面，可以只点击前5页。
	6.提供分类页链接，见附件分类12.17.txt
	7.[TODO]搜索页面的默认搜索词和内置搜索词都需要点击一遍
	8.链接的参数可以通过修改header的方式，不影响后台统计
	9.图书title需要打印 
	10.图片资源的检查，链接中带有detail说明已经进入详情页，可以停止点击
	11.提供Android和Symbian和java平台的UA如下：
	Android:
	Mozilla/5.0/test (Linux; U; Android 2.3.4; zh-cn; TCL A906 Build/FSR)
	AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1
	Symbian:
	Mozilla/5.0/test (SymbianOS/9.3 U Series60/3.2 N6730c-1/021.002
	Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/525 (KHTML,like Gecko) Version/3.0 Safari/525
	Java:
	Opera/9.80/test(J2ME/MIDP;Opera Mini/6.5.28117/26.1488;U;zh)Presto/2.8.119 Version/10.54
	"""
	DOMAIN = 'http://read.oupeng.com/'
	androidplatform = ['AndroidTesting','Mozilla/5.0/test (Linux; U; Android 2.3.4; zh-cn; TCL A906 Build/FSR)',
				'AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1']
	symbianplatform = ['SysbianTesting',
				'Mozilla/5.0/test (SymbianOS/9.3 U Series60/3.2 N6730c-1/021.002 Profile/MIDP-2.1 Configuration/CLDC-1.1 )',
				'AppleWebKit/525 (KHTML,like Gecko) Version/3.0 Safari/525']
	javaplatform = ['JavaTesting','Opera/9.80/test(J2ME/MIDP;Opera Mini/6.5.28117/26.1488;U;zh)','Presto/2.8.119 Version/10.54']  
	
	READLINK_RE = r'<a\s*href="(/resource/download.*?)".*?>\s*阅读\s*</a>'
	READMORE_RE = r'<a\s*href="(/more/chapter.*?)".*?>\s*继续.*?</a>'
	BOOK_TITLE_RE = r'<a\s*href="(/home/detail.*?)".*?>\s*(.*?)\s*</a>' 
	# ADV_RE = r'<a\s*href="(/more/advertise.*?)".*?>'
	
	RANK_RE = r'<a\s*href="(/rank/index.*?)".*?>\s*排行\s*</a>' 
	FENLEI_RE = r'<a\s*href="(/fenlei/navi.*?)".*?>\s*分类\s*</a>'
	SHUDAN_RE = r'<a\s*href="(/shudan/navi.*?)".*?>\s*书单\s*</a>'
	
	HREF_RE = r'<a\s*href="(.*?)"'
	
	SHUDAN_SUB_RE = r'<a\s*href="(/shudan/.*?)".*?>' 
	FENLEI_SUB_RE = r'<a\s*href="(/fenlei/[^"]*?)"\s*class="dis_table">\s*<div>\s*<em\s*class="f_green">([^<]*?)</em>'																						
	FENLEI_NEXT_RE = r'<a\s*href="([^"]*?)"[^>]*?>\s*下一页\s*</a>'
	#SUB_FENLEI_MENU_RE = r'<a\s*href="(/fenlei/[^"]*?)"[^>]*?>([^<]*?)</a>'
	SUB_FENLEI_MENU_RE = r'<a\s*href="(/fenlei/[^"]*?)"[^>]*?>(最热榜|人气榜|最新榜)</a>'
	 
	TITLE = u'看小说'

	def __init__(self):
		try:
			self.read = MixPageJob(self.DOMAIN,u"READ",self.androidplatform)   
		except Exception,e:
			logger.error(u"Error in initiating ReadJob ("+unicode(str(e),'utf-8')+u")")	  
	
	def indexrun(self):
		# 首页 20本书 下载页面
		self.read.extract_list(self.READLINK_RE)
		self.read.check_list_item()
		#logger.debug(u"Info: Handle number: " + unicode(str(self.read.get_listno()),'utf-8'))
		
		self.read.extract_list(self.READMORE_RE)
		self.read.check_list_item()
		#logger.debug(u"Info: Handle number: " + unicode(str(self.read.get_listno()),'utf-8'))
		
		# 首页 20本书 详细页面, 书名
		titles = self.read.extract_list(self.BOOK_TITLE_RE) 
		self.read.check_list_item()
		num = len(titles)		
		for title in titles:
			if len(title[1]) < 40 and len(title[1])>0:	# to be fixed  
				logger.debug(u"Info: 书名 " + unicode(title[1],'utf-8'))
			else:
				# book description, not title
				num -= 1
		if num!=20:
			logger.error(u"Error: (READ 首页书名总数!＝20) " + unicode(self.DOMAIN,'utf-8'))
		else:
			logger.debug(u"Success: (READ 首页书名总数＝20) " + unicode(self.DOMAIN,'utf-8'))
		
	def run(self):
	
		try:				
			# 首页<TITLE> 
			self.read.check_title(self.TITLE)
		
			# 首页20本书链接及书名验证
			self.indexrun()
			
			# 首页搜索
			SearchPagejob(self.DOMAIN,u"READ->搜索",platform="android").run(False)
			   
			# 排行/分类/书单页
			restrList = [self.RANK_RE,self.FENLEI_RE,self.SHUDAN_RE]
			self.menus = self.read.extract_menu(restrList)
		
			# 排行,书单页面处理
			rank = ListPageJob(self.menus[0],u"READ->排行")
			rank.run(self.HREF_RE)
			rank.check_title(self.TITLE)
		
			shudan = ListPageJob(self.menus[2],u"READ->书单")
			shudan.run(self.HREF_RE)
			shudan.check_title(self.TITLE)
		
			# 分类页面 list -> submenu 
			fenlei = ListPageJob(self.menus[1],u"READ->分类")
		
			subfenlei = fenlei.extract_list(self.FENLEI_SUB_RE)
			for sub in subfenlei:
				# 最热榜 人气榜 最新榜
				temp = MixPageJob(sub[0],u"READ->分类->"+unicode(sub[1],'utf-8'))  #sub[0]:url, sub[1]:CN channel name by re
				if temp.has_submenu(self.SUB_FENLEI_MENU_RE,True):
					templist = temp.extract_sub_menus()
					for t in templist: # t means xx榜
						# to fix
						try:
							path = DOMAIN + 'fenlei'+t[0].split('/fenlei')[1]  # remove extra / (end with DOMAIN start with fenlei)
							tListPage = ListPageJob(path+self.FENLEI_NEXT_RE,u"READ->分类->"+unicode(sub[1],'utf-8')+ u"->" +unicode(t[1],'utf-8'))
							
							logger.debug('~~~~~~~~~~~~ page No:%s  '%(path+self.FENLEI_NEXT_RE))
							tListPage.run(self.HREF_RE, self.FENLEI_NEXT_RE, path)
						except Exception,e:
							pass
						
			# thread run to check url
			#while pool.taskleft():
			#	 url,ans,position = pool.pop()
			#	 if ans == False:

			#		 pass # already pop error in __init method

			#	 else:
			#		 logger.debug(u"Success: (url check True: " + position + u") " + unicode(url,'utf-8'))
		
		except Exception,e:
			logger.error(u"Error in READ module run ("+unicode(str(e),'utf-8')+u")")
		   
# App Module	 
class AppJob(object):
	"""
	[TODO]点击首页全部软件的下载按钮和打开详情页
	[DONE]软件下的各个分类链接提供,见附件app fenlei 12.17.txt
	[TODO]软件下的各个分类是否内容为空，需要看前3页
	[DONE]游戏下的各个分类链接提供，见附件app youxi 12.18.txt
	[DONE]取title的链接，首页，软件，游戏, 搜索页面，见附件title 12.18.txt
	[TODO]图片资源的检查，进入详情页后图片为非链接形式，不能点击
	[DONE]跟云龙确认，链接的参数不必特别加入，只需要在header信息上加入 - same as READ
	"""				   
	androidplatform = ['AndroidTesting','Mozilla/5.0 (Linux; U; Android 2.3.4; zh-cn; TCL A906 Build/FSR) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
				'Opera/9.80 (Android; Opera Mini/6.1.26730/26.1005; U; zh']
				
	DOMAIN = "http://apps.oupeng.com/"
	
	HREF_RE = r'<a\s*href="([^"]*?)"'
	NEXT_RE = r'<a\s*class="more"\s*href="([^"]*?)">\s*点击加载更多\s*</a>' 
	
	RANK_RE = r'<a\s*href="(/rank/index.*?)".*?>\s*榜单\s*</a>'
	FENLEI_RE = r'<a\s*href="(/fenlei/navi.*?)".*?>\s*分类\s*</a>'
	SEARCH_RE = r'<a\s*href="(/search/index.*?)".*?>\s*搜索\s*</a>'
	   
	DOWNLOAD_RE = r'<a\s*href="(/resource/download.*?)".*?class="btn-down">'   
	DETAILLINK_RE = r'<a\s*href="(/home/detail.*?)".*?class="app-msg">'
	APP_TITLE_RE = r'<a\s*href="(/fenlei/[^"]*?)".*?class="app-msg">.*?<p\s*class="app-name">([^<]*?)</p>'	
	
	RANK_MENU_RE = r'<a\s*href="(/rank/index[^"]*?)"[^>]*?>.*?(热门游戏|热门应用).*?</a>'  
	
	FENLEI_MENU_RE = r'<a\s*href="(/fenlei/[^"]*?)"[^>]*?>.*?(软件|游戏).*?</a>'   
	FENLEI_SUB_RE = r'<a\s*href="(/fenlei/[^"]*?)".*?<span class="app-name">\s*([^<]*?)</span>\s*</a>'																							
	SUB_FENLEI_MENU_RE = r'<a\s*href="(/fenlei/[^"]*?)"[^>]*?>.*?<span>(热门|上升最快|新品)</span>.*?</a>'
	
	TITLE = u'应用商店'
	
	def __init__(self):
		try:
			self.apps = MixPageJob(self.DOMAIN,u"APPS",self.androidplatform)   
		except Exception,e:
			logger.error(u"Error in initiating AppJob ("+unicode(str(e),'utf-8')+u")")	 

	def check_download_link(self,url,uPosition=u""):
		try:
			req = urllib2.Request(url)
					   
			req.add_header('X-OperaMini-Platform', self.androidplatform[0])
			req.add_header('User-Agent',self.androidplatform[1])

			req.add_header('X-OperaMini-Phone-UA',self.androidplatform[2])

			req.add_header('X-OperaMini-Screen-Width', '320')
			req.add_header('X-OperaMini-Screen-Height', '480')
			req.add_header('X-OperaMini-ID', 'testuid')
		
			req.add_header('Accept','text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1')
			req.add_header('Connection','Keep-Alive')
			#req.add_header('Accept-Encoding','gzip,deflate')
			req.add_header('Accept-Language','zh-cn,en;q=0.9')
 
			sock = urllib2.urlopen(req) 
			code = sock.code
			self.htmlsource = sock.read(10) 
			sock.close()		

		except urllib2.HTTPError,e:
			self.code = e.code
			logger.error(u"Error: (" + unicode(str(e),'utf-8') + u") (" + uPosition + u") " + unicode(url,'utf-8'))										
		except urllib2.URLError,e:
			logger.error(u"Error: (" + unicode(str(e),'utf-8') + u") (" + uPosition + u") " + unicode(url,'utf-8'))								   
		except Exception,e: 
			logger.error(u"Error: (" + unicode(str(e),'utf-8') + u") (" + uPosition + u") " + unicode(url,'utf-8'))		
	
	def run(self):
	
		try:		   
			# 首页<TITLE> 
			self.apps.check_title(self.TITLE)
			self.apps.set_max_page(3)
			# 点击首页全部软件的下载按钮和打开详情页
			self.apps.run(self.HREF_RE,self.NEXT_RE) 
		   
			# 榜单/分类/搜索页
			restrList = [self.RANK_RE,self.FENLEI_RE,self.SEARCH_RE]
			self.menus = self.apps.extract_menu(restrList)
		
			# 榜单页面处理: 热门应用 | 热门游戏 
			rank = MixPageJob(self.menus[0],u"APPS->榜单")
			if rank.has_submenu(self.RANK_MENU_RE,True):
				templist = rank.extract_sub_menus() 
				for t in templist:
					try:
						#ListPageJob(t[0],u"APPS->榜单->"+unicode(t[1],'utf-8')).run(self.HREF_RE) 
						ListPageJob(t[0],u"APPS->榜单->"+unicode(t[1],'utf-8')).run(self.DETAILLINK_RE)
					except Exception,e:
						pass   
			#rank.run(self.HREF_RE)	 
			rank.run(self.DETAILLINK_RE) 
			#rank.run(self.DOWNLOAD_RE) 
			 
			rank.check_title(self.TITLE)
		
			# 分类页面 list -> submenu -> sub category -> sub menu
			fenlei = MixPageJob(self.menus[1],u"APPS->分类")
			if fenlei.has_submenu(self.FENLEI_MENU_RE,True):
				templist = fenlei.extract_sub_menus() 
				# 软件和游戏
				for t in templist:
					try:
						subfenleilist = ListPageJob(t[0], fenlei.get_uPosition()+ unicode(t[1],'utf-8')).extract_list(self.FENLEI_SUB_RE)
						for sub in subfenleilist:	  
							subtemp = MixPageJob(sub[0],u"APPS->分类->" + unicode(t[1],'utf-8') + u"->" + unicode(sub[1],'utf-8'))
							if subtemp.has_submenu(self.SUB_FENLEI_MENU_RE,True):
								subtemplist = subtemp.extract_sub_menus()
								for subt in subtemplist:
									try:												
										#ListPageJob(subt[0],subtemp.get_uPosition() + u"->" + unicode(subt[1],'utf-8')).run(self.HREF_RE)
										ListPageJob(subt[0],subtemp.get_uPosition() + u"->" + unicode(subt[1],'utf-8')).run(self.DETAILLINK_RE)
										#ListPageJob(subt[0],subtemp.get_uPosition() + u"->" + unicode(subt[1],'utf-8'),readless=True).run(self.DOWNLOAD_RE)
									except Exception,e:
										logger.error(u"Error:("+unicode(str(e),'utf-8')+u")("+subtemp.get_uPosition() + u"->" + unicode(subt[1],'utf-8')+u") "+unicode(subt[0],'utf-8'))
					except Exception,e:
						pass   
		   
			# 搜索页面 SearchPagejob 
			SearchPagejob(self.menus[2],u"APPS->搜索").run()
				   
			# thread run to check url
			#while pool.taskleft():
			#	 url,ans,position = pool.pop()
			#	 if ans == False:

			#		pass # already pop error in __init method

			#	 else:
			#		 logger.debug(u"Success: (url check True: " + position + u") " + unicode(url,'utf-8'))
		
		except Exception,e:
			logger.error(u"Error in APP module run ("+unicode(str(e),'utf-8')+u")")

# Nav Module	  
class NavJob(object):
	""" 按各手机平台自动获取导航页面内的所有链接，然后检查200可用性。 """
	DOMAIN = 'http://nav.oupeng.com/'	
	HREF_RE = r'<a\s*href="([^"]*?)"[^>]*?>(.*?)</a>' 

	def __init__(self):
		try:
			self.nav = ListPageJob(self.DOMAIN,u"Nav",platform="android") 
		except Exception,e:
			logger.error(u"Error in initiating NavJob ("+unicode(str(e),'utf-8')+u")")	 
		   
	def run(self):
		try:			
			self.nav.run(self.HREF_RE)		  
		except Exception,e:
			logger.error(u"Error in NAV module run ("+unicode(str(e),'utf-8')+u")")

# Game Module			
class GameJob(object):
	"""
	[TODO]点击下一页直到最后一页
	[DONE]分别提供页数为2页和5页的UA
	显示2页游戏的UA:
	http://game.oupeng.com/product/list.do?&_pf=Android_2.3.5
	显示5页游戏的UA:
	http://game.oupeng.com/product/list.do?&_pf=Android_4.1
	[DONE]所有图片资源链接的提供，由cck更新
	[DONE]检查title的链接，由cck更新
	"""
	DOMAIN = 'http://games.oupeng.com/' 
	
	androidplatform = ['AndroidTesting','Mozilla/5.0 (Linux; U; Android 2.3.4; zh-cn; TCL A906 Build/FSR) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
				'Opera/9.80 (Android; Opera Mini/6.1.26730/26.1005; U; zh']
	
	HREF_RE = r'<a\s*href="([^"]*?)"'
	NEXT_RE = r'<a\s*class="more[^"]*?"\s*href="([^"]*?)">\s*点击加载更多\s*</a>' 
	
	FENLEI_RE = r'<a\s*href="(/fenlei/navi.*?)".*?>\s*单机\s*</a>'
	WANGYOU_RE =  r'<a\s*href="(/wangyou/index.*?)".*?>\s*网游\s*</a>'	
	SEARCH_RE = r'<a\s*href="(/search/index.*?)".*?>\s*搜索\s*</a>'
		 
	WANGYOU_MENU_RE = r'<a\s*href="(/wangyou/index[^"]*?)"[^>]*?>.*?(热门|上升最快|新品).*?</a>'  
	FENLEI_SUB_RE = r'<a\s*href="(/fenlei/[^"]*?)".*?<p>\s*([^<]*?)\s*</p>'		 
	   
	TITLE = u'游戏中心'
	
	def __init__(self):
		try:
			self.games = MixPageJob(self.DOMAIN,u"GAMES",self.androidplatform)
		except Exception,e:
			logger.error(u"Error in initiating GameJob ("+unicode(str(e),'utf-8')+u")")	  

	def run(self):
		try:	 
			# 首页<TITLE> 
			self.games.check_title(self.TITLE)
		
			# 点击首页全部游戏的下载按钮和打开详情页
			self.games.run(self.HREF_RE,self.NEXT_RE) 
		   
			# 单机/网游/搜索页
			restrList = [self.FENLEI_RE,self.WANGYOU_RE,self.SEARCH_RE]
			self.menus = self.games.extract_menu(restrList)
		
			# 搜索页面 SearchPagejob 
			SearchPagejob(self.menus[2],u"GAMES->搜索").run()

			# 网游页面处理: (热门|上升最快|新品)
			wangyou = MixPageJob(self.menus[1],u"GAMES->网游")
			if wangyou.has_submenu(self.WANGYOU_MENU_RE,True):
				templist = wangyou.extract_sub_menus() 
				for t in templist:
					try:
						ListPageJob(t[0],wangyou.get_uPosition()+u"->"+unicode(t[1],'utf-8')).run(self.HREF_RE) 
					except Exception,e:
						pass   
			wangyou.check_title(self.TITLE)
		
			# 单机页面 -> sub category 
			fenlei = ListPageJob(self.menus[0],u"GAMES->单机")
			templist = fenlei.extract_list(self.FENLEI_SUB_RE)
			for t in templist:
				try:
					ListPageJob(t[0],fenlei.get_uPosition() + u"->" + unicode(t[1],'utf-8')).run(self.HREF_RE)
				except Exception,e:
					logger.error(u"Error:("+unicode(str(e),'utf-8')+u")("+subtemp.get_uPosition() + u"->" + unicode(subt[1],'utf-8')+u") "+unicode(subt[0],'utf-8'))
			
			# thread run to check url
			#while pool.taskleft():
			#	 url,ans,position = pool.pop()
			#	 if ans == False:

			#		pass # already pop error in __init method

			#	 else:
			#		 logger.debug(u"Success: (url check True: " + position + u") " + unicode(url,'utf-8'))
			
		except Exception,e:
			logger.error(u"Error in GAME module run ("+unicode(str(e),'utf-8')+u")")
					  
# Shop Module 
class ShopJob(object):
	"""
	首页的链接都可以点击 - Done
	广告链接提供有cck更新 - Needs to check
	[TODO]搜索页面的搜过结果是否可以显示 
	首页中有特定组件点击后进入二级页面，需要检查页面的正确性，以及点击”查看更多“按钮	  ？什么组件 - Needs to check
	跟云龙确认，链接的参数不必特别加入，只需要在header信息上加入
	"""
	DOMAIN = 'http://shop.oupeng.com/'
	
	HREF_RE = r'<a\s*href="([^"]*?)"'
	
	def __init__(self):
		try:
			self.shop = ListPageJob(self.DOMAIN,u"SHOP",platform="android")
		except Exception,e:
			logger.error(u"Error in initiating ShopJob ("+unicode(str(e),'utf-8')+u")")	  
	
	def run(self):
		try:		  
			self.shop.run(self.HREF_RE)
			SearchPagejob(self.DOMAIN,u"SHOP->搜索",platform="android").run(False)
			
		except Exception,e:
			logger.error(u"Error in SHOP module run ("+unicode(str(e),'utf-8')+u")")

# Sdf Module 
class SdfJob(object):
	""" 按各手机平台自动获取SDF页面内的所有链接，然后检查200可用性。 """
	DOMAIN = 'http://sdf.oupeng.com'
	HREF_RE = r'<a\s*href="bream:speeddialfarm.*?url=([^"]*?)"' 
	
	def __init__(self):
		try:
			self.sdf = ListPageJob(self.DOMAIN,u"Sdf",platform="android")
		except Exception,e:
			logger.error(u"Error in initiating SdfJob ("+unicode(str(e),'utf-8')+u")")	 
	
	def run(self):
		try:		  
			#f=file(sdfSource)
			#for line in f.readlines():
			#	url = "href="+'"'+line.split('\n')[0]+'"'
			#	print (" Checking:	  "+url)
			#	self.sdf.run(url)
			#self.sdf.debug()
			
		    urls = self.sdf.extract_strings(self.HREF_RE)
		    for url in urls:
		        url2= urllib.unquote(url)
		        # not push pool for url like "nh-redir://"
		        if url2.startswith("http"):  
		            pool.push(url2,self.sdf.uPosition  + u"->Item access",self.sdf.platform,self.sdf.readless)
		    
		    while pool.taskleft():
			    url,ans,position = pool.pop()
			    if ans == False:
				    pass # already pop error in __init method
			    else:
				    logger.debug(u"Success: (url check True: " + position + u") " + unicode(url,'utf-8'))
				    
			    #self.sdf.run(self.HREF_RE)
			
		except Exception,e:
			logger.error(u"Error in SdfJob module run ("+unicode(str(e),'utf-8')+u")") 
			
# MAIN FUNCTION
if __name__ == '__main__':

    
	# # Ran 1 test in 192.652s
	# defineLogger("EZINE")
	# ezine = EzineJob()
	# ezine.run()
	# sendMailwithLog("EZINE")
	
	# # Ran 1 test in 755.291s
	defineLogger("READ")
	read = ReadJob()
	read.run()
	# sendMailwithLog("READ")
	
	# Ran 1 test in 31.466s
	# defineLogger("NAV")
	# nav = NavJob()
	# nav.run()
	# sendMailwithLog("NAV")
		
	# # Ran 1 test in 5487.764s
	# defineLogger("APP")
	# app = AppJob()
	# app.run()
	# sendMailwithLog("APP")
		
	# # Ran 1 test in 1564.022s
	# defineLogger("GAME")
	# game = GameJob()
	# game.run()  
	# sendMailwithLog("GAME")
	
	# Ran 1 test in 14.403s
	# defineLogger("SHOP")
	# shop = ShopJob()
	# shop.run()	
	# sendMailwithLog("SHOP")
	
	# sdf = SdfJob()
	# defineLogger("SDF")
	# sdf.run() 
	# sendMailwithLog("SDF")

	#-------------------
	# Ezine: 7135
	#Read : 28271
	# Nav  : 233
	# App  : 10065
	# Game : 5018
	# Shop : 82
	# Total: 50804