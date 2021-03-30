# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
from pathlib import Path
sys.path.insert(
    0,
    os.path.abspath(
        Path(__file__).parents[2] # Get the parent directory three levels up
    )
)
sys.path.append(
    os.path.dirname(__file__)
)

# CUSTOM IMPORTS

# import recommonmark
# from recommonmark.transform import AutoStructify
# from recommonmark.parser import CommonMarkParser
# source_parsers = {
#    '.md': CommonMarkParser
# }
# import sphinx_bootstrap_theme

import sphinx_rtd_theme

# -- Project information -----------------------------------------------------

project = 'Fenix Installer'
copyright = '2021, RebornOS'
author = 'Shivanand Pattanshetti'

# The full version, including alpha/beta/rc tags
release = '0.0.1'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.autosummary',
    'sphinx_rtd_theme',
    'sphinxcontrib.mermaid',
    # 'sphinx_automodapi.automodapi',
    # 'sphinx_automodapi.smart_resolver',
    'sphinx.ext.graphviz',
    'sphinx.ext.inheritance_diagram'
]

autosummary_generate = True
graphviz_output_format = 'svg'
source_suffix = ['.rst', '.md']
rst_prolog = """
.. raw:: html

   <style type="text/css">
     span.underlined {
       text-decoration: underline;
     }
   </style>

.. role:: underlined
   :class: underlined
"""
inheritance_graph_attrs = dict(rankdir="TB", size='""')

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_context = {
    'css_files': {'_static/custom.css'}
}
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_logo = 'images/rebornos.svg'
html_theme_options = {
    # 'analytics_id': 'UA-XXXXXXX-1',  #  Provided by Google in your dashboard
    # 'analytics_anonymize_ip': False,
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'both',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    # 'style_nav_header_background': 'blue',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/3/': None}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# Custom functions
def setup(app):
    app.add_config_value(
        'recommonmark_config', {
            'enable_math': True,
            'enable_eval_rst': True,
            'enable_auto_doc_ref': True,
            'auto_code_block': True,
        },
        True
    )
    # app.add_transform(AutoStructify)
