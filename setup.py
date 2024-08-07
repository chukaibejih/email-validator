from setuptools import setup, find_packages

# Read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="email_validator",
    version="0.1.0",
    author="Chukwuka Ibejih",
    author_email="chukaibejih@gmail.com",
    description="A Python library for validating and suggesting corrections for email addresses.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chukaibejih/email-validator",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['data/*.txt'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "django>=3.0",
        "python-Levenshtein",
        "dnspython",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'email_validator=email_validator:main',
        ],
    },
    test_suite='tests',
)
