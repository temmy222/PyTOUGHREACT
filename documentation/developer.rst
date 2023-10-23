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
added to the index.rst file. Examples can be found in the index.rst file for how to add a new file
to it.

Updates to documentation are automatically upladed to https://pytoughreact.readthedocs.io/en/latest/developer.html

Important links
~~~~~~~~~~~~~~~~~~~~
1. https://www.sphinx-doc.org/en/master/tutorial/automatic-doc-generation.html
2. https://www.sphinx-doc.org/en/master/tutorial/getting-started.html#creating-the-documentation-layout
3. https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#literal-blocks
4. https://sphinx-rtd-theme.readthedocs.io/en/stable/installing.html 
5. https://sphinx-tutorial.readthedocs.io/step-3/
6. https://docutils.sourceforge.io/docs/user/rst/quickref.html#block-quotes 
7. https://www.youtube.com/watch?v=BWIrhgCAae0&ab_channel=LearnProgrammingwithJoel
8. https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#cross-referencing-arbitrary-locations


Test
------------------------------
Testing for the software was done using pytest. Before test can be run, pytest has to be
installed using `pip install pytest`. The tests can be run by navigating to
the root folder and running `pytest`. The results are then shown together with the 
coverage of the tests. The settings for the tests can be modified through pyproject.toml