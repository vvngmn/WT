import unittest
import Handler, testContact #, testMail, testCalendar

URLLINK = 'http://http.btstaging.cpcloud.co.uk/cp/dd' #ENV	http://btdantefe01.cpth.ie:8080/cp/dd	
# global CURRENT_USER # qa.596.user29@uat.cpcloud.co.uk	build768.user22@test.ie
CURRENT_USER = 'build768.user22@test.ie' # qa.596.user29@uat.cpcloud.co.uk	build768.user22@test.ie
initHandler = Handler.initHandler()

# 执行测试的类
class testSets(unittest.TestCase):
	def setUp(self):
		initHandler.login(CURRENT_USER,URLLINK)
		contact = testContact.contactSets()
		
	def tearDown(self, logout=False):
		logout = True
		
	def testcontactSets(self):
		if contact.testCreateContacts() is True:
			self.result = 'pass'
		else:
			self.result = 'fail'
			
			
		self.assertEqual(self.result, 'pass')
		
	def testmailSets(self):
		pass
		
	def testcalendarSets(self):
		pass
		
# 构造测试集
def suite():
	suite = unittest.TestSuite()
	suite.addTest(testSets("testcontactSets"))
	suite.addTest(testSets("testmailSets"))
	suite.addTest(testSets("testcalendarSets"))
	return suite
# 测试
if __name__ == "__main__":
	unittest.main(defaultTest = 'suite')