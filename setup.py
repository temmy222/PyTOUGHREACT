# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="pytoughreact",
    version="0.0.2",
    description="Python Library for automating reaction simulations using TOUGHREACT, TMVOC and TMVOC-BIO",
    url="https://pytoughreact.readthedocs.io/",
    author="Temitope Ajayi",
    author_email="ajayi_temmy@yahoo.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    # packages=["pytoughreact", "ChemicalCompositions", "pytough"],
    # packages=find_packages(),
    packages=find_packages(include=['pytoughreact', 'pytoughreact.*']),
    include_package_data=True,
    install_requires=["numpy"]
)