import xlwt, datetime, os, re, WebtopResponseWrap

class xmltoXls():
	def createxls(self):
		HmS=datetime.datetime.now().strftime('%H%m%S')
		self.file = xlwt.Workbook()	#style_compression=0)
		self.sheet = self.file.add_sheet(HmS)

	def savexls(self,name):
		self.file.save(name+'.xls')
		
	def write_file(self,rowNum,colNum,value):
		self.sheet.write(rowNum,colNum,value) #rowNum, colNum
		
	def run(self):
		xmlfile = open(os.getcwd()+'\\output.xml')
		xml = xmlfile.read()
		titles = re.findall('.*<test id=".*" name="(.*)">.*',xml)
		results = re.findall('.*</tags>\n.*<status status="(.*)" endtime=.*</status>',xml)
		print (titles, results)
		for title in titles:
			status = results[titles.index(title)]
			self.write_file(titles.index(title),0,title)
			self.write_file(titles.index(title),1,status)
		xmlfile.close()
		print 'Done!'
	
if __name__=='__main__': 
	tool = xmltoXls()
	tool.createxls()
	tool.run()
	tool.savexls('hah')