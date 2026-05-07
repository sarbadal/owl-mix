import os
import sys
 
# Add your package root to PYTHONPATH
sys.path.insert(0, os.path.abspath('../../..'))

def setup(app):
    app.add_js_file('custom.js')
 
project = 'owlmix-docs'
copyright = '2026, Sarbadal Pal'
author = 'Sarbadal Pal'
release = '0.0.1'
 
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'myst_parser',
]
 
templates_path = ['_templates']
exclude_patterns = []
 
html_theme = 'sphinx_rtd_theme'
 
html_static_path = ['_static']
html_css_files = [
    'custom.css',
]

html_show_sphinx = False
