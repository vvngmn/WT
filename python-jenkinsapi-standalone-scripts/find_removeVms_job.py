### 
# Requirement
# 1. Have python3 environment
# 2. Install jenkinsapi package via $ pip3 install jenkinsapi (or easy_install)
#    doc: https://jenkinsapi.readthedocs.io/en/latest/
# 3. Set jenkins API token:
#    3.1   Log in to Jenkins. 
#         Click your name (upper-right corner).
#         Click Configure (left-side menu).
#         Click Show API Token.
#    3.2 update for below values: 
#         username : your name
#         password : your token
#         job_name : expected job

# Use directly from terminal: 
# $ python3 find_my_build.py <start number> <end number> <job owner>
# eg. $ python3 -Wignore find_my_build.py 75189 75200 xiaocwan

# Output: list of build id
###

import sys
from jenkinsapi.jenkins import Jenkins

username = "xiaocwan"                              # your name
password = "11dcdf77f0c368f177a7446390156938c4"   # your token
jenkins_url = "https://mastern-jenkins-csb-openshift-qe.cloud.paas.psi.redhat.com"
job_name = "Remove VMs"
# below are params from terminal in order
startJob = int(sys.argv[1]) # first job number Eg. 75189
endJob = int(sys.argv[2])   # last job number Eg. 75190
removed_job = sys.argv[3] # removed flexy job id

jenkins_server = Jenkins(jenkins_url, username, password, timeout=120, ssl_verify=False)
print("===== Login Success on Jenkins ===== \n")

job_server = jenkins_server[job_name]
print("===== Got Runner server ===== \n")

try:
	builds = []
	n = range(startJob, endJob+1)
	for i in n:
		build = job_server.get_build(i)
		build_params = build.get_params()
		print("..... Checking job: %i ....."%i )
		if "BUILD_NUMBER" in build_params and build_params["BUILD_NUMBER"] == removed_job:
			builds.append(i)
			print("## Find job: %i ##\n"%i )

except Exception as e: print(e)
finally:
	print("\n##### RESULTS: #####")
	print(builds)

