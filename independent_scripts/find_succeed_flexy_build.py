### 
# Requirement
# 1. Have python3 environment
# 2. Install jenkinsapi package via $ pip3 install jenkinsapi
# 3. Set jenkins API token:
#    3.1   Log in to Jenkins. 
#         Click your name (upper-right corner).
#         Click Configure (left-side menu).
#         Click Show API Token.
#    3.2 update for below values: 
#         username : your name
#         password : your token

# Use directly from terminal: 
# $ python3 find_succeed_flexy_build.py <build1>, <build2>, ... need white space between args
# eg. $ python3 -Wignore find_succeed_flexy_build.py 84606, 84608 84609 ...

# Output: the build list of status(succeed,running,abort) and build id
###

import sys
from jenkinsapi.jenkins import Jenkins

username = user_id = "xiaocwan"                              # your name
password = "11dcdf77f0c368f177a7446390156938c4"   # your token
jenkins_url = "https://mastern-jenkins-csb-openshift-qe.cloud.paas.psi.redhat.com"
job_name = "Launch Environment Flexy"

jenkins_server = Jenkins(jenkins_url, username, password, timeout=120, ssl_verify=False)
print(" ===== Login Success on Jenkins ===== \n")

job_server = jenkins_server[job_name]
print(" ===== Got Runner server ===== \n\n")

n = sys.argv
del n[0]
try:
	builds = []
	for i in n:
		i = i.replace(',', '')
		i = int(i)
		build = job_server.get_build(i)
		print(" ===== Checking number job: %i ===== \n"%i )
		if build.is_good():
			builds.append("succeed: "+ str(i))
			print(" ===== Find SUCCEED job: %i ===== \n"%i )
		elif build.is_running(): 
			builds.append("running: "+ str(i))
			print(" ===== Find Running job: %i ===== \n"%i )
		elif build.stop():
			builds.append("abort: "+ str(i))
			print(" ===== Find Abort job: %i ===== \n"%i )	

except Exception as e: print(e)
finally:
	print("##### RESULTS: #####")
	print(builds)
