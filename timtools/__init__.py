"""
timtools
Some functions I find myself rewriting frequently
"""

# Add imports here
from .timtools import *

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
