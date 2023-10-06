Developer Notes
===================================

Summary of important notes for developers modifying the repo

Documentation
------------------------------
Documentation for this repo is done using sphinx and readthedocs. To compile the documentation, 
you need install sphinx and sphinx-rtd-theme using pip. 

The documentation for this project is in the documentation folder. The build 
and source folders are not separated in this project. The build is also called _build
for the project. Important folders and files and their uses are shown below::

    _build/
    An empty directory (for now) that will hold the rendered documentation.

    make.bat and Makefile
    Convenience scripts to simplify some common Sphinx operations, such as rendering the content.

    conf.py
    A Python script holding the configuration of the Sphinx project. It contains the project name and release you specified to sphinx-quickstart, as well as some extra configuration keys.

    index.rst
    The root document of the project, which serves as welcome page and contains the root of the “table of contents tree” (or toctree).

A new page to the documentation is added as a .rst file to the documentation folder and also 
added to the 

