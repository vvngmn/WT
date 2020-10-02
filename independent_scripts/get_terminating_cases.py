import re, sys, requests
from bs4 import BeautifulSoup

date = sys.argv[1] # '2020-03-26'

url='http://virt-openshift-05.lab.eng.nay.redhat.com/buildcorp/Runner-v3/'

print('######## connecting ########')
buildcop_runners = requests.get(url).text
soup = BeautifulSoup(buildcop_runners, features="html.parser") 
tds = soup.find_all("td",{"align":"right"})

print('######## looking for the date jobs ########')
target_jobs = []
for td in tds:
	if date in td.getText(): 
		target_jobs.append(td.parent.find('a').getText())
print('find %i jobs for the target date'%len(target_jobs))

print('######## looking for the terminated scenarios ########')
try:
	for job in target_jobs:
		job_url = url + job + 'console'
		job_log = requests.get(job_url).text

		if 'Test Execution will finish prematurely' in job_log:
			before_terminated, after_terminated = job_log.split('Test Execution will finish prematurely')
			author = re.findall('# @author [\w]+@redhat.com',before_terminated)[-1]
			last_case = re.findall('# @case_id OCP-[\w]+',before_terminated)[-1]
			scenario = re.findall('Scenario: .*# features.*feature',before_terminated.split(last_case)[-1])[0]
			
			print('Job: ' + job)
			print(last_case)
			print(scenario)
			print(author)
			print('Raised message:\n')
			for msg in after_terminated.split('\n')[:5]: print(msg)
			print('\n------------------------')

except Exception as e: print(e)

