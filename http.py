import urllib2,urllib,httplib,re,os,sys
import sqlite3,cookielib,time

def login():
	try:
		# cookie
		cookie = cookielib.CookieJar()
		cookieProc = urllib2.HTTPCookieProcessor(cookie)
		opener = urllib2.build_opener(cookieProc)
		urllib2.install_opener(opener)

		# request
		header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36'}
		post = {
			'os_username':'qa.596.user29', # build596.user23
			'os_password':'password',
			}
				
		postdata = urllib.urlencode(post)

		req = urllib2.Request(
			# url='http://btdantefe01.cpth.ie:8080/cp/index-touch.jsp?d=test.ie',
			url='http://http.btstaging.cpcloud.co.uk/cp/index-touch.jsp',
			data=postdata,
			headers = header
			)
		res = urllib2.urlopen(req).read(1000)
		print (res)

	except Exception,e:
		print (e)

def getResponse():
	# conn = httplib.HTTPConnection('http://btdantefe01.cpth.ie/',8080) # http://btdantefe01.cpth.ie:8080/cp/index-touch.jsp?d=test.ie
	conn = httplib.HTTPConnection('http://http.btstaging.cpcloud.co.uk','8080') 
	conn.request('GET', '/cp/resources/images/bt/icons/128x128/ic_more.png') # /cp/version.xml
	r1 = conn.getresponse()
	print r1.status, r1.reason


if __name__ == '__main__':	
	login()
	# getResponse()