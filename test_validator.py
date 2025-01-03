from email_safeguard.validator import EmailSafeguard, ValidationResult
from typing import List
import sys

def test_email_validation(emails: List[str]) -> None:
    """
    Test email validation for a list of email addresses.
    
    Args:
        emails: List of email addresses to validate
    """
    # Initialize the email validator with default settings
    validator = EmailSafeguard(
        check_mx=True,
        allow_disposable=False,
        suggest_corrections=True
    )
    
    print("\nEmail Validation Results:")
    print("-" * 80)
    
    for email in emails:
        try:
            result = validator.validate(email)
            
            # Format the output
            status = "✓" if result.is_valid else "✗"
            
            print(f"\nEmail: {email}")
            print(f"Status: {status} ({result.result.value})")
            print(f"Message: {result.message}")
            print(f"Validation Result: {result.result}")
            
            # Display suggestions if available
            if result.suggestions:
                if 'domain' in result.suggestions:
                    print(f"Suggested domain: {result.suggestions['domain']}")
                if 'tld' in result.suggestions:
                    print(f"Suggested TLD: {result.suggestions['tld']}")
            
        except Exception as e:
            print(f"\nEmail: {email}")
            print(f"Error: An unexpected error occurred - {str(e)}")
            print(f"Type: {type(e).__name__}")

def main():
    # List of email addresses to validate
    email_addresses = [
        "valid.email@example.com",
        "invalid-email",
        "missing@domain",
        "too@many@ats.com",
        "123456@numbers.com",
        "UPPERCASE@DOMAIN.COM",
        "special!chars@domain.co",
        "spaces in@address.com",
        "trailingdot.@domain.com",
        "valid+alias@example.com",
        "user@gmial.com",  # Common typo
        "test@disposable.temp.com",  # Disposable domain
    ]
    
    try:
        test_email_validation(email_addresses)
    except KeyboardInterrupt:
        print("\nValidation process interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn error occurred in the main program: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":  
    main()