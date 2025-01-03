# Email Safeguard

A comprehensive email validation library that provides domain suggestions, disposable email detection, and MX record validation with a focus on security and user experience.

[![PyPI version](https://badge.fury.io/py/email-safeguard.svg)](https://badge.fury.io/py/email-safeguard)
[![Python Versions](https://img.shields.io/pypi/pyversions/email-safeguard.svg)](https://pypi.org/project/email-safeguard/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🔍 Smart validation with helpful suggestions
- 🛡️ Disposable email detection
- 📨 MX record validation with configurable timeout handling
- ⚡ Fast and customizable
- 🎯 Type hints and modern Python support
- 🔧 Configurable validation rules
- 🔄 Automatic retry mechanism for DNS queries

## Installation

```bash
pip install email-safeguard
```

## Quick Start

```python
from email_safeguard.validator import EmailSafeguard

validator = EmailSafeguard()
result = validator.validate("user@gmial.com")

if result.is_valid:
    if result.suggestions:
        print(f"Email is valid but did you mean: {result.suggestions.get('domain')}?")
    else:
        print("Email is valid!")
else:
    print(f"Error: {result.message}")
```

## Advanced Usage

### Custom Configuration

```python
validator = EmailSafeguard(
    check_mx=True,              # Enable MX record validation
    allow_disposable=False,     # Reject disposable emails
    suggest_corrections=True,   # Suggest corrections for typos
    max_distance=2,            # Maximum edit distance for suggestions
    dns_timeout=3.0,          # DNS query timeout in seconds
    dns_retries=2,            # Number of retry attempts for DNS queries
    retry_delay=1.0          # Delay between retries in seconds
)
```

### Timeout Handling

You can control how the validator handles MX record timeouts:

```python
# Strict validation (timeouts treated as invalid)
result = validator.validate("example@domain.com", skip_mx_on_timeout=False)

# Lenient validation (timeouts treated as valid with warning)
result = validator.validate("example@domain.com", skip_mx_on_timeout=True)

if result.result == ValidationResult.TIMEOUT:
    print("DNS query timed out")
```

### Handling Results

```python
from email_safeguard.validator import EmailSafeguard, ValidationResult

validator = EmailSafeguard()
result = validator.validate("user@tempmail.com")

# Check the validation result
if result.result == ValidationResult.VALID:
    print("Email is valid!")
elif result.result == ValidationResult.DISPOSABLE:
    print("Disposable emails not allowed")
elif result.result == ValidationResult.INVALID_DOMAIN:
    if result.suggestions and 'domain' in result.suggestions:
        print(f"Invalid domain. Did you mean: {result.suggestions['domain']}?")
elif result.result == ValidationResult.NO_MX_RECORD:
    print("Domain has no mail server")
elif result.result == ValidationResult.TIMEOUT:
    print("MX record check timed out")
```

### ValidationResult Types

The library provides several validation result types:

```python
from email_safeguard.validator import ValidationResult

# Available validation results:
# ValidationResult.VALID          - Email is valid
# ValidationResult.INVALID_FORMAT - Email format is invalid
# ValidationResult.INVALID_DOMAIN - Domain is invalid
# ValidationResult.INVALID_TLD    - Top-level domain is invalid
# ValidationResult.DISPOSABLE     - Domain is a disposable email provider
# ValidationResult.NO_MX_RECORD   - Domain has no MX records
# ValidationResult.TIMEOUT        - MX record check timed out
```

## Validation Response

The `validate()` method returns a `ValidationResponse` object with the following attributes:

```python
class ValidationResponse:
    is_valid: bool              # Whether the email is valid
    result: ValidationResult    # The specific validation result
    message: str               # A descriptive message
    suggestions: Optional[Dict[str, str]]  # Suggested corrections if any
```

## Performance Tuning

Adjust DNS query settings for your needs:

```python
# For faster validation with less reliability
validator = EmailSafeguard(
    dns_timeout=1.0,    # Short timeout
    dns_retries=1,      # Single attempt
    retry_delay=0.5     # Short retry delay
)

# For more reliable validation
validator = EmailSafeguard(
    dns_timeout=5.0,    # Longer timeout
    dns_retries=3,      # More retries
    retry_delay=1.0     # Standard retry delay
)
```

## Data Files

The library uses three customizable data files:

- `popular_domains.txt`: Common email domains
- `popular_tlds.txt`: Valid top-level domains
- `disposable_domains.txt`: Known disposable email providers

### Custom Data Files

```python
validator = EmailSafeguard(data_dir="path/to/data/directory")
```

## Development

### Running Tests

```bash
# Run all tests
python run test_validator
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Chukwuka Ibejih ([chukaibejih@gmail.com](mailto:chukaibejih@gmail.com))

## Acknowledgements

Built with:
- [Django](https://www.djangoproject.com/) - Email validation
- [python-Levenshtein](https://github.com/ztane/python-Levenshtein/) - String similarity
- [dnspython](https://www.dnspython.org/) - DNS queries

---

If you find this library helpful, please give it a ⭐!