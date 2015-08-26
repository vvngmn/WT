import xlwt, xlrd, datetime, os, re, sys
from sys import argv

class outputResults():
	''' argv[1]-robut output file full path full name
		argv[2]-output xls name '''
	def createxls(self):
		# HmS=datetime.datetime.now().strftime('%H%m%S')
		HmS = argv[2]
		self.file = xlwt.Workbook()	#style_compression=0)
		self.sheet = self.file.add_sheet(HmS)

	def savexls(self,name):
		self.file.save(name+'.xls')
		
	def write_file(self,rowNum,colNum,value):
		self.sheet.write(rowNum,colNum,value) #rowNum, colNum
		
	def run(self, fullpath):
	
		self.createxls()
		xmlfile = open(fullpath)
		xml = xmlfile.read()
		titles = re.findall('.*<test id=".*" name="(.*)">.*',xml)
		results = re.findall('.*</tags>\n.*<status status="(.*)" endtime=.*</status>',xml)
		print (titles, results)
		for title in titles:
			try:
				status = results[titles.index(title)]
				self.write_file(titles.index(title),0,title)
				self.write_file(titles.index(title),1,status)
			except:
				print title + ', '
		xmlfile.close()
		# self.savexls('result'+datetime.datetime.now().strftime('%Y%m%d'))
		self.savexls('result_'+argv[2])
		print 'Done!'
	
class outputTestsuite():
	def readXls(self,file):
		data = xlrd.open_workbook(file)
		table = data.sheets()[3] #debug for sheet
		self.names = table.col_values(1)
		self.result = table.col_values(2)
		self.names.pop(0)
		self.result.pop(0) # output for results
		
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
		output = os.getcwd()+'\\testsuite'+datetime.datetime.now().strftime('%Y%m%d')+'.xml'
		testlinkXML = open(output,'w')
		testlinkXML.write(wholexml)
		testlinkXML.close()
		print 'Done!'
	
	
if __name__=='__main__': 
	# from robot output.xml to excel
	tool = outputResults()
	# inputRobotXml = r'c:\users\didozhao\appdata\local\temp\RIDE_7eljb.d\output.xml'
	inputRobotXml = argv[1]
	tool.run(inputRobotXml)
	
	# # from report excel to testlink testSuite
	# write = outputTestsuite()
	# inputXls = 'sanityTestResult.xls'
	# write.createXML(os.getcwd() + '\\' + inputXls)
	
	
	
	
	