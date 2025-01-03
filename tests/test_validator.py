import unittest
from unittest.mock import patch, MagicMock
import dns.resolver
from pathlib import Path
import tempfile
import os

from email_validator.validator import EmailSafeguard, ValidationResult

class TestEmailSafeguard(unittest.TestCase):
    def setUp(self):
        # Create temporary data files
        self.temp_dir = tempfile.mkdtemp()
        self.create_test_data_files()
        
        # Initialize with test data directory
        self.validator = EmailSafeguard(data_dir=self.temp_dir)
        self.custom_validator = EmailSafeguard(
            check_mx=False,
            allow_disposable=True,
            suggest_corrections=False,
            data_dir=self.temp_dir
        )
        
        # Add MX record mock
        self.mx_patcher = patch('dns.resolver.resolve')
        self.mock_resolve = self.mx_patcher.start()
        self.mock_resolve.return_value = True

    def tearDown(self):
        self.mx_patcher.stop()
        # Clean up temp files
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def create_test_data_files(self):
        """Create test data files with sample domains"""
        popular_domains = ['gmail.com', 'yahoo.com', 'hotmail.com']
        popular_tlds = ['com', 'net', 'org']
        disposable_domains = ['tempmail.com', 'throwaway.com']
        
        self._write_file('popular_domains.txt', popular_domains)
        self._write_file('popular_tlds.txt', popular_tlds)
        self._write_file('disposable_domains.txt', disposable_domains)

    def _write_file(self, filename: str, data: list):
        """Write test data to a file"""
        with open(os.path.join(self.temp_dir, filename), 'w') as f:
            f.write('\n'.join(data))

    def test_custom_data_loading(self):
        """Test loading custom domain and TLD data"""
        custom_data_dir = tempfile.mkdtemp()
        custom_domains = ['custom.com']
        custom_tlds = ['custom']
        
        self._write_file(os.path.join(custom_data_dir, 'popular_domains.txt'), custom_domains)
        self._write_file(os.path.join(custom_data_dir, 'popular_tlds.txt'), custom_tlds)
        
        validator = EmailSafeguard(data_dir=custom_data_dir)
        self.assertEqual(validator.popular_domains, custom_domains)
        self.assertEqual(validator.popular_tlds, custom_tlds)
        
        # Cleanup
        for file in os.listdir(custom_data_dir):
            os.remove(os.path.join(custom_data_dir, file))
        os.rmdir(custom_data_dir)

    def test_domain_suggestions(self):
        """Test domain suggestion functionality"""
        test_cases = [
            ("user@gmial.com", "gmail.com"),
            ("user@yaho.com", "yahoo.com"),
            ("user@hotmial.com", "hotmail.com")
        ]
        
        for email, expected in test_cases:
            with self.subTest(email=email):
                result = self.validator.validate(email)
                self.assertTrue(result.is_valid)
                self.assertIn('domain', result.suggestions)
                self.assertEqual(result.suggestions['domain'], expected)

    def test_tld_suggestions(self):
        """Test TLD suggestion functionality"""
        test_cases = [
            ("user@domain.con", "com"),
            ("user@domain.nett", "net"),
            ("user@domain.kom", "com")
        ]
        
        for email, expected in test_cases:
            with self.subTest(email=email):
                result = self.validator.validate(email)
                self.assertTrue(result.is_valid)
                self.assertIn('tld', result.suggestions)
                self.assertEqual(result.suggestions['tld'], expected)

    def test_disposable_email_detection(self):
        """Test disposable email detection"""
        result = self.validator.validate("user@tempmail.com")
        self.assertFalse(result.is_valid)
        self.assertEqual(result.result, ValidationResult.DISPOSABLE)

        result = self.custom_validator.validate("user@tempmail.com")
        self.assertTrue(result.is_valid)

    def test_edge_cases(self):
        """Test edge cases"""
        edge_cases = [
            "very.long.email@domain.com",
            "user+tag@domain.com",
            "user@domain.co.uk"
        ]
        
        for email in edge_cases:
            with self.subTest(email=email):
                self.mock_resolve.return_value = True
                result = self.validator.validate(email)

                self.assertTrue(result.is_valid)

    def test_concurrent_usage(self):
        """Test concurrent usage"""
        import concurrent.futures
        
        def validate_email(email):
            return self.validator.validate(email)
        
        emails = [f"user{i}@domain.com" for i in range(10)]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(validate_email, emails))
        
        self.assertTrue(all(result.is_valid for result in results))

if __name__ == '__main__':
    unittest.main()