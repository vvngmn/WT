from ftplib import FTP

f=FTP('btdantefe01.cpth.ie')
f.login('vwang','criticalpath')
f.pwd()
f.dir()