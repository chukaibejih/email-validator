from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict, Union
import os
import re
import dns.resolver
from pathlib import Path
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from Levenshtein import distance as levenshtein_distance
import time

class ValidationResult(Enum):
    VALID = "valid"
    INVALID_FORMAT = "invalid_format"
    INVALID_DOMAIN = "invalid_domain"
    INVALID_TLD = "invalid_tld"
    DISPOSABLE = "disposable"
    NO_MX_RECORD = "no_mx_record"
    TIMEOUT = "timeout"

@dataclass
class ValidationResponse:
    is_valid: bool
    result: ValidationResult
    message: str
    suggestions: Optional[Dict[str, str]] = None

class EmailSafeguard:
    def __init__(
        self,
        check_mx: bool = True,
        allow_disposable: bool = False,
        suggest_corrections: bool = True,
        max_distance: int = 2,
        data_dir: Optional[str] = None,
        dns_timeout: float = 2.0,  # Timeout in seconds
        dns_retries: int = 2,      # Number of retries
        retry_delay: float = 1.0   # Delay between retries in seconds
    ):
        """
        Initialize the email validator with customizable settings.
        
        Args:
            check_mx: Whether to verify MX records
            allow_disposable: Whether to allow disposable email addresses
            suggest_corrections: Whether to suggest corrections for typos
            max_distance: Maximum Levenshtein distance for suggestions
            data_dir: Custom directory for data files
            dns_timeout: Timeout for DNS queries in seconds
            dns_retries: Number of retry attempts for DNS queries
            retry_delay: Delay between retry attempts in seconds
        """
        self.check_mx = check_mx
        self.allow_disposable = allow_disposable
        self.suggest_corrections = suggest_corrections
        self.max_distance = max_distance
        self.dns_timeout = dns_timeout
        self.dns_retries = dns_retries
        self.retry_delay = retry_delay
        
        # Configure DNS resolver
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = self.dns_timeout
        self.resolver.lifetime = self.dns_timeout
        
        data_dir = data_dir or os.path.join(os.path.dirname(__file__), 'data')
        self._load_data(data_dir)

    def _check_mx_record(self, domain: str) -> Union[bool, str]:
        """
        Verify MX records exist for the domain with retry logic.
        
        Args:
            domain: Domain to check for MX records
            
        Returns:
            bool: True if MX records exist, False if not
            str: "timeout" if all retries failed
        """
        attempts = 0
        while attempts <= self.dns_retries:
            try:
                self.resolver.resolve(domain, 'MX')
                return True
            except dns.resolver.Timeout:
                attempts += 1
                if attempts <= self.dns_retries:
                    time.sleep(self.retry_delay)
                    continue
                return "timeout"
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                return False
            except Exception:  # Handle other DNS-related errors
                return False
        return "timeout"

    def _load_data(self, data_dir: str) -> None:
        """Load domain lists from data files."""
        self.popular_domains = self._load_file(os.path.join(data_dir, 'popular_domains.txt'))
        self.popular_tlds = self._load_file(os.path.join(data_dir, 'popular_tlds.txt'))
        self.disposable_domains = self._load_file(os.path.join(data_dir, 'disposable_domains.txt'))

    @staticmethod
    def _load_file(filepath: str) -> List[str]:
        """Load and clean data from a file."""
        try:
            with open(filepath, 'r') as file:
                return [line.strip().lower() for line in file if line.strip()]
        except FileNotFoundError:
            return []

    def validate(self, email: str, skip_mx_on_timeout: bool = True) -> ValidationResponse:
        """
        Validate an email address and provide detailed feedback.
        
        Args:
            email: The email address to validate
            skip_mx_on_timeout: If True, consider email valid if MX check times out
            
        Returns:
            ValidationResponse object containing validation results
        """
        # Basic format validation
        try:
            validate_email(email)
        except ValidationError:
            return ValidationResponse(
                is_valid=False,
                result=ValidationResult.INVALID_FORMAT,
                message="Invalid email format"
            )

        user_part, domain_part = email.rsplit('@', 1)
        domain_part = domain_part.lower()
        
        # Disposable email check
        if not self.allow_disposable and self.is_disposable(domain_part):
            return ValidationResponse(
                is_valid=False,
                result=ValidationResult.DISPOSABLE,
                message="Disposable email addresses are not allowed"
            )

        suggestions = {}
        
        # Domain and TLD suggestions
        if self.suggest_corrections:
            domain_suggestion = self._suggest_domain(domain_part)
            if domain_suggestion:
                suggestions['domain'] = domain_suggestion
            
            tld_suggestion = self._suggest_tld(domain_part)
            if tld_suggestion:
                suggestions['tld'] = tld_suggestion[0]

        # MX record validation
        if self.check_mx:
            mx_result = self._check_mx_record(domain_part)
            if mx_result == "timeout":
                if skip_mx_on_timeout:
                    # Consider email valid but with suggestions if available
                    return ValidationResponse(
                        is_valid=True,
                        result=ValidationResult.VALID,
                        message="Email format is valid (MX check timed out)",
                        suggestions=suggestions if suggestions else None
                    )
                else:
                    return ValidationResponse(
                        is_valid=False,
                        result=ValidationResult.TIMEOUT,
                        message="Operation timed out while checking MX records"
                    )
            elif not mx_result:
                return ValidationResponse(
                    is_valid=False,
                    result=ValidationResult.NO_MX_RECORD,
                    message=f"No MX records found for domain '{domain_part}'"
                )

        # If we have suggestions but the email is otherwise valid
        if suggestions:
            return ValidationResponse(
                is_valid=True,
                result=ValidationResult.VALID,
                message="Email is valid but could be improved",
                suggestions=suggestions
            )

        return ValidationResponse(
            is_valid=True,
            result=ValidationResult.VALID,
            message="Email is valid"
        )

    def is_disposable(self, domain: str) -> bool:
        """Check if the domain is a known disposable email provider."""
        return domain in self.disposable_domains

    def _suggest_domain(self, domain: str) -> Optional[str]:
        """Suggest a similar popular domain."""
        if domain not in self.popular_domains:
            suggestion = min(self.popular_domains, 
                           key=lambda x: levenshtein_distance(x, domain))
            if levenshtein_distance(suggestion, domain) <= self.max_distance:
                return suggestion
        return None

    def _suggest_tld(self, domain: str) -> Optional[tuple]:
        """Suggest a valid TLD for common typos."""
        if '.' in domain:
            domain_name, tld = domain.rsplit('.', 1)
            if tld not in self.popular_tlds:
                suggestion = min(self.popular_tlds, 
                               key=lambda x: levenshtein_distance(x, tld))
                if levenshtein_distance(suggestion, tld) <= self.max_distance:
                    return (suggestion, tld)
        return None

    def _check_mx_record(self, domain: str) -> Union[bool, str]:
        """Verify MX records exist for the domain."""
        try:
            dns.resolver.resolve(domain, 'MX')
            return True
        except dns.resolver.Timeout:
            return "timeout"
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            return False