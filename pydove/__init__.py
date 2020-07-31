import os

try:
    # If a VERSION file exists, use it!
    version_file = os.path.join(os.path.dirname(__file__), "VERSION")
    with open(version_file, "r") as infile:
        __version__ = infile.read().strip()
except NameError:
    __version__ = "unknown (running code interactively?)"
except IOError as ex:
    __version__ = "unknown (%s)" % ex

if __doc__ is not None:  # fix for the ``python -OO``
    __doc__ += "\n@version: " + __version__

__license__ = "None"

__longdescr__ = """\
PyDove is a Python package for computing GameTheory basic concepts."""
__keywords__ = [
    "GameTheory",
]
__url__ = "None"

# Maintainer, contributors, etc.
__maintainer__ = "juadolfob"
__maintainer_email__ = "juadolfob@gmail.com"
__author__ = __maintainer__
__author_email__ = __maintainer_email__

# "Trove" classifiers for Python Package Index.
__classifiers__ = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Intended Audience :: Information Technology",
    "Intended Audience :: Science/Research",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.8",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Game Theory",
]

# support numpy from pypy
try:
    import numpypy
except ImportError:
    pass

# Override missing methods on environments where it cannot be used like GAE.
import subprocess

if not hasattr(subprocess, "PIPE"):
    def _fake_PIPE(*args, **kwargs):
        raise NotImplementedError("subprocess.PIPE is not supported.")


    subprocess.PIPE = _fake_PIPE
if not hasattr(subprocess, "Popen"):
    def _fake_Popen(*args, **kwargs):
        raise NotImplementedError("subprocess.Popen is not supported.")


    subprocess.Popen = _fake_Popen

###########################################################
# TOP-LEVEL MODULES
###########################################################

# Import top-level functionality into top-level namespace

from pydove.gamematrix import *
from pydove.game import *

###########################################################
# PACKAGES
###########################################################

from pydove.util import *

try:
    import numpy
except ImportError:
    pass
