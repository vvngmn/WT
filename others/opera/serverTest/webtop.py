import os
import urllib2
import socket
import logging
import logging.handlers
logger = logging.getLogger("ServiceStatusReport")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s',) 
loggerFolder = 'log\\'
if not os.path.exists(loggerFolder):
    os.mkdir(loggerFolder)

timeout = 10
urllib2.socket.setdefaulttimeout(timeout)

def defineLogger(service_name):
	# file_name = startTime.strftime('%Y-%m-%d') +'_' + service_name + ".log"
	file_name = loggerFolder + startTime.strftime('%Y-%m-%d') + '_' + service_name + ".log"

	file_handler = logging.FileHandler(file_name, mode='w')
	file_handler.setFormatter(formatter)  
	file_handler.setLevel(logging.DEBUG)

	#error_file_handler = logging.handlers.RotatingFileHandler("Error"+file_name,mode='w', maxBytes=1024*1024*10, backupCount=100, encoding="utf-8") 
	error_file_handler =logging.FileHandler("Error"+file_name, mode='w')
	error_file_handler.setFormatter(formatter)	
	error_file_handler.setLevel(logging.ERROR)

	stream_handler = logging.StreamHandler(sys.stderr) 
	stream_handler.setLevel(logging.ERROR)

	logger.addHandler(file_handler)	 
	logger.addHandler(error_file_handler) 
	logger.addHandler(stream_handler) 
	
class testLink(object):
	''' 
	richUrl = 'http://HOSTNAMEbtfe01.cpth.ie:8080/cp/index.jsp?'
	touchUrl = 'http://HOSTNAMEbtfe01.cpth.ie:8080/cp/index-touch.jsp?'
	'''
	HOSTNAME = 'btdantefe01'	 # 'btdantefe01' 
	UI = 'index.jsp?' # 'index-touch.jsp?'			  touchUi only supported by chrome(User-Agent)
	DMN = 'test.ie'	 # domain
	
	def __init__(self): #,url,uPosition=u"",OS="android",readless=False
		self.HOSTNAMEUrl = 'http://'+self.HOSTNAME+'.cpth.ie:8080/cp/'+ self.UI
		self.touchUrl = 'http://HOSTNAMEbtfe01.cpth.ie:8080/cp/index-touch.jsp?'
			
	def addHeader(self,req,OS=''):
		# add header to access url
		if OS=="android":
			req.add_header('X-OperaMini-Platform', 'Android')
			req.add_header('User-Agent', 'Opera/9.80 (Android; Opera Mini/6.1.26730/26.1005; U; zh)	 Presto/2.8.119 Version/10.54')
			req.add_header('X-OperaMini-Phone-UA', 'Mozilla/5.0 (Linux; U; Android 2.3.4; zh-cn; TCL A906 Build/FSR) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')		
		elif OS=='ios':
			pass
		elif OS=="s60":	   
			req.add_header('X-OperaMini-Platform', 'Series 60')
			req.add_header('User-Agent', 'Opera/9.80 (Series 60; Opera Mini/6.1.22827/26.1006; U; zh) Presto/2.8.119 Version/10.54')
			req.add_header('X-OperaMini-Phone-UA', 'NokiaC6-01/012.002 (Symbian/3; Series60/5.2 Mozilla/5.0; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/525 (KHTML, like Gecko) Version/3.0 BrowserNG/7.2.7.3')
		elif OS=="j2me":
			req.add_header('X-OperaMini-Platform', 'J2ME/MIDP')
			req.add_header('User-Agent', 'Opera/9.80 (J2ME/MIDP; Opera Mini/6.5.28117/26.1341; U; zh) Presto/2.8.119 Version/10.54')
			req.add_header('X-OperaMini-Phone-UA', 'NokiaC6-01/012.002 (Symbian/3; Series60/5.2 Mozilla/5.0; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/525 (KHTML, like Gecko) Version/3.0 BrowserNG/7.2.7.3')
		else:
			pass
			
		req.add_header('X-OperaMini-Screen-Width', '320')
		req.add_header('X-OperaMini-Screen-Height', '480')
		req.add_header('X-OperaMini-ID', 'testuid')
	
		req.add_header('Accept','text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1')
		req.add_header('Connection','Keep-Alive')
		#req.add_header('Accept-Encoding','gzip,deflate')
		req.add_header('Accept-Language','zh-cn,en;q=0.9')	  
	
		return req
	
	# check url code		
	def check_url(self):
		if self.code ==0 or self.code/100 >= 4:
			return False  
		else:
			print ('check url succesfully')
			return True	 

		
	def run(self):
		try:
			req = urllib2.Request(self.HOSTNAMEUrl)
			sockReq = self.addHeader(req)
			sock = urllib2.urlopen(sockReq)		
			self.code = sock.code
			self.check_url()
			sock.close()		

		except urllib2.HTTPError,e:
			self.code = e.code
			logger.error(u"Error: (" + unicode(str(e),'utf-8') + u") " )									  
		except urllib2.URLError,e:
			logger.error(u"Error: (" + unicode(str(e),'utf-8') + u") ")								   
		except Exception,e: 
			logger.error(u"Error: (" + unicode(str(e),'utf-8') + u") ")		
	

				
if __name__ == '__main__':
	link=testLink()
	link.run()
