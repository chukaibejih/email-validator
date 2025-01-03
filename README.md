# Email Safeguard

A comprehensive email validation library that provides domain suggestions, disposable email detection, and MX record validation with a focus on security and user experience.

[![PyPI version](https://badge.fury.io/py/email-safeguard.svg)](https://badge.fury.io/py/email-safeguard)
[![Python Versions](https://img.shields.io/pypi/pyversions/email-safeguard.svg)](https://pypi.org/project/email-safeguard/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🔍 Smart validation with helpful suggestions
- 🛡️ Disposable email detection
- 📨 MX record validation
- ⚡ Fast and customizable
- 🎯 Type hints and modern Python support
- 🔧 Configurable validation rules

## Installation

```bash
pip install email-safeguard
```

## Quick Start

```python
from email_safeguard import EmailSafeguard

validator = EmailSafeguard()
result = validator.validate("user@gmial.com")

if result.is_valid:
    if result.suggestions:
        print(f"Email is valid but did you mean: {result.suggestions['domain']}?")
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
    max_distance=2             # Maximum edit distance for suggestions
)
```

### Handling Results

```python
from email_safeguard import EmailSafeguard, ValidationResult

validator = EmailSafeguard()
result = validator.validate("user@tempmail.com")

match result.result:
    case ValidationResult.VALID:
        print("Email is valid!")
    case ValidationResult.DISPOSABLE:
        print("Disposable emails not allowed")
    case ValidationResult.INVALID_DOMAIN:
        print(f"Invalid domain. Did you mean: {result.suggestions['domain']}?")
    case ValidationResult.NO_MX_RECORD:
        print("Domain has no mail server")
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
python -m pytest

# Run with coverage
python -m pytest --cov=email_safeguard
```

### Type Checking

```bash
mypy email_safeguard
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