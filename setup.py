from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="email-safeguard",
    version="0.2.0",
    author="Chukwuka Ibejih",
    author_email="chukaibejih@gmail.com",
    description="A comprehensive email validation library with smart suggestions and security features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chukaibejih/email-safeguard",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    package_data={
        'email_safeguard': ['data/*.txt'],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Email",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "django>=3.0",
        "python-Levenshtein>=0.12.0",
        "dnspython>=2.0.0",
        "typing-extensions>=4.0.0;python_version<'3.8'",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'email-safeguard=email_safeguard.cli:main',
        ],
    },
    test_suite='tests',
    project_urls={
        'Documentation': 'https://github.com/chukaibejih/email-safeguard/wiki',
        'Bug Reports': 'https://github.com/chukaibejih/email-safeguard/issues',
        'Source': 'https://github.com/chukaibejih/email-safeguard',
    },
)