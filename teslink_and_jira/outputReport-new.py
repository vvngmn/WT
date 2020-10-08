import xlwt, xlrd, datetime, os, re, sys
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement as SE
import codecs

class outputResults_xml():
	'''
	create result xml for testlink
	'''
	container = '<results><testproject name="Fusion" prefix="FUS" /><testplan name="Webtop - Sanity check" /><build name="%s"/>%s</results>'
	resultnode = '<testcase external_id="%s"><result>%s</result><notes>%s</notes></testcase>'
	def __init__(self,sheetname,versionname):
		self.sheetname = sheetname
		self.versionname = versionname
	
	def get_results_from_outputxml(self,xlspath,sheetname):
		data = xlrd.open_workbook(xlspath)
		#table = data.sheets()[3] #debug for sheet
		table = data.sheet_by_name(sheetname)
		self.ids = table.col_values(0)
		#self.names = table.col_values(1)
		self.result = table.col_values(2)
		self.notes = table.col_values(3)#notes
		self.ids.pop(0)
		#self.names.pop(0)
		self.result.pop(0)#pop out column title
		self.notes.pop(0)

	def create_resultxml(self, xlspath):
		self.get_results_from_outputxml(xlspath, self.sheetname)
		resultxml = ''
		for (caseid, caseresult, note) in zip(self.ids, self.result, self.notes):
			resultxml = resultxml + self.resultnode%(caseid, caseresult[0].lower(), note)
			
		resultxml = self.container%(self.versionname, resultxml)
	
		output = os.getcwd()+'\\testresult'+datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+'.xml'
		try:
			testlinkXML = codecs.open(output,'w', 'utf-8')
			testlinkXML.write(resultxml)
			testlinkXML.close()
		except:
			raise Exception('unable to save to file!')
			sys.exit()
		
		print 'result xml created successfully!'
		print 'you can find result file:' + output

class outputResults_xls():
	'''
	create xls from output.xml
	'''
	def createxls(self):
		HmS=datetime.datetime.now().strftime('%H%m%S')
		self.file = xlwt.Workbook()	#style_compression=0)
		self.sheet = self.file.add_sheet(HmS)

	def savexls(self,name):
		self.file.save(name+'.xls')
		
	def write_file(self,rowNum,colNum,value):
		self.sheet.write(rowNum,colNum,value) #rowNum, colNum
		
	def run(self, fullpath, dstname=''):
		self.createxls()
		xmlfile = open(fullpath)
		xml = xmlfile.read()
		titles = re.findall('.*<test id=".*" name="(.*)">.*',xml)
		results = re.findall('.*</tags>\n.*<status status="(.*)" endtime=[\s\S]*?</status>',xml)

		#print (titles, results)
		for title in titles:
			status = results[titles.index(title)]
			self.write_file(titles.index(title),0,title)
			self.write_file(titles.index(title),1,status)
		xmlfile.close()
		if not dstname:
			self.savexls('result'+datetime.datetime.now().strftime('%Y%m%d'))
		else:
			self.savexls(dstname)
		print 'xls is created successfully!'
	
class outputTestsuite():
	'''
	create testsuite xml for testlink
	'''
	def readXls(self,robotxml):
		tool = outputResults_xls()
		tempFileName = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '_' + 'temp'
		tool.run(robotxml, tempFileName)
		data = xlrd.open_workbook(tempFileName + '.xls')
		table = data.sheets()[0] #debug for sheet
		self.names = table.col_values(0)
		self.result = table.col_values(1)
		#self.names.pop(0)
		#self.result.pop(0) # output for results
		
	def createXML(self,file):
		self.readXls(file)
		testcase = ''
		for i in zip(self.names, self.result):
			name = i[0]
			result = i[1]
			case = '''
				<testcase internalid="" name="%s"> 
				<node_order><![CDATA[]]></node_order>
				<externalid><![CDATA[]]></externalid>
				<version><![CDATA[]]></version>
				<summary><![CDATA[]]></summary>
				<preconditions><![CDATA[]]></preconditions>
				<execution_type><![CDATA[1]]></execution_type>
				<importance><![CDATA[2]]></importance>
				<steps>
				<step>
				<step_number><![CDATA[1]]></step_number>
				<actions><![CDATA[]]></actions>
				<expectedresults><![CDATA[PASS]]></expectedresults> 
				<execution_type><![CDATA[1]]></execution_type>
				</step>
				</steps>
				</testcase>'''%(name)  #,result
			testcase = testcase + case
		wholexml = '<testcases>%s</testcases>'%testcase.replace('\t','')
		output = os.getcwd()+'\\testsuite'+datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+'.xml'
		testlinkXML = open(output,'w')
		testlinkXML.write(wholexml)
		testlinkXML.close()
		print 'Done!'
	
	
if __name__=='__main__': 
	'''
	name:sheetname.find the latest sheet with 'sheetname'
	type:xls,testcase,result
	'''
	default_output_xml = r'C:\Users\Kate\Desktop\output.xml'

	type = raw_input("Please input type(result, xls, testcase):")
	if not type in ['result', 'xls', 'testcase']:
		print 'not a valid type!'
		sys.exit()
	if type == 'result':
		# from testlink import and excel to testlink results
		sheetName = raw_input("Please input the sheet name of sanityTestResult.xls:")
		if not sheetName:
			print 'not a valid sheet name!'
			sys.exit()
		buildVersion = raw_input("Please input the build version in TestLink:")
		if not buildVersion:
			print 'not a valid build version!'
			sys.exit()	
		fullXlsPath = raw_input("Please input the full path of sanityTestResult.xls:")
		if not fullXlsPath:
			print 'not a valid xls path!'
			sys.exit()			
		test = outputResults_xml(sheetName, buildVersion)
		test.create_resultxml(fullXlsPath)
	elif type == 'xls':
		# from robot output.xml to excel
		outputXMLPath = raw_input("Input full path of Robot output.xml(default path: %s):"%default_output_xml)
		if not outputXMLPath:
			outputXMLPath = default_output_xml
		
		tool = outputResults_xls()
		tool.run(outputXMLPath)
	elif  type == 'testcase':
		# from report excel to testlink testSuite
		outputXMLPath = raw_input("Input full path of Robot output.xml(default path: %s):"%default_output_xml)
		if not outputXMLPath:
			outputXMLPath = default_output_xml

		write = outputTestsuite()
		write.createXML(outputXMLPath)
	else:
		print 'Invalid type!'
		sys.exit()
	
	
	
	
	
	

	

	
	


	
	
	
	