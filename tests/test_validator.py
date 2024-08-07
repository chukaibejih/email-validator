import unittest
from email_validator.validator import EmailValidator

class TestEmailValidator(unittest.TestCase):

    def setUp(self):
        # Initialize the EmailValidator before each test
        self.validator = EmailValidator()

    def test_valid_email(self):
        # Test with a valid email
        result = self.validator.validate("valid.email@gmail.com")

        # Check that the email is valid
        self.assertTrue(result["valid"])
        # Ensure there is no error message
        self.assertNotIn("error", result)

    def test_invalid_format(self):
        # Test with an email that has an invalid format
        result = self.validator.validate("invalid-email")

        # Check that the email is invalid
        self.assertFalse(result["valid"])
        # Ensure the correct error message is returned
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Invalid email format")

    def test_disposable_email(self):
        # Test with a known disposable email address
        result = self.validator.validate("test@mailinator.com")

        # Check that the email is invalid
        self.assertFalse(result["valid"])
        # Ensure the correct error message is returned
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Disposable email addresses are not allowed")

    def test_domain_suggestion(self):
        # Test with an email that has a common typo in the domain
        result = self.validator.validate("user@gnail.com")

        # Check that the email is invalid
        self.assertFalse(result["valid"])
        # Ensure the suggestion for the correct domain is present in the error message
        self.assertIn("error", result)
        self.assertIn("Did you mean", result["error"])

    def test_tld_suggestion(self):
        # Test with an email that has a common typo in the TLD
        result = self.validator.validate("user@gmail.co")

        # Check that the email is invalid
        self.assertFalse(result["valid"])
        # Ensure the suggestion for the correct TLD is present in the error message
        self.assertIn("error", result)
        self.assertIn("Did you mean", result["error"])

    def test_mx_record_check(self):
        # Test with an email that has a domain with no MX records
        result = self.validator.validate("user@custom.com")

        # Check that the email is invalid
        self.assertFalse(result["valid"])
        # Ensure the correct error message is returned
        self.assertIn("error", result)
        self.assertIn("No MX records found", result["error"])

    def test_custom_domains(self):
        # Test with a custom list of popular domains
        custom_validator = EmailValidator(popular_domains=["nonexistentdomain.xyz"])
        result = custom_validator.validate("user@nonexistentdomain.xyz")

        # Check that the email is valid according to the custom list
        self.assertTrue(result["valid"])
        # Ensure there is no error message
        self.assertNotIn("error", result)

    def test_custom_tlds(self):
        # Test with a custom list of popular TLDs
        custom_validator = EmailValidator(popular_tlds=["xyz"])
        result = custom_validator.validate("user@nonexistentdomain.xyz")

        # Check that the email is valid according to the custom list
        self.assertTrue(result["valid"])
        # Ensure there is no error message
        self.assertNotIn("error", result)

if __name__ == "__main__":
    unittest.main()
