#!/usr/bin/python
# pip3 install requests
# pass only one parameter which is job id number, eg. job: 181015
import requests, sys

r = requests.get('https://mastern-jenkins-csb-openshift-qe.cloud.paas.psi.redhat.com/job/Runner-v3/%s/consoleText'%sys.argv[1], verify=False).text

failedCases = []
passedCases = []


l = r.split('# @case_id OCP-')
for i in l:
	if 'Scenario' in i:
		if 'RuntimeError' in i: failedCases.append(i.split()[0])
		else: passedCases.append(i.split()[0])

print('--- done search ---')
print('failed cases: '+ str(failedCases))
print('passed cases: '+ str(passedCases))
