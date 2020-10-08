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
# $ python3 find_cluster_for_version.py <first job number> <last job number> <expect version>
# eg. $ python3 -Wignore find_cluster_for_version.py 75189 75200 4.5

# Output: list of build id including ALL status
###

import sys
from jenkinsapi.jenkins import Jenkins

username = user_id = "xiaocwan"                              # your name
password = user_token = "11dcdf77f0c368f177a7446390156938c4"   # your token
jenkins_url = "https://mastern-jenkins-csb-openshift-qe.cloud.paas.psi.redhat.com"
job_name = "Launch Environment Flexy"
startJob = int(sys.argv[1]) # first job number Eg. 75189
endJob = int(sys.argv[2])   # last job number Eg. 75190
expect_version = sys.argv[3]    # version in LAUNCHER_VARS Eg. 4.5

jenkins_server = Jenkins(jenkins_url, username, password, timeout=120, ssl_verify=False)
print("===== Login Success on Jenkins =====")

job_server = jenkins_server[job_name]
print("===== Got Runner server ===== \n")

def get_build_status(build):
	if build.is_good():
		return "succeed"
	elif build.is_running(): 
		return "running"
	elif build.stop():	
		return "abort"

try:
	builds = {}
	n = range(startJob, endJob+1)
	for i in n:
		build = job_server.get_build(i)
		build_env = build.get_env_vars()
		print("===== Checking number - %i job: %i ====="%(n.index(i)+1, i) )
		if "LAUNCHER_VARS" in build_env and expect_version in build_env["LAUNCHER_VARS"]:
			print("Find the job: %i"%i )
			builds[i] = get_build_status(build)
			print(builds[i])
			if "installer_payload_image" in build_env["LAUNCHER_VARS"]: print(build_env["LAUNCHER_VARS"])
			if "functionality-testing" in build_env['VARIABLES_LOCATION']: print(build_env['VARIABLES_LOCATION'].split('functionality-testing')[1].split('/versioned-installer')[0])

except Exception as e: 
	print(e)

finally:
	print("##### RESULTS: #####")
	print(builds)

