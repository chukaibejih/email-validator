import os
import re
import dns.resolver
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from Levenshtein import distance as levenshtein_distance

class EmailValidator:
    def __init__(self, domains_file='data/popular_domains.txt', tlds_file='data/popular_tlds.txt', disposable_file='data/disposable_domains.txt', popular_domains=None, popular_tlds=None, disposable_domains=None):
        self.popular_domains = popular_domains or self.load_list_from_file(domains_file)
        self.popular_tlds = popular_tlds or self.load_list_from_file(tlds_file)
        self.disposable_domains = disposable_domains or self.load_list_from_file(disposable_file)

    def load_list_from_file(self, filename):
        file_path = os.path.join(os.path.dirname(__file__), filename)
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]

    def validate(self, email):
        """
        Validate the email format, domain, and TLD. Suggest corrections for common typos.
        
        Args:
            email (str): The email address to validate.
        
        Returns:
            dict: A dictionary containing validation results and suggestions.
        """
        try:
            validate_email(email)
        except ValidationError:
            return {"valid": False, "error": "Invalid email format"}

        user_part, domain_part = email.rsplit('@', 1)

        domain_suggestion = self.suggest_domain(domain_part)
        if domain_suggestion:
            return {"valid": False, "error": f"Invalid domain '{domain_part}'. Did you mean '{domain_suggestion}'?"}

        tld_suggestion = self.suggest_tld(domain_part)
        if tld_suggestion:
            return {"valid": False, "error": f"Invalid TLD '{tld_suggestion[1]}'. Did you mean '{tld_suggestion[0]}'?"}
        
        if self.is_disposable(domain_part):
            return {"valid": False, "error": "Disposable email addresses are not allowed"}

        mx_result = self.mx_record_exists(domain_part)
        if mx_result == "timeout":
            return {"valid": False, "error": f"Operation timed out. Check your connection and try again."}
        elif not mx_result:
            return {"valid": False, "error": f"No MX records found for domain '{domain_part}'"}
        

        return {"valid": True}

    def is_disposable(self, domain):
        """
        Check if the domain is a known disposable email provider.
        
        Args:
            domain (str): The domain part of the email.
        
        Returns:
            bool: True if the domain is disposable, False otherwise.
        """
        return domain in self.disposable_domains

    def suggest_domain(self, domain):
        """
        Suggest a popular domain if there are common typos.
        
        Args:
            domain (str): The domain part of the email.
        
        Returns:
            str: Suggested domain or None if the domain is valid.
        """
        if domain not in self.popular_domains:
            suggestion = min(self.popular_domains, key=lambda x: levenshtein_distance(x, domain))
            return suggestion if levenshtein_distance(suggestion, domain) <= 3 else None
        return None

    def suggest_tld(self, domain):
        """
        Suggest a valid TLD if there are common typos.
        
        Args:
            domain (str): The domain part of the email.
        
        Returns:
            tuple: Suggested TLD and the invalid TLD.
        """
        if '.' in domain:
            domain_name, tld = domain.rsplit('.', 1)
            if tld not in self.popular_tlds:
                suggestion = min(self.popular_tlds, key=lambda x: levenshtein_distance(x, tld))
                return (suggestion, tld) if levenshtein_distance(suggestion, tld) <= 2 else None
        return None

    def mx_record_exists(self, domain):
        """
        Check if the domain has MX records.
        
        Args:
            domain (str): The domain part of the email.
        
        Returns:
            bool: True if MX records exist, False otherwise.
        """
        try:
            dns.resolver.resolve(domain, 'MX')
            return True
        except dns.resolver.Timeout:
            return "timeout"
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            return False