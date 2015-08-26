import urllib2,urllib,re,os,sys
import sqlite3,cookielib,time
from sgmllib import SGMLParser 

global JIRA
JIRA = ''
txt = os.getcwd()+'\\'+'a.txt'
file = open(txt,'r')
resFile = open('aa.txt','a')
inputIssues=''
issueIDs = []
content = ''

BTDanteService = ''
timeout = 60
urllib2.socket.setdefaulttimeout(timeout)

def getUSJira():
	# last id format for which jira login
	if 'MBL' in issueIDs[0]:
		USJira = True
	elif 'BTDANTE' in issueIDs[0]:
		USJira = False
	else:
		print 'invalid id in id list!'
	return USJira

def login():
	try:
		# cookie
		cookie = cookielib.CookieJar()
		cookieProc = urllib2.HTTPCookieProcessor(cookie)
		opener = urllib2.build_opener(cookieProc)
		urllib2.install_opener(opener)
		
		USJira = getUSJira()
		if USJira:
			username='vivianwang'
			url='http://jira.qa.laszlosystems.com/jira/secure/Dashboard.jspa'
		else:
			username='vivian.wang'
			url='http://atlas.cpcloud.eu/login.jsp'
		
		# request
		header = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2'}
		post = {
			'os_username':username,
			'os_password':'123456',
			}
				
		post = urllib.urlencode(post)

		req = urllib2.Request(
			url=url,
			data=post,
			headers = header
			)
		res = urllib2.urlopen(req).read()
		if 'Vivian Wang' in res:
			if USJira:
				print "login succesfully to "+'US Jira'
			else:
				print "login succesfully to "+'Berlin Jira'
		else:
			print 'failed to login'
	except Exception,e:
		print (e)

def readIssue():
	if sys.argv[0]:
		print (sys.argv[0])
		
	for line in file.readlines():
		if line.split('\n')[0]:
			issueIDs.append(line.split('\n')[0])
	return issueIDs
	file.close()
		
def writeFile():
	USJira = getUSJira()
	if USJira:
		BTDanteService = 'http://jira.qa.laszlosystems.com/jira/browse/'
	else:
		BTDanteService = 'http://atlas.cpcloud.eu/browse/'
	
	for issueID in issueIDs:
		fullUrl = BTDanteService + issueID
		content = getContent(fullUrl, readAll = True )
		titleLine = issueID + content+'\n'
		print titleLine
		resFile.write(titleLine)
	resFile.close()

def getContent(url, readAll = True, returnTitle = True, returnQa = True, returnPrty = True):
	req = urllib2.Request(url)
	sock = urllib2.urlopen(req)		
	code = sock.code

	USJira = getUSJira()
	
	if readAll:
		htmlsource = sock.read()
	else:
		htmlsource = sock.read(15000)
	
	content = ''
	if returnTitle:
		if USJira:
			issueTitle = htmlsource.split(']')[1].split('- Laszlo')[0]
		else:
			issueTitle = htmlsource.split(']')[1].split('- CriticalPath')[0]
		content = content + '@' + issueTitle
		
	if returnQa:
		if USJira:
			reporter = htmlsource.split('Reporter:')[1].split('ViewProfile.jspa?')[1].split('>')[1].split('</')[0]
		else:
			reporter = htmlsource.split('issue_summary_reporter')[1].split('>')[1].split('</span')[0]
		content = content + '@' + reporter
	if returnPrty:
		if USJira:
			priority = htmlsource.split('Priority:')[1].split('title=')[1].split('>\n             ')[1].split('</')[0]
		else:
			priority = htmlsource.split('Priority:')[1].split(' /> ')[1].split('                </span>')[0]
		content = content + '@' + priority
		
	# if 'Functional Area:' in htmlsource:
		# functionalArea = htmlsource.split('Functional Area:')[1].split('<span>')[1].split('            </div>')[0]
		# print 'ffffffffffff\n   '+ functionalArea
		# l = re.findall('<span>(.*)</span>',functionalArea)
		# l[0],replace('</span>,                  ','')
		# print l
		
		
		
	sock.close()
	return content
	

if __name__ == '__main__':	
	readIssue()
	login()
	writeFile()
