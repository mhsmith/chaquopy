# -*- coding: utf-8 -*-
#
# Chaquopy documentation build configuration file, created by
# sphinx-quickstart on Thu May 25 17:30:18 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

from datetime import datetime
import re


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.intersphinx',
              'sphinx_better_subsection']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Chaquopy'
author = u'Chaquo Ltd'
copyright = u'{} {}'.format(datetime.now().year, author)

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The full version, including alpha/beta/rc tags.
#
# Chaquopy: this is no longer auto-generated from VERSION.txt, because that made it awkward to
# release documentation updates between versions.
release = "13.0.0"
# The short X.Y version.
version = release.rpartition(".")[0]

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ["changes"]

# The name of the Pygments (syntax highlighting) style to use.
# Leave unset to use the theme's default style.
# pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

default_role = "code"


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    "light_css_variables": {
        "color-background-border": "#dddddd",                 # Increase contrast
        "toc-title-font-size": "var(--font-size--small--3)",  # Increase size
        "toc-font-size": "var(--font-size--small--2)",        #
    },

    # https://stackoverflow.com/q/57606960
    "dark_css_variables": {
        "color-background-border": "#404040",                 # Increase contrast
    },

}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = ["chaquopy.css"]
html_js_files = []

html_title = "Chaquopy {}".format(version)
html_copy_source = False
html_show_copyright = False
html_show_sphinx = False


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'Chaquopydoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'Chaquopy.tex', u'Chaquopy Documentation',
     u'Chaquo Ltd', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'chaquopy', u'Chaquopy Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'Chaquopy', u'Chaquopy Documentation',
     author, 'Chaquopy', 'One line description of project.',
     'Miscellaneous'),
]


# -- Options for Intersphinx ----------------------------------------------

intersphinx_mapping = {'https://docs.python.org/3': None}


# -- Local extensions -----------------------------------------------------

def setup(app):
    app.connect("source-read", make_changelog_anchors)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

# Sections titled with numbers will by default get auto-numbered anchors like "id5".
# Replace these with anchors suitable for permanent links (based on
# https://github.com/pypa/pip/blob/22.3.1/docs/pip_sphinxext.py).
def make_changelog_anchors(app, docname, source):
    if docname == "changelog":
        lines = source[0].splitlines()
        source[0] = "\n".join(_iter_lines_with_refs(lines))
        # print("FIXME", source[0])

def _iter_lines_with_refs(lines):
    """Transform the input lines to add a ref before each section title.
    This is done by looking one line ahead and locate a title's underline,
    and add a ref before the title text.
    Dots in the version is converted into dash, and a ``v`` is prefixed.
    This makes Sphinx use them as HTML ``id`` verbatim without generating
    auto numbering (which would make the the anchors unstable).
    """
    prev = None
    for line in lines:
        # Transform the previous line to include an explicit ref.
        if _is_version_section_title_underline(prev, line):
            assert prev is not None
            vref = prev.split(None, 1)[0].replace(".", "-")
            yield f".. _`v{vref}`:"
            yield ""  # Empty line between ref and the title.
        if prev is not None:
            yield prev
        prev = line
    if prev is not None:
        yield prev

def _is_version_section_title_underline(prev, curr):
    """Find a ==== line that marks the version section title."""
    if prev is None:
        return False
    if re.match(r"^=+$", curr) is None:
        return False
    if len(curr) < len(prev):
        return False
    return True
