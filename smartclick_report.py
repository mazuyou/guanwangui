import unittest
from smartclick import smartclick
import ddt

path = "D:\深信服官网测试2022-04-20-09-20"
text = open(path,"r",encoding="utf8")
testData = []
for line in text.readlines():
    param = line.split("----")
    url = param[0]
    routepath = param[1]
    asserturl = param[2].replace(" ","")
    testData.append([url,routepath,asserturl])
@ddt.ddt
class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    @ddt.data(*testData)
    def testCase(self,testData):
        print(testData)
        returnurl = smartclick(testData[0],testData[1])
        self.assertEqual(testData[2],asserturl)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
        # suite = unittest.TestLoader().loadTestsFromTestCase(TestCase().testCase())
        # exesuite = suite.addTest(suite)
        # unittest.TextTestRunner(verbosity=3).run(exesuite)


