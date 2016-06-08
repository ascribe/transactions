# -*- coding: utf-8 -*-

import sphinx_rtd_theme

from transactions import __version__


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'transactions'
copyright = u'2016, ascribe GmbH'
author = u'transactions contributors'
version = __version__
release = __version__
language = None
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = True

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['_static']
htmlhelp_basename = 'transactionsdoc'

latex_elements = {}
latex_documents = [
    (master_doc, 'transactions.tex', u'transactions Documentation',
     u'transactions contributors', 'manual'),
]

man_pages = [
    (master_doc, 'transactions', u'transactions Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'transactions', u'transactions Documentation',
     author, 'transactions', 'One line description of project.',
     'Miscellaneous'),
]

intersphinx_mapping = {'https://docs.python.org/': None}
