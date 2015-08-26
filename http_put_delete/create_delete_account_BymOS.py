import httplib
import urllib
import sys
from sys import argv

#Invoke mOS API for mailbox(a.k.a account) creation
def send_request_multiple(user_root, start_number, end_number, hostname, port, domain, passwd, cosid):
	params_dict = {'password': passwd, 'cosId': cosid}
	params = urllib.urlencode(params_dict)

	headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "*/*"}
	# conn = httplib.HTTPConnection(hostname, int(port))

	for x in range(int(start_number), int(end_number)+1):
		email = user_root + str(x) + '@' + domain
		path_withEmail = mxos_path + email
		conn = httplib.HTTPConnection(hostname, int(port))
		conn.request("PUT", path_withEmail, params, headers)
		response = conn.getresponse()
		if response.status == 200:
			print "%s is created succssfully." % email
		else:
			print "Error occured, please check the following info for details."
			print response.status, response.reason
			print response.read()


def delete_account(user_root, start_number, end_number, hostname, port, domain):

	headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "*/*"}
	# conn = httplib.HTTPConnection(hostname, int(port))

	for x in range(int(start_number), int(end_number)+1):
		email = user_root + str(x) + '@' + domain
		path_withEmail = mxos_path + email
		conn = httplib.HTTPConnection(hostname, int(port))
		conn.request("DELETE", path_withEmail, "", headers)
		response = conn.getresponse()
		if response.status == 200:
			print "%s is deleted succssfully." % email
		else:
			print "Error occured, please check the following info for details."
			print response.status, response.reason
			print response.read()


if __name__ == '__main__':

#	if len(argv) == 2 and argv[1] == '-help':
#		print '''
# Usage: 
#	There're two modes on this scripts: 
#	1.
#	2.	
#		'''
#		sys.exit(0)

	#moxs ip(hostname), mxos port, mxos path, usercount, username, userpsd, userdomain, cosid=default
	if len(argv) != 9:
		print 'please input: moxs ip(hostname), mxos port, mxos path, user number, user name, user psd, user domain, cosid=default \n'
		sys.exit(0)
	
	print str(argv)
	mxos_ip = argv[1]
	mxos_port = argv[2]
	mxos_path = argv[3]
	start_number = '1'
	end_number = argv[4]
	user_name = argv[5]
	user_domain = argv[6]
	user_pwd = argv[7]
	cosid = argv[8]
	
	print "You will create %i accounts, from %s to %s through %s, with COSID is %s." % (int(end_number)-int(start_number)+1, user_name+start_number+'@'+user_domain, user_name+end_number+user_domain, mxos_ip+":"+mxos_port+mxos_path, cosid) + '\n'
	
	try:
		delete_account(user_name, start_number, end_number, mxos_ip, mxos_port, user_domain)
	except Exception, e:
		print 'delete account failed! \n'
		print str(e) + '\n'
		
	try:
		send_request_multiple(user_name, start_number, end_number, mxos_ip, mxos_port, user_domain, user_pwd, cosid)
	except Exception, e:
		print str(e) +'\n'
		sys.exit(1)
	sys.exit(0)

	#Get the info from CLI
#	hostname = raw_input("Target mxos hostname or IP address: ")
#	port = raw_input("mxos port: ")
#	path = raw_input("Path of mxos:(default value is /mxos/mailbox/v2/) ")
#	if not path: 
#		path = '/mxos/mailbox/v2/'
#
#	create_or_delete = raw_input("Create or Delete account? (C or D) ")
#	if create_or_delete.lower() == 'c':
#		passwd = raw_input("Account password:(default value is 'test') ")
#		if not passwd:
#			passwd = 'test'
#		cosid = raw_input("CosID account belongs to:(default is 'default') ")
#		if not cosid:
#			cosid = 'default'
#		start_number = raw_input("Provide start_number: ")
#		end_number = raw_input("Provide end_number: ")
#		user_root = raw_input("Provide user root format, e.g. 'steven_test')")
#		domain = raw_input("The expected domain name: ")
#
#		#Confirmaton 
#		print "You will create %i accounts, from %s to %s through %s, with COSID is %s." % (
#			int(end_number)-int(start_number)+1,
#			user_root+start_number+'@'+domain,
#			user_root+end_number+domain,
#			hostname+":"+port+path,
#			cosid
#			)
#
#		# Proceed request or not
#		confirmation = raw_input("Are you going to proceed this?(Y/N, default: Y) ")
#		if	not confirmation or confirmation == 'Y':
#			send_request_multiple(user_root, start_number, end_number, hostname, port, domain, passwd, cosid)
#		else:
#			print "Cancelled!"
#			sys.exit(0)
#
#	elif create_or_delete.lower() == 'd':
#		start_number = raw_input("Provide start_number: ")
#		end_number = raw_input("Provide end_number: ")
#		user_root = raw_input("Provide user root format, e.g. 'steven_test')")
#		domain = raw_input("The expected domain name: ")
#
#		print "You will delete %i accounts, from %s to %s through %s." % (
#			int(end_number)-int(start_number)+1,
#			user_root+start_number+'@'+domain,
#			user_root+end_number+'@'+domain,
#			hostname+":"+port+path,
#			)
#		confirmation = raw_input("Are you going to proceed this?(Y/N, default: Y) ")
#		if	not confirmation or confirmation == 'Y':
#			delete_account(user_root, start_number, end_number, hostname, port, domain)
#		else:
#			print "Cancelled!"
#			sys.exit(0)
#	else:
#		print "Sorry, can't recognize your option."
#		sys.exit(0)

	

