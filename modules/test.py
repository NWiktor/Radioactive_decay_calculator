import unittest
from utils import InputValidatorBaseClass, InputError


class TestInputValidatorBaseClass(unittest.TestCase):

    def test_ival(self):
        valid_class = InputValidatorBaseClass()

        # Base check for empty
        self.assertEqual(valid_class.ival(""), None, "Should be 'None'")
        self.assertEqual(valid_class.ival(None), None, "Should be 'None'")

        # Check for default
        self.assertEqual(valid_class.ival(None, default=23), 23, "Should be 23")

        # Check for invalid input
        with self.assertRaises(InputError):
            valid_class.ival("hahahaha")

        # Check for valid input
        self.assertEqual(valid_class.ival("100_000"), 100000,
                         "Should be 100000")
        self.assertEqual(valid_class.ival("1 000 000"), 1000000,
                         "Should be 1000000")
        self.assertEqual(valid_class.ival(200.0), 200,
                         "Should be 200")
        self.assertEqual(valid_class.ival(200), 200,
                         "Should be 200")

    def test_fval(self):
        valid_class = InputValidatorBaseClass()

        # Base check for empty
        self.assertEqual(valid_class.fval(""), None, "Should be None")
        self.assertEqual(valid_class.fval(None), None, "Should be None")

        # Check for default
        self.assertEqual(valid_class.fval(None, default=23), 23, "Should be 23")

        # Check for invalid input
        with self.assertRaises(InputError):
            valid_class.ival("hahahaha")

        # Check for valid numbers
        self.assertEqual(valid_class.fval("100_000"), 100000,
                         "Should be 100000")
        self.assertEqual(valid_class.fval("1 000 000"), 1000000,
                         "Should be 1000000")
        self.assertEqual(valid_class.fval(200), 200, "Should be 200")
        self.assertEqual(valid_class.fval(200.0), 200, "Should be 200.0")
        self.assertEqual(valid_class.fval(4e+3), 4000, "Should be 4000")

    def test_sval(self):
        valid_class = InputValidatorBaseClass()

        # Base check for empty
        self.assertEqual(valid_class.sval(""), None, "Should be None")
        self.assertEqual(valid_class.sval(None), None, "Should be None")

        # Check for default
        self.assertEqual(valid_class.sval("", default=12), 12,
                         "Should be 12")
        self.assertEqual(valid_class.sval(None, default=23), 23,
                         "Should be 23")
        self.assertEqual(valid_class.sval("haha", default=0), "haha",
                         "Should be 'haha'")

        # Checking for numbers and special default values
        self.assertEqual(valid_class.sval(256), "256", "Should be '256'")
        self.assertEqual(valid_class.sval(100.56), "100.56",
                         "Should be '100.56'")
        self.assertEqual(valid_class.sval(
                None, default="foo", chars=2, suffix="..."),
                "foo", "Should be 'foo'"
        )
        self.assertEqual(valid_class.sval(
                "", default=["foo", "bar"], chars=2, suffix="..."),
                ["foo", "bar"], "Should be '['foo', 'bar']'"
        )
        self.assertEqual(valid_class.sval(
                "a b c d e", default="foo", chars=5, suffix="..."),
                "a b c...", "Should be 'a_b_c...'"
        )

    def test_pval(self):
        valid_class = InputValidatorBaseClass()

        # Base check for empty
        self.assertEqual(valid_class.pval(""), None, "Should be None")
        self.assertEqual(valid_class.pval(None), None, "Should be None")
        self.assertEqual(valid_class.pval("haha"), "haha", "Should be 'haha'")

        # Check for default
        self.assertEqual(valid_class.pval("", default=12), 12, "Should be 12")
        self.assertEqual(valid_class.pval(None, default=23), 23,
                         "Should be 23")
        self.assertEqual(valid_class.pval("haha", default=0), "haha",
                         "Should be 'haha'")

        # Checking for non digital default values
        self.assertEqual(valid_class.pval(
                None, default="foo", chars=2),
                "foo", "Should be 'foo'"
        )
        self.assertEqual(valid_class.pval(
                "", default=["foo", "bar"], chars=2),
                ["foo", "bar"], "Should be '['foo', 'bar']'"
        )
        self.assertEqual(valid_class.pval(
                "a b c d e", default="foo", chars=5),
                "a_b_c", "Should be 'a_b_c'"
        )


if __name__ == '__main__':
    unittest.main()
