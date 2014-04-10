import unittest

# 执行测试的类
class test1(unittest.TestCase):
    def setUp(self):
        self.login = 'user login ok ...'
    def tearDown(self):
        self.widget = None
    def testSize(self):
		if 'ok' in self.login:
			self.result = 'pass'
		else:
			self.result = 'fail'
        self.assertEqual(self.result, 'pass')
# 构造测试集
def suite():
    suite = unittest.TestSuite()
    suite.addTest(test1("testSize"))
    return suite
# 测试
if __name__ == "__main__":
    unittest.main(defaultTest = 'suite')