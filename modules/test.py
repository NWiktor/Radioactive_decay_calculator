import unittest
from utils import InputValidatorBaseClass


class TestInputValidatorBaseClass(unittest.TestCase):


     def test_ival(self):
          valid_class = InputValidatorBaseClass()

          # Base check for empty
          self.assertEqual(valid_class.ival("")[0], None, "Should be None")
          self.assertEqual(valid_class.ival(None)[0], None, "Should be None")
          self.assertEqual(valid_class.ival("hahahaha")[0], None, "Should be None")

          # Cheecking of non-digital default-value
          self.assertEqual(valid_class.ival("", default=0)[0], 0, "Should be 0")
          self.assertEqual(valid_class.ival(None, default=0)[0], 0, "Should be 0")
          self.assertEqual(valid_class.ival("hahahaha", default=0)[0], 0, "Should be 0")

          # Checking for non digital default values          
          self.assertEqual(valid_class.ival("hahahaha", default="foo")[0], "foo", "Should be 'foo'")
          self.assertEqual(valid_class.ival("", default=["foo", "bar"])[0], ["foo", "bar"], "Should be '['foo', 'bar']'")

          # Check for valid numbers
          self.assertEqual(valid_class.ival("100_000")[0], 100000, "Should be 100000")
          self.assertEqual(valid_class.ival("1 000 000")[0], 1000000, "Should be 1000000")
          self.assertEqual(valid_class.ival(200.0)[0], 200, "Should be 200")
          self.assertEqual(valid_class.ival(200)[0], 200, "Should be 200")


     def test_fval(self):
          valid_class = InputValidatorBaseClass()

          # Base check for empty
          self.assertEqual(valid_class.fval("")[0], None, "Should be None")
          self.assertEqual(valid_class.fval(None)[0], None, "Should be None")
          self.assertEqual(valid_class.fval("hahahaha")[0], None, "Should be None")

          # Cheecking of non-default default-value
          self.assertEqual(valid_class.fval("", default=0)[0], 0, "Should be 0")
          self.assertEqual(valid_class.fval(None, default=0)[0], 0, "Should be 0")
          self.assertEqual(valid_class.fval("hahahaha", default=0)[0], 0, "Should be 0")

          # Checking for non digital default values
          self.assertEqual(valid_class.fval("hahahaha", default="foo")[0], "foo", "Should be 'foo'")
          self.assertEqual(valid_class.fval("", default=["foo", "bar"])[0], ["foo", "bar"], "Should be '['foo', 'bar']'")

          # Check for valid numbers
          self.assertEqual(valid_class.fval("100_000")[0], 100000, "Should be 100000")
          self.assertEqual(valid_class.fval("1 000 000")[0], 1000000, "Should be 1000000")
          self.assertEqual(valid_class.fval(200)[0], 200, "Should be 200")
          self.assertEqual(valid_class.fval(200.0)[0], 200, "Should be 200.0")
          self.assertEqual(valid_class.fval(4e+3)[0], 4000, "Should be 4000")


     def test_sval(self):
          valid_class = InputValidatorBaseClass()

          # Base check for empty
          self.assertEqual(valid_class.sval("")[0], None, "Should be None")
          self.assertEqual(valid_class.sval(None)[0], None, "Should be None")
          self.assertEqual(valid_class.sval("haha")[0], "haha", "Should be 'haha'")

          # Cheecking of non-default default-value
          self.assertEqual(valid_class.sval("", default=0)[0], 0, "Should be 0")
          self.assertEqual(valid_class.sval(None, default=0)[0], 0, "Should be 0")
          self.assertEqual(valid_class.sval("haha", default=0)[0], "haha", "Should be 'haha'")

          # Checking for non digital default values
          self.assertEqual(valid_class.sval(None, default="foo", chars=2, suffix="...")[0], "foo", "Should be 'foo'")
          self.assertEqual(valid_class.sval("", default=["foo", "bar"], chars=2, suffix="...")[0], ["foo", "bar"], "Should be '['foo', 'bar']'")
          self.assertEqual(valid_class.sval("a b c d e", default="foo", chars=5, suffix="...")[0], "a b c...", "Should be 'a_b_c...'")


     def test_pval(self):
          valid_class = InputValidatorBaseClass()

          # Base check for empty
          self.assertEqual(valid_class.pval("")[0], None, "Should be None")
          self.assertEqual(valid_class.pval(None)[0], None, "Should be None")
          self.assertEqual(valid_class.pval("haha")[0], "haha", "Should be 'haha'")

          # Cheecking of non-default default-value
          self.assertEqual(valid_class.pval("", default=0)[0], 0, "Should be 0")
          self.assertEqual(valid_class.pval(None, default=0)[0], 0, "Should be 0")
          self.assertEqual(valid_class.pval("haha", default=0)[0], "haha", "Should be 'haha'")

          # Checking for non digital default values
          self.assertEqual(valid_class.pval(None, default="foo", chars=2)[0], "foo", "Should be 'foo'")
          self.assertEqual(valid_class.pval("", default=["foo", "bar"], chars=2)[0], ["foo", "bar"], "Should be '['foo', 'bar']'")
          self.assertEqual(valid_class.pval("a b c d e", default="foo", chars=5)[0], "a_b_c", "Should be 'a_b_c'")



if __name__ == '__main__':
    unittest.main()