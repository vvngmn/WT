'''
How To Use
python upload_robot_result.py "Fusion" "Webtop - Fusion" test-kate1 "c:\users\kate\appdata\local\temp\RIDEthrlyl.d\output.xml"
'''
from testlink import TestlinkAPIClient, TestLinkHelper
import time, sys, re

def getTestResultMap(fullpath):
	xmlfile = open(fullpath)
	xml = xmlfile.read()
	titles = re.findall('.*<test id=".*" name="(.*)">.*',xml)
	results = re.findall('.*</tags>\n.*<status status="(.*)" endtime=[\s\S]*?</status>',xml)
	result_map = {}#id result
	#print (titles, results)
	for title in titles:
		names = title.split(' : ')#testlink id, case name
		if len(names) < 2:#it is not a regular case name, maybe it is a case for test
			continue
		status = results[titles.index(title)]
		result_map[names[0]] = status[0].lower()
	xmlfile.close()
	return result_map

def upload_case_results(api, testplanid, buildname, platformid, result_map):
	for case_id in result_map.keys():
		print case_id
		try:
			res = ''
			if platformName == 'no_platform':
				res = api.reportTCResult(case_id, testplanid, buildname, result_map[case_id], '' )
			else:
				res = api.reportTCResult1(case_id, testplanid, buildname, platformid, result_map[case_id], '' )
			if not ('Success' in str(res)):
				raise Exception('Import case(%s) result failed !'%case_id)
			print 'imported!'
		except Exception, e:
			print str(e)

	print 'Successfully uploaded all case result to testlink !'

if __name__ == '__main__':
	#retrieve result from output.xml
	print sys.argv
	if len(sys.argv) != 6:
		print 'Please input 5 parameters: project name, testplan name, build name, platform name(input no_platform if there is no platform), fullpath of output.xml'
		print sys.exit()
	projName = sys.argv[1]
	testPlanName = sys.argv[2]
	buildName = sys.argv[3]
	platformName = sys.argv[4]
	robot_result_path = sys.argv[5]
	result_map = getTestResultMap(robot_result_path)
	#prepare to upload test result
	tlapi = TestLinkHelper().connect(TestlinkAPIClient)
	#get testplan id
	testplan_res = tlapi.getTestPlanByName(projName, testPlanName)
	if len(testplan_res) != 1 :
		raise Exception('Find %s testplan(%s) in project(%s)'%(len(testplan_res), testPlanName, projName))
	if not testplan_res[0].has_key('id'):
		raise Exception('Did not find testplan(%s) id!')
	testplan_id = testplan_res[0]['id']
	#get platforms
	platform_id = ''
	if platformName != 'no_platform':
		platform_list = tlapi.getTestPlanPlatforms(testplan_id)
		#[{'notes': '<p>\n\tCPMS+PAB+CAL+CPDS+FS</p>', 'id': '240', 'name': 'Fusion-CPMS Backend'}, {'notes': '<p>\n\tMX+PAB+CAL+mOS+SUR</p>', 'id': '241', 'name': 'Fusion-MX Backend'}]
		for platform in platform_list:
			if platform['name'] == platformName:
				platform_id = platform['id']
		if platform_id == '':
			raise Exception('Can not found platform(%s) id!'%platform_id)
	else:
		platform_id = 'no_platform'

	#create new build if necessary
	build_list = tlapi.getBuildsForTestPlan(testplan_id)
	need_create_new_build = True
	for each_build in build_list:
		if buildName == each_build['name']:
			need_create_new_build = False
	if need_create_new_build:
		print 'need to create new build(%s).'%buildName
		create_build_res = tlapi.createBuild(testplan_id, buildName, 'created automatically by Jenkins.')
		if 'Success' in str(create_build_res):
			print 'Successfully created new build(%s).'%buildName
		else:
			raise Exception('Create new build(%s) failed.'%buildName)
	#upload test result
	upload_case_results(tlapi, testplan_id, buildName, platform_id, result_map)
	