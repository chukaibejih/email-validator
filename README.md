# Email Safeguard

A robust email validation library with domain and TLD suggestions, disposable email detection, and MX record validation.

## Features

- Validates email format using Django's built-in validators.

- Detects disposable email addresses.

- Suggests corrections for common domain and TLD typos.

- Checks for valid MX records for the domain.

## Installation

To install the library, use pip:

```sh

pip install email-safeguard

```

## Usage

### Basic Usage

Here's an example of how to use the `EmailValidator` class:

```python

from email_validator.validator import EmailValidator

validator = EmailValidator()

result = validator.validate("user@example.com")

if result["valid"]:

    print("Email is valid!")

else:

    print("Error:", result["error"])

```

### Custom Domain and TLD Lists

You can customize the lists of popular domains, TLDs, and disposable domains by providing your own text files:

```python

validator = EmailValidator(

    domains_file='path/to/custom_domains.txt',

    tlds_file='path/to/custom_tlds.txt',

    disposable_file='path/to/custom_disposable_domains.txt'

)

```

## Data Files

The library uses three data files for validation:

- **popular_domains.txt**: A list of popular email domains.

- **popular_tlds.txt**: A list of popular top-level domains (TLDs).

- **disposable_domains.txt**: A list of known disposable email domains.

Each file should contain one entry per line.

### Example `popular_domains.txt`

```

gmail.com

yahoo.com

outlook.com

hotmail.com

```

### Example `popular_tlds.txt`

```

com

net

org

edu

```

### Example `disposable_domains.txt`

```

mailinator.com

10minutemail.com

```

## Full Example

Here's a more detailed example demonstrating all features:

```python

import os

from email_validator import EmailValidator

# Initialize the validator with custom data files

validator = EmailValidator(

    domains_file='data/popular_domains.txt',

    tlds_file='data/popular_tlds.txt',

    disposable_file='data/disposable_domains.txt'

)

emails = [

    "valid.email@gmail.com",

    "invalid-email",

    "test@mailinator.com",

    "user@gnail.com",

    "user@gmail.cmo",

    "user@nonexistentdomain.xyz"

]

for email in emails:

    result = validator.validate(email)

    if result["valid"]:

        print(f"{email} is valid!")

    else:

        print(f"Error with {email}: {result['error']}")

```

## Running Tests

To run the tests, use the following command:

```sh

python -m unittest discover

```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to contribute to this project if you want to add new features, improve existing ones, or fix bugs.

## Issues

Please raise and issue for bug reporst, feature requests or suggestions.
## Author

Chukwuka Ibejih

For any questions or feedback, please contact [chukaibejih@gmail.com](mailto:chukaibejih@gmail.com).

## Acknowledgements

This library uses the following third-party packages:

- [Django](https://www.djangoproject.com/) for email validation

- [Levenshtein](https://pypi.org/project/python-Levenshtein/) for string similarity calculations

- [dnspython](https://www.dnspython.org/) for DNS queries


If you love this project, please consider giving me a ⭐