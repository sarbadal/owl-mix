import os
import sys
# import sphinx_bootstrap_theme
 
# Add your package root to PYTHONPATH
sys.path.insert(0, os.path.abspath('../..'))

def setup(app):
    app.add_js_file('custom.js')

html_title = 'OwlMix'
project = 'OwlMix'
copyright = '2026, Sarbadal Pal'
author = 'Sarbadal Pal'
release = '0.0.1'
 
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'myst_parser',
    'sphinx_togglebutton',
    'sphinx_copybutton',
]
 
templates_path = ['_templates']
exclude_patterns = []

html_context = { 
    "READTHEDOCS": False,
    "display_lower_left": False,
}
 
html_theme = 'furo'
# html_theme = 'sphinx_rtd_theme'
# html_theme = 'python_docs_theme'

# html_theme = 'bootstrap'
# html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# html_permalinks_icon = '<span>#</span>'
# html_theme = 'sphinxawesome_theme'
 
html_static_path = ['_static']
html_css_files = [
    'custom.css',
]

html_show_sphinx = False
html_copy_source = False
html_show_sourcelink = False