
import unittest

from dbgrep.rexp import any_match, any_match_set

class TestRexp(unittest.TestCase):
    
    def testAnyMatch_singleValue(self):
        self.assertTrue(any_match(['\d+$', 'asd'], '123'))

    def testNoMatch_singleValue(self):
        self.assertFalse(any_match(['\d+$', 'asd'], 'dgjoi'))

    def testAnyMatchSet(self):
        self.assertTrue(any_match_set(['\d+$'], ['sdf', '345']))

    def testAnyNoMatchSet(self):
        self.assertFalse(any_match_set(['\d+$'], ['df', 'dfg']))

