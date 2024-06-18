# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

# Include external folders

# sys.path.insert(0, os.path.abspath('..\mapfbench'))
sys.path.insert(0, os.path.abspath("tutorial"))
sys.path.insert(0, os.path.abspath("..\mapfbench"))
sys.path.insert(0, os.path.abspath("..")) # for Readme

# with pathlib
# import pathlib
# May be needed in future
# path = pathlib.Path(__file__).resolve() / '..' / '..' / 'mapfbench'

project = 'MAPFbench'
copyright = '2024, Stefano Lanza, Luca Leonzio'
author = 'Stefano Lanza, Luca Leonzio'
release = '2.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['myst_parser', 'sphinx.ext.githubpages', 'sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'sphinx.ext.viewcode']
myst_enable_extensions = ["colon_fence"]
templates_path = ['_templates']
exclude_patterns = ['architecture', 'material', '_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
html_title = 'MAPFbench documentation'
