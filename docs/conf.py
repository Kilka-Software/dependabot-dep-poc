import pathlib
import re


def read(*parts: str) -> str:
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    path = pathlib.Path(__file__).parent / pathlib.Path(*parts)
    return path.read_text()


def find_version(*file_paths: str) -> str:
    """
    Build a path from *file_paths* and search for a ``__version__``
    string inside.
    """
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# -- Project information -----------------------------------------------------

project = "jsr-core"
copyright = "2021, JaSure Financial Services"
author = "Anri Goosen, Jason Paidoussi, Mantse Tshikhovhokhovho"

# The full version, including alpha/beta/rc tags
release = find_version("../src/jsr_core/__init__.py")
version = release.rsplit(".", 1)[0]


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "classic"

html_theme_options = {
    "sidebar_hide_name": True,
    "light_logo": "logo.png",
    "dark_logo": "logo.png",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "attr": ("https://attrs.rtfd.io/", None),
    "structlog": ("http://structlog.rtfd.io/", None),
}
