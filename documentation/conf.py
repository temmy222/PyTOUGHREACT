# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


# restructured text link - https://docutils.sourceforge.io/docs/user/rst/quickref.html

import os
import sys
print(sys.executable)
sys.path.insert(0, os.path.abspath("../src/pytoughreact"))

project = 'PyTOUGHREACT'
copyright = '2023, Temitope Ajayi'
author = 'Temitope Ajayi'
release = '1.0.3'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.todo", "sphinx.ext.viewcode", "sphinx.ext.autodoc", "sphinx.ext.autosummary",
              "sphinx.ext.mathjax",
              "sphinx.ext.napoleon", "sphinx.ext.intersphinx", "sphinx.ext.extlinks", 'sphinx_rtd_theme']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


# Add __init__ to documentation
def skip(app, what, name, obj, would_skip, options):
    if name == "__init__":
        return False
    return would_skip


def setup(app):
    app.connect("autodoc-skip-member", skip)
