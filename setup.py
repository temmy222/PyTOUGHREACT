'''
MIT License

Copyright (c) [2022] [Temitope Ajayi]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
# To use a consistent encoding
from codecs import open
from os import path

import pip

if __name__ == "__main__":
    setup()

# The directory containing this file
# HERE = path.abspath(path.dirname(__file__))

# # exec(open('pytoughreact/version.py').read())

# # Get the long description from the README file
# with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
#     long_description = f.read()

# # This call to setup() does all the work
# setup(
#     #Package Name
#     name="pytoughreact",

#     # Version number (initial):
#     version='0.0.15',

#     #Package Description and Details
#     description="Python Library for automating reaction simulations using TOUGHREACT, TMVOC and TMVOC-BIO",
#     url="https://github.com/temmy222/PyTOUGHREACT/tree/master",

#     #Package Author
#     author="Temitope Ajayi",
#     author_email="ajayi_temmy@yahoo.com",

#     #License
#     license="MIT",


#     packages=find_packages(include=['pytoughreact', 'pytoughreact.*']),
#     include_package_data=True,
#     python_requires='>=3.7',

#     keywords=['python', 'reaction', 'TOUGHREACT', 'TMVOC-BIO', 'Uncertainty quantification', 'Sensitivity Analysis'],
#     install_requires=[
#     "numpy", 
#     "scipy", 
#     "vtk", 
#     "matplotlib",
#     "pandas"
#    ]
# )

#Other Details
# classifiers=[
#     "Intended Audience :: Researchers",
#     "License :: OSI Approved :: MIT License",
#     "Programming Language :: Python",
#     "Programming Language :: Python :: 3",
#     "Programming Language :: Python :: 3.6",
#     "Programming Language :: Python :: 3.7",
#     "Programming Language :: Python :: 3.8",
#     "Programming Language :: Python :: 3.9",
#     "Programming Language :: Python :: 3.10",
#     "Programming Language :: Python :: 3.11",
#     "Operating System :: OS Independent"
# ],
# packages=["pytoughreact", "ChemicalCompositions", "pytough"],
# packages=find_packages(),
# 'repo @ https://github.com/acroucher/PyTOUGH-master.zip#egg=PyTOUGH'
# PyTOUGH @ git+ssh://git@github.com/acroucher/PyTOUGH@master#egg=PyTOUGH
# 'PyTOUGH @ git+https://github.com/acroucher/PyTOUGH.git@master'
    # dependency_links=[
    #     "git+https://github.com/acroucher/PyTOUGH.git#egg=PyTOUGH",
    #     # "git+ssh://git@github.com:acroucher/PyTOUGH.git@1.5.6#egg=PyTOUGH"
    # ],