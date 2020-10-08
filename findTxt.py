#filename:findTxt.py 
#funtion: 
    # search all test cases in root folder
    # return full path
    # return certain string in certain pattern (class name,subarea,feature,funcion name)
    # Need run with ipython and transfer to BAT combined with some command
#writen by :wxc 
import os
import re
from re import M
from win32com.client import Dispatch
from xml.dom.minidom import Document

class finder():
    def __init__(self):
        self.result=0
        self.tcIDList=[]
		
        self.xmlName='' # xml 'testcase name'
        self.feature=""
        self.subarea=""
        self.directory='' # py def reader 'path'
        self.file=''      # file name in full path
        self.classN=""    # xml 'class', test case - class name
        self.method=""    # test case def name
        
        self.doc = Document()
        self.testset = self.doc.createElement("testset")
        self.doc.appendChild(self.testset)
    
    def find(self,xls):
        self.xmlReader(xls)
        IdList = self.tcIDList
        # IdList = self.xmlReader(xls)
        for what in IdList:
            self.result=0
            iter=os.walk(os.getcwd())
            for path,folder,file in iter:
                if len(file)!=0:
                    for oneFile in file:
                        self.fileReader(what,oneFile)
                        self.directory = path
            if not self.result:
                print ("sorry,can\'t find '%s' in '%s'"%(what,self.directory))
        print ("\n XML generated: \n" + self.doc.toprettyxml(indent=" "))
        f = open('testset.xml','w')
        f.write(self.doc.toprettyxml(indent = ''))
        f.close()
        
    def xmlReader(self,xls):
        app = Dispatch("Excel.Application")
        app.Visible = 0
        doc = app.Workbooks.Open(xls)
        sheet = doc.Sheets(1)
        content = 1 # There's content in the first line
        i = 1
        while content:
            if (sheet.Cells(i,5).Value): # colum 5 is the value of tcID colum 'E'
                i=i+1
                self.tcIDList.append(sheet.Cells(i,5).Value)
            else:
                content = 0
        app.Quit()

    def fileReader(self,what,oneFile):
        if '.py'and not '.pyc' and not '.xls' and not '.testset' in oneFile:
            if oneFile !='findTxt.py':  #stupid way to ignore this file itself
                fReader=open(oneFile,'rb')
                fString=fReader.read()
                if what in fString:
                    self.searchLogCreater(what,oneFile)
                    self.result=1
                fReader.close
    
    def searchLogCreater(self,what,oneFile):
        print ("Find '%s'"%what+' in: '+ self.directory +'\\'+oneFile) #full path need return in future
        self.xmlName= what
        self.file = oneFile.split(".")[0]
        
        patternFeature = re.compile( r'subarea\s*=\s*(.+)') #something wrong with re pattern
        match = patternFeature.match(oneFile)
        if match:
            self.teature = match.group().split('=')[1]
        
        # print "self.file = %s \n\
               # self.xmlName = %s \n\
               # self.directory = %s \n\
               # self.feature = %s \n\
               # \n"%(self.file,self.xmlName,self.directory,self.feature)    #need to transfer to xml in future
        
        self.xmlTcCreater(self.file,self.xmlName,self.directory,self.feature)
        
    def xmlTcCreater(self,file,xmlName,directory,feature):
        testcase = self.doc.createElement("testcase")
        testcase.setAttribute("directory",directory)
        testcase.setAttribute("file",file)
        testcase.setAttribute("name",xmlName)
        self.testset.appendChild(testcase)
        
        
        
        
        
