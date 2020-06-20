# -*- coding: utf-8 -*-

import sys
import os
import re

if not 'READTHEDOCS' in os.environ:
    sys.path.insert(0, os.path.abspath('..'))
sys.path.append(os.path.abspath('./demo/'))

from sphinx.locale import _
from sphinx_rtd_theme import __version__
from docutils.parsers.rst import Directive, directives

project = u'tech-note'
slug = re.sub(r'\W+', '-', project.lower())
version = '1.0.0'
release = '1.0.0'
author = u'ny1030'
copyright = author
language = 'jp'

extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinxcontrib.httpdomain',
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
source_suffix = '.rst'
exclude_patterns = []
locale_dirs = ['locale/']
gettext_compact = False

master_doc = 'index'
suppress_warnings = ['image.nonlocal_uri']
pygments_style = 'native'

intersphinx_mapping = {
    'rtd': ('https://docs.readthedocs.io/en/latest/', None),
    'sphinx': ('http://www.sphinx-doc.org/en/stable/', None),
}

html_theme = 'sphinx_rtd_theme'
#html_theme_options = {
#    'logo_only': True
#}
html_theme_path = ["../.."]
#html_logo = "demo/static/logo-wordmark-light.svg"
#html_show_sourcelink = True

htmlhelp_basename = slug

latex_documents = [
  ('index', '{0}.tex'.format(slug), project, author, 'manual'),
]

man_pages = [
    ('index', slug, project, [author], 1)
]

texinfo_documents = [
  ('index', slug, project, author, slug, project, 'Miscellaneous'),
]

class ToggleDirective(Directive):
    has_content = True
    option_spec = {'header': directives.unchanged}
    optional_arguments = 1

    def run(self):
        node = nodes.container()
        node['classes'].append('toggle-content')

        par = nodes.container()
        par['classes'].append('toggle-header')
        if self.arguments and self.arguments[0]:
            par['classes'].append(self.arguments[0])

        self.state.nested_parse(StringList([self.options["header"]]), self.content_offset, par)
        self.state.nested_parse(self.content, self.content_offset, node)

        return [par, node]

# Extensions to theme docs
def setup(app):
    from sphinx.domains.python import PyField
    from sphinx.util.docfields import Field
    
    app.add_stylesheet('custom.css')
    app.add_javascript("custom.js")
    app.add_javascript("https://cdn.jsdelivr.net/npm/clipboard@1/dist/clipboard.min.js")
    app.add_directive('toggle-header', ToggleDirective)

    app.add_object_type(
        'confval',
        'confval',
        objname='configuration value',
        indextemplate='pair: %s; configuration value',
        doc_field_types=[
            PyField(
                'type',
                label=_('Type'),
                has_arg=False,
                names=('type',),
                bodyrolename='class'
            ),
            Field(
                'default',
                label=_('Default'),
                has_arg=False,
                names=('default',),
            ),
        ]
    )
